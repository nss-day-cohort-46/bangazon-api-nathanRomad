from django.urls import path
from .views import favseller_list
from .views import incomplete_orders_list

urlpatterns = [
    path('reports/favseller', favseller_list),
    path('reports/incompleteorders', incomplete_orders_list),
]