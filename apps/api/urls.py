from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from apps.customer.viewsets import (
    CustomerFlatViewset,
    CustomerInvoiceViewset,
    CustomerReportViewset,
    CustomerViewset,
)
from apps.flat.viewsets import FlatTemplateViewset, FlatViewset
from apps.invoice.viewsets import InvoiceViewset
from apps.report.viewsets import ReportViewset
from apps.task.viewsets import TaskViewset
from apps.invoice.views import InvoicePreviewView


def trigger_error(request):
    raise Exception("Sentry Debug")


router = routers.DefaultRouter()
router.register(r"customers", CustomerViewset)
router.register(r"tasks", TaskViewset)
router.register(r"reports", ReportViewset)
router.register(r"invoices", InvoiceViewset)
router.register(r"flats", FlatViewset)
router.register(r"flat_templates", FlatTemplateViewset)

customer_router = nested_routers.NestedSimpleRouter(
    router, r"customers", lookup="customer"
)
customer_router.register(
    r"invoices", CustomerInvoiceViewset, basename="customer-invoice"
)
customer_router.register(r"flats", CustomerFlatViewset, basename="customer-flat")
customer_router.register(r"reports", CustomerReportViewset, basename="customer-report")

urlpatterns = router.urls + customer_router.urls
urlpatterns.append(path("auth/", include("apps.authentication.urls")))
urlpatterns.append(path("invoicepreview/", InvoicePreviewView.as_view()))
urlpatterns.append(
    path("sentry-debug/", trigger_error),
)
