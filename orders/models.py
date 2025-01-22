from django.db import models


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'В ожидании'
        READY = 'Готово'
        PAID = 'Оплачено'


    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, 
                              choices=OrderStatus.choices, 
                              default=OrderStatus.PENDING
                            )
    
    def __str__(self):
        return f'Заказ №{self.id}'

class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Блюдо: {self.name} - {self.price} единиц'
    
class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    dish = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='order_items')
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Заказ №{self.order.id} - {self.dish.name} x {self.amount} шт.'
