from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, OrderProductDetailView, OrderProductListView, ProductAvailabilityView, \
    ProductTotalRentalSumView

router = DefaultRouter()

router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:order_pk>/products/<int:order_product_pk>/', OrderProductDetailView.as_view()),
    path('orders/<int:order_pk>/products/', OrderProductListView.as_view()),
    path('products-availability/', ProductAvailabilityView.as_view()),
    path('products-rental-sum/', ProductTotalRentalSumView.as_view()),

]