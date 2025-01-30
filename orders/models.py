from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'В ожидании'
        READY = 'Готово'
        PAID = 'Оплачено'

    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    items = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, 
                              choices=OrderStatus.choices, 
                              default=OrderStatus.PENDING
                            )

    def __str__(self):
        return f'Заказ №{self.id}'
    
    def save(self, *args, **kwargs):
        if len(self.items):
            self.total_price = sum(float(item['price']) for item in self.items)
        else:
            self.total_price = 0
        super().save(*args, **kwargs)
        

    def next_status(self):
        if self.status == Order.OrderStatus.PENDING:
            return Order.OrderStatus.READY
        elif self.status == Order.OrderStatus.READY:
            return Order.OrderStatus.PAID
        return Order.OrderStatus.PENDING
