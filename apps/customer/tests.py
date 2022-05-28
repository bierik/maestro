from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from maestro.testing import MaestroTestCase, create_customer

User = get_user_model()


class CustomerTestCase(MaestroTestCase):
    def test_natural_and_legal_customer(self):
        client = APIClient()
        user = baker.make(User)
        client.force_authenticate(user)
        response = client.post(
            reverse_lazy("customer-list"),
            {
                "first_name": "Hugo",
                "last_name": "Boss",
                "price_per_hour": 40,
                "addresses": [
                    {"address": "Dammweg 9", "zip_code": "3012", "place": "Bern"}
                ],
            },
            format="json",
        )
        self.assertEqual(201, response.status_code)

        response = client.post(
            reverse_lazy("customer-list"),
            {
                "company": "Putztrix",
                "price_per_hour": 40,
                "addresses": [
                    {"address": "Dammweg 9", "zip_code": "3012", "place": "Bern"}
                ],
            },
            format="json",
        )
        self.assertEqual(201, response.status_code)

        response = client.post(
            reverse_lazy("customer-list"),
            {
                "company": "Putztrix",
                "first_name": "Hugo",
                "last_name": "Boss",
                "price_per_hour": 40,
                "addresses": [
                    {"address": "Dammweg 9", "zip_code": "3012", "place": "Bern"}
                ],
            },
            format="json",
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {
                "non_field_errors": [
                    "Es muss entweder ein Vor- und Nachname oder eine Firma eingegeben werden."  # noqa
                ]
            },
            response.json(),
        )

    def test_deactivate(self):
        customer = create_customer()
        self.assertTrue(customer.is_active)
        response = self.client.post(
            reverse_lazy("customer-deactivate", kwargs={"pk": customer.pk})
        )
        self.assertEqual(200, response.status_code)
        customer.refresh_from_db()
        self.assertFalse(customer.is_active)

    def test_activate(self):
        customer = create_customer(is_active=False)
        self.assertFalse(customer.is_active)
        response = self.client.post(
            reverse_lazy("customer-activate", kwargs={"pk": customer.pk})
        )
        self.assertEqual(200, response.status_code)
        customer.refresh_from_db()
        self.assertTrue(customer.is_active)
