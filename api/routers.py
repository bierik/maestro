from rest_framework import routers
from customer.viewsets import CustomerViewset
from task.viewsets import TaskViewset
from report.viewsets import ReportViewset

router = routers.DefaultRouter()
router.register(r"customers", CustomerViewset)
router.register(r"tasks", TaskViewset)
router.register(r"reports", ReportViewset)
