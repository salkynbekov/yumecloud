from datetime import timedelta

from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

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


class OrderProductListView(generics.ListAPIView):
    def get_queryset(self):
        order_id = self.kwargs['order_pk']
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail="Заказ не найден")

        return OrderProduct.objects.filter(order_id=order_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        products_data = [
            {
                "product_name": item.product.name,
                "rental_days": item.duration,
                "total_price": item.product_price
            }
            for item in queryset
        ]

        total_sum = sum(item['total_price'] for item in products_data)

        return Response({
            "products": products_data,
            "total_rental_days": sum(item['rental_days'] for item in products_data),
            "total_price": total_sum
        })


class ProductAvailabilityView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        result = []

        for product in products:
            rental_periods = OrderProduct.objects.filter(product=product).select_related('order')
            rental_periods = rental_periods.order_by('order__start_rental')

            busy_periods = [
                (rental.order.start_rental, rental.order.end_rental)
                for rental in rental_periods
            ]

            available_periods = []
            last_end_date = None

            for start_date, end_date in busy_periods:
                if last_end_date:
                    if start_date > last_end_date + timedelta(days=1):
                        available_periods.append((
                            last_end_date + timedelta(days=1),
                            start_date - timedelta(days=1)
                        ))
                last_end_date = end_date

            if last_end_date:
                available_periods.append((last_end_date + timedelta(days=1), None))

            result.append({
                "product_name": product.name,
                "available_periods": [
                    {
                        "start_date": period[0].strftime('%Y-%m-%d'),
                        "end_date": period[1].strftime('%Y-%m-%d') if period[1] else "∞"
                    }
                    for period in available_periods
                ]
            })

        return Response(result)
