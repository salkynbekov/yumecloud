from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound

from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProductDetailView(generics.RetrieveAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order_id = self.kwargs['order_pk']
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail="Заказ не найден")

        return OrderProduct.objects.filter(order_id=order_id)

    def get_object(self):
        queryset = self.get_queryset()
        order_product_index = self.kwargs['order_product_pk']

        obj = queryset[order_product_index - 1] if 0 < order_product_index <= len(queryset) else None
        if not obj:
            raise NotFound(detail="Продукт в заказе не найден")
        return obj