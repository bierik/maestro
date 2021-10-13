import tempfile
from datetime import datetime

import arrow
import requests
from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone

from apps.customer.models import Customer
from apps.flat.serializers import FlatInvoiceSerializer
from apps.invoice.models import Invoice
from apps.report.serializers import ReportInvoiceSerializer


class InvoiceService:
    def __init__(self, customer, start, end):
        self.customer = customer
        self.start = start
        self.end = end

    @classmethod
    def from_data(cls, data):
        customer = data.get("customer")
        start = data.get("start")
        end = data.get("end")
        customer = Customer.objects.get(id=customer)
        start = arrow.get(start, tzinfo=settings.TIME_ZONE).date()
        end = arrow.get(end, tzinfo=settings.TIME_ZONE).shift(days=1).date()
        return cls(customer, start, end)

    def generate_content(self, created, number):
        template = get_template("default.html")
        reports = self.customer.reports.filter(
            start__gte=self.start, start__lt=self.end
        )
        flats = self.customer.flats.filter(
            created__gte=self.start, created__lt=self.end
        )
        reports_data = ReportInvoiceSerializer(reports, many=True).data

        subtotal_reports = 0
        for report in list(reports.all()):
            subtotal_reports += report.price()

        flats_data = FlatInvoiceSerializer(flats, many=True).data

        subtotal_flats = 0
        for flat in list(flats):
            subtotal_flats += flat.price

        route_flats_count = reports.filter(route_flat=True).count()
        subtotal_route_flats = (
            route_flats_count * self.customer.primary_address.route_flat
        )

        route_flat_data = [
            {
                "name": "Wegpauschale",
                "price": "{:.2f} CHF".format(self.customer.primary_address.route_flat),
                "amount": route_flats_count,
                "total": "{:.2f} CHF".format(subtotal_route_flats),
            }
        ]

        flats_data = route_flat_data + flats_data

        subtotal_flats += subtotal_route_flats

        total = float(subtotal_flats) + subtotal_reports

        return template.render(
            {
                "sex": self.customer.get_sex_display(),
                "full_name": self.customer.full_name,
                "address": self.customer.primary_address.address,
                "place": self.customer.primary_address.place,
                "zipcode": self.customer.primary_address.zip_code,
                "date": created.format("DD.MM.YYYY"),
                "invoice_place": "Bönigen",
                "invoice_number": number,
                "reports": reports_data,
                "subtotal_reports": "{:.2f} CHF".format(subtotal_reports),
                "flats": flats_data,
                "subtotal_flats": "{:.2f} CHF".format(subtotal_flats),
                "total": "{:.2f} CHF".format(total),
            }
        )

    def generate_invoice_files(self, content):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as html_file:
            html_file.write(content.encode())
        with open(html_file.name, mode="rb") as html_file:
            resp = requests.post(
                f"http://{settings.WEASYPRINT_HOST}:8080", files={"html": html_file}
            )

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
                pdf_file.write(resp.content)
                pdf_file.flush()
                return {
                    "pdf_file": pdf_file,
                    "html_file": html_file,
                }

    def preview_invoice(self):
        content = self.generate_content(arrow.now(), "<Nummer>")
        return self.generate_invoice_files(content)

    def persist_invoice(self):
        invoice = Invoice.objects.create(date=timezone.now(), customer=self.customer)
        content = self.generate_content(
            arrow.get(invoice.created).format("DD.MM.YYYY"), invoice.number()
        )
        invoice_files = self.generate_invoice_files(content)
        html_file = invoice_files["html_file"]
        pdf_file = invoice_files["pdf_file"]
        filename = datetime.now().timestamp()
        invoice.source_file.save(f"{filename}.html", open(html_file.name, "rb"))
        invoice.file.save(f"{filename}.pdf", open(pdf_file.name, "rb"))
        pdf_file.close()
        html_file.close()
