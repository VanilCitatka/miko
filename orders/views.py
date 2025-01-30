from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

from orders.froms import ItemForm
from .models import Order

# Create your views here.

class HubHome(ListView):
    model = Order
    template_name='index.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if search_query := self.request.GET.get('search'):
            return super().get_queryset().annotate(
                search=SearchVector('table_number', 'status')
            ).filter(search=search_query)
        return super().get_queryset().order_by('id')

def order_page(request, id):
    order = Order.objects.get(id=id)
    bg_orders = Order.objects.all().order_by('id')
    form = ItemForm()

    return render(request, 'order.html', context={'orders': bg_orders,'order': order, 'form': form})

def create_new_order(request):
    new_order = Order.objects.create(table_number=1)    
    return HttpResponseRedirect(f'/order/{new_order.id}')

def delete_item(request):
    item_id = int(request.GET.get('item_id'))
    order = Order.objects.get(id=request.GET.get('id'))
    del order.items[item_id]
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

def add_item(request):
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
    id = request.POST.get('id')
    Order.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

def shift_end(request):
    paid_orders = Order.objects.filter(status=Order.OrderStatus.PAID)

    shift_sum = sum(paid_order.total_price for paid_order in paid_orders)

    return render(request, 'shift_end.html', context={'orders': paid_orders, 'shift_sum': shift_sum})