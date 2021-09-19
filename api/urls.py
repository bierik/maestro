from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from customer.viewsets import (
    CustomerFlatViewset,
    CustomerInvoiceViewset,
    CustomerReportViewset,
    CustomerViewset,
)
from flat.viewsets import FlatTemplateViewset, FlatViewset
from invoice.viewsets import InvoiceViewset
from report.viewsets import ReportViewset
from task.viewsets import TaskViewset

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
urlpatterns.append(path("auth/", include("authentication.urls")))
