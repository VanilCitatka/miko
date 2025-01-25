from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Блюдо: {self.name} - {self.price} единиц'
    

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'В ожидании'
        READY = 'Готово'
        PAID = 'Оплачено'


    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    items = models.ManyToManyField(Item, through='OrderItems')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, 
                              choices=OrderStatus.choices, 
                              default=OrderStatus.PENDING
                            )
    
    def __str__(self):
        return f'Заказ №{self.id}'
    
    def get_total_price(self):
        return sum(item.get_price() for item in self.order_items.all())

class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Заказ №{self.order.id} - {self.dish.name} x {self.amount} шт.'
    
    def get_price(self):
        return self.dish.price * self.amount
