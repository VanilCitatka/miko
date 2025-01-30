"""
URL configuration for miko_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
import orders.crud
import orders.views

crud_api = [
    path('all', orders.crud.get_all_orders),
    path('create_new_order', orders.crud.create_new_order),
    path('get_by_id', orders.crud.get_order_by_id),
    path('delete_by_id', orders.crud.delete_order)
]

urlpatterns = [
    path('', orders.views.HubHome.as_view()),
    path('delete_order', orders.views.delete_order),
    path('new_order', orders.views.create_new_order),
    path('order/<int:id>', orders.views.order_page),
    path('add_item/', orders.views.add_item),
    path('update_status', orders.views.update_status),
    path('update_order_header', orders.views.update_header),
    path('delete_item', orders.views.delete_item),
    path('shift_end', orders.views.shift_end),
    path('api/', include(crud_api))
]
