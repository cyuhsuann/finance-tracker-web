from rest_framework.routers import DefaultRouter
from .views import (
    AccountViewSet,
    CategoryViewSet,
    TransactionViewSet,
    InvestmentViewSet,
)

router = DefaultRouter()
router.register("accounts", AccountViewSet, basename="account")
router.register("categories", CategoryViewSet, basename="category")
router.register("transactions", TransactionViewSet, basename="transaction")
router.register("investments", InvestmentViewSet, basename="investment")

urlpatterns = router.urls
