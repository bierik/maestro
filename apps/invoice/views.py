from django.db import transaction
from django.http import FileResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from apps.invoice.services import InvoiceService


class PreviewAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.query_params.get("token", "").replace("Token ", "")
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
        return (token.user, None)


class InvoicePreviewView(APIView):
    authentication_classes = [PreviewAuthentication]

    @transaction.atomic
    def get(self, request):
        invoice_service = InvoiceService.from_data(request.query_params)
        invoice = invoice_service.preview_invoice()
        pdf_file = invoice["pdf_file"]
        response = FileResponse(open(pdf_file.name, "rb"))
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response
