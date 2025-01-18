from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name="Название продукта")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="Цена продукта")

    def __str__(self):
        return self.name


class Order(models.Model):
    start_rental = models.DateField(verbose_name="Начало аренды")
    end_rental = models.DateField(verbose_name="Конец аренды")
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      verbose_name="Общая стоимость",
                                      default=None)

    def clean(self):
        if self.start_rental >= self.end_rental:
            raise ValidationError("Дата конца аренды должна быть после даты начала аренды")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id} ({self.start_rental} - {self.end_rental})"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="order_products",
                              verbose_name="Заказ")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="order_products",
                                verbose_name="Продукт")
    product_price = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        verbose_name="Цена продукта в аренде")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность аренды")

    def clean(self):
        overlapping_orders = OrderProduct.objects.filter(
            product=self.product,
            order__start_rental__lt=self.order.end_rental,
            order__end_rental__gt=self.order.start_rental
        ).exclude(order=self.order)

        if overlapping_orders.exists():
            raise ValidationError(f"Продукт {self.product.name} уже в арендован на определенный срок")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} в заказе #{self.order.id}"
