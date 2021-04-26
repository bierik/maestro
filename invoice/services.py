import os
import subprocess
from datetime import datetime

import arrow
from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone

from flat.serializers import FlatInvoiceSerializer
from invoice.models import Invoice
from report.serializers import ReportInvoiceSerializer


class InvoiceService:
    def __init__(self, customer, start, end):
        self.customer = customer
        self.start = start
        self.end = end

    def generate_invoice(self):
        template = get_template("default.tex")
        invoice = Invoice.objects.create(date=timezone.now(), customer=self.customer)
        filename = datetime.now().timestamp()
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
        subtotal_route_flats = route_flats_count * 5
        flats_data.append(
            {
                "name": "Wegpauschale",
                "price": "5.00 CHF",
                "amount": route_flats_count,
                "total": "{:.2f} CHF".format(subtotal_route_flats),
            }
        )
        subtotal_flats += subtotal_route_flats

        total = float(subtotal_flats) + subtotal_reports

        latex_content = template.render(
            {
                "sex": self.customer.get_sex_display(),
                "full_name": self.customer.full_name,
                "address": self.customer.primary_address.address,
                "place": self.customer.primary_address.place,
                "zipcode": self.customer.primary_address.zip_code,
                "date": arrow.get(invoice.created).format("DD.MM.YYYY"),
                "invoice_place": "Bönigen",
                "invoice_number": invoice.number(),
                "reports": reports_data,
                "subtotal_reports": "{:.2f} CHF".format(subtotal_reports),
                "flats": flats_data,
                "subtotal_flats": "{:.2f} CHF".format(subtotal_flats),
                "total": "{:.2f} CHF".format(total),
            }
        )

        latex_file_path = os.path.join(settings.MEDIA_ROOT, f"{filename}.tex")

        with open(latex_file_path, "w") as latex_file:
            latex_file.write(latex_content)

        with open(latex_file_path, "rb") as latex_file:
            invoice.source_file.save(f"{filename}.tex", latex_file)

        subprocess.run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                latex_file_path,
            ],
            cwd=settings.MEDIA_ROOT,
        )

        with open(
            os.path.join(settings.MEDIA_ROOT, f"{filename}.pdf"), "rb"
        ) as pdf_file:
            invoice.file.save(f"{filename}.pdf", pdf_file)