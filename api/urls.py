from .views import CustomerViewSet, LoansViewSet, PaymentsViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'loan', LoansViewSet, basename='loan')
router.register(r'payment', PaymentsViewSet, basename='payment')

urlpatterns = router.urls