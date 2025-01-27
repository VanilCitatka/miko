from django.http import HttpResponseRedirect
from django.shortcuts import render

import json 

from orders.froms import ItemForm
from .models import Order

# Create your views here.
def index(request):
    orders = [{
        'id': order.id,
        'table_number': order.table_number,
        'total_price': order.total_price,
        'status': order.status,
        'items': order.items
    } for order in Order.objects.all()]


    return render(request, 'index.html', context={'orders': orders})

def create_new_order(request):
    new_order = Order.objects.create(table_number=1)    
    return HttpResponseRedirect(f'/order/{new_order.id}')

def delete_item(request):
    item_name = request.GET.get('name')
    order = Order.objects.get(id=request.GET.get('id'))
    print(order.items)
    for item_id in range(len(order.items)):
        if order.items[item_id]['name'] == item_name:
            del order.items[item_id]
            break
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def update_status(request):
    order = Order.objects.get(id=request.POST.get('id'))
    order.status = order.next_status()
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def update_header(request):
    print(request.POST)
    order = Order.objects.get(id=request.POST.get('id'))
    order.table_number = int(request.POST.get('table_num'))
    status = request.POST.get('status', None)
    if status:
        order.status = order.next_status()
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    order.save()
    return HttpResponseRedirect('/')

def order_page(request, id):
    order = Order.objects.get(id=id)
    itemform = ItemForm()
    order = {
        'id': order.id,
        'table_number': order.table_number,
        'total_price': order.total_price,
        'status': order.status,
        'items': order.items,
        'check_end': sum(int(item['price']) for item in order.items)
    }

    return render(request, 'order.html', context={'order': order, 'form': itemform})

def update_order(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            id = request.GET.get('id')
            order = Order.objects.get(id=id)
            item = {
                'name': form.cleaned_data['name'],
                'price': form.cleaned_data['price'] * form.cleaned_data['amount'],
                'amount': form.cleaned_data['amount']
            }
            order.items.append(item)
            order.save()
            return HttpResponseRedirect(f'/order/{order.id}')
    return HttpResponseRedirect('/')

def delete_order(request):
    id = request.GET.get('id')
    Order.objects.get(id=id).delete()
    return HttpResponseRedirect('/')