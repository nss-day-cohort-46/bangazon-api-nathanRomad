from django.urls import path
from .views import favseller_list
from .views import incomplete_orders_list
from .views import completed_orders_list
from .views import inexpensive_products_list
from .views import expensive_products_list

urlpatterns = [
    path('reports/favseller', favseller_list),
    path('reports/incompleteorders', incomplete_orders_list),
    path('reports/completedorders', completed_orders_list),
    path('reports/inexpensiveproducts', inexpensive_products_list),
    path('reports/expensiveproducts', expensive_products_list),
]