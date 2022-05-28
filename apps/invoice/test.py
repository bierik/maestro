import arrow
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from apps.invoice.models import Invoice
from apps.invoice.services import InvoiceService

from maestro.testing import MaestroTestCase

User = get_user_model()


class CustomerTestCase(MaestroTestCase):
    def test_create_invoice_with_different_address_from_customer(self):
        client = APIClient()
        user = baker.make(User)
        client.force_authenticate(user)

        address1 = baker.make('Address', is_primary=True, address="Address1")
        address2 = baker.make('Address', address="Address2")
        customer = baker.make('Customer', addresses=[address1, address2], first_name="Max", last_name="Muster")

        # Fall back to primary address
        invoice_service = InvoiceService.from_data({"customer": customer.id})
        self.assertEqual("Address1", invoice_service.generate_context(arrow.now(), '1')['address'])

        invoice_service = InvoiceService.from_data({"customer": customer.id, "address": address2.id})
        self.assertEqual("Address2", invoice_service.generate_context(arrow.now(), '1')['address'])
