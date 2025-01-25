from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Order, Item

# Create your views here.
def index(request):
    orders = [{
        'id': order.id,
        'table_number': order.table_number,
        'total_price': order.total_price,
        'status': order.status,
        'items': [{
            'name': item.dish.name,
            'price': item.get_price(),
            'amount': item.amount
        } for item in order.order_items.all()]
    } for order in Order.objects.all()]


    return render(request, 'index.html', context={'orders': orders})

def create_order(request):
    order = Order.objects.create(table_number=228)
    order.items.set([
        Item.objects.create(name='Борщ', price=1000),
        Item.objects.create(name='Пельмени', price=500)
    ],
    through_defaults={
        'amount': 3
    })
    order.total_price = order.get_total_price()
    order.save()
    return HttpResponseRedirect('/')

def delete_order(request):
    id = request.GET.get('id')
    Order.objects.get(id=id).delete()
    return HttpResponseRedirect('/')