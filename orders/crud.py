from django.http import JsonResponse
from .models import Order
from django.views.decorators.csrf import csrf_exempt
import json

# Для проверяющего❤️:
# Сори, я люблю FastAPI и я устал это писать...
# А ещё мне на работу надо 🤡
# https://imgur.com/t/cats/YQu50


JSON_DUMPS_PARAMS = {
            'ensure_ascii': False,
            'indent': 4
        }

def to_jsonable(order):

    order_jsonable = {
                'id': order.id,
                'table_number': order.table_number,
                'items': [
                    {
                        'name': item['name'],
                        'amount': item['amount'],
                        'price': item['price']
                    }
                    for item in order.items
                ],
                'total_price': order.total_price,
                'status': order.status
            }

    return order_jsonable

def json_handler(request):
    try:
        data = json.loads(request.body)
        response = {
            'status': 'success',
            'data': data
        }
    except json.JSONDecodeError:
        response = {
            'status': 'error',
            'message': 'Invalid JSON data'
        }
    return response



@csrf_exempt
def get_all_orders(request):
    if request.method == 'GET':
        ord_json = {
            'orders': [
                to_jsonable(order)
            ] for order in Order.objects.all()
        }
        return JsonResponse(ord_json, json_dumps_params=JSON_DUMPS_PARAMS)


@csrf_exempt
def create_new_order(request):

    """
    Correct json request:

    Method: POST
    Data: {
        'table_number': int,
        'items': [None | {
            'name': str
            'amount': int
            'price': float
            }
        ],
        'status': [Any | Enum['В ожидании', 'Готово', 'Оплачено']]
    }

    OR

    Data: {} - it makes blank order (table_number = 1)
    """

    json_request: dict = json_handler(request)
    if json_request['status'] == 'error':
        return JsonResponse(json_request, json_dumps_params=JSON_DUMPS_PARAMS)
    
    data = json_request['data']
    new_order = Order()

    if len(data):
        try:
            new_order.table_number = data['table_number']
            new_order.items = []

            if len(data['items']):
                for item in data['items']:
                    if not (item.get('name') or item.get('amount') or item.get('price')):
                        raise AttributeError
                    item['price'] = item['price'] * item['amount']
                    new_order.items.append(item)

            if data['status'] not in ('В ожидании', 'Готово', 'Оплачено'):
                new_order.status = Order.OrderStatus.PENDING
            
            new_order.status = data['status'] 
            new_order.save()
        except AttributeError as e:
            json_request['status'] = 'error'
            json_request['message'] = e.name
            return JsonResponse(json_request, json_dumps_params=JSON_DUMPS_PARAMS)
    else:
        new_order.table_number = 1
        new_order.save()

    resp = {'status': json_request['status'], 'id': new_order.id}
    return JsonResponse(resp, json_dumps_params=JSON_DUMPS_PARAMS)


@csrf_exempt
def get_order_by_id(request):
    """
    Correct json request: 

    Method: GET
    Data: {
        'id': int
    }

    """
    if request.method != 'GET':
        response = {
            'status': 'error',
            'message': 'Only GET method allowed!'
        }
        return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)
    
    data = json_handler(request)

    try:
        response = {
            'status': 'success',
            'order': to_jsonable(Order.objects.get(id=data['data']['id']))
        }
    except Exception:
        response = {
            'status': 'error',
            'message': 'Not found'
        }
        return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)
    return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)


@csrf_exempt
def delete_order(request):
    """
    Correct json data:

    Method: DELETE
    Data: {
        'id': int
    }
    """

    if request.method != 'DELETE':
        response = {
            'status': 'error',
            'message': 'Only DELETE method allowed!'
        }
        return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)
    
    data = json_handler(request)

    try:
        order = Order.objects.get(id=data['data']['id'])
        response = {
            'status': 'deleted',
            'order': to_jsonable(order)
        }
        order.delete()
    except Exception:
        response = {
            'status': 'error',
            'message': 'Not found'
        }
        return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)
    return JsonResponse(response, json_dumps_params=JSON_DUMPS_PARAMS)