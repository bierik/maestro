from collections import OrderedDict
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.test import TestCase
from freezegun import freeze_time

from customer.models import Customer
from report.models import Report
from report.serializers import ReportInvoiceSerializer


@freeze_time("2000-01-01")
class ReportInvoiceSerializerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Kevin",
            last_name="Bieri",
            price_per_hour=45,
        )

    def test_rounds_hours_to_quarters(self):
        Report.objects.create(
            start=datetime(2000, 1, 1, 8, 0, 0, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)),
            end=datetime(2000, 1, 1, 9, 13, 0, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)),
            title="Hauswirtschaft",
            customer=self.customer,
        )
        report_invoice_serializer = ReportInvoiceSerializer(
            Report.objects.all(), many=True
        )
        self.assertEqual(
            [
                OrderedDict(
                    {
                        "date": "01.01.2000",
                        "title": "Hauswirtschaft",
                        "hours": "01:15",
                        "price_per_hour": "45.00",
                        "total": "56.25",
                    }
                )
            ],
            report_invoice_serializer.data,
        )
