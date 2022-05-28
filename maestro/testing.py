from django.test import TestCase


from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


class MaestroTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        user = baker.make(User)
        self.client.force_authenticate(user)


def create_customer(**kwargs):
    return baker.make("Customer", **kwargs)
