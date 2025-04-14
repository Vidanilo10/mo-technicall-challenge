from loans.views import LoansViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'loan', LoansViewSet, basename='loan')

urlpatterns = router.urls