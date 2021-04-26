from rest_framework import routers

from customer.viewsets import CustomerViewset
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
