from rest_framework import routers
from .api_view import DispatcherViewset, BoardViewset, OwnerOperatorViewset, DriverViewset, InvoiceViewset, \
    InvoiceStatusViewset, DocumentsViewset, DriverStatusViewset

router = routers.DefaultRouter()

router.register("dispatcher", DispatcherViewset)
router.register("board", BoardViewset)
router.register("owner-operator", OwnerOperatorViewset)
router.register("driver", DriverViewset)
router.register("invoice", InvoiceViewset)
router.register("invoice-status", InvoiceStatusViewset)
router.register("driver-status", DriverStatusViewset)
router.register("documents", DocumentsViewset)
