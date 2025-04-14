from payments.views import PaymentViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = router.urls