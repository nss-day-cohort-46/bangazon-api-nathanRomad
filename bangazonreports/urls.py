from django.urls import path
from .views import favseller_list

urlpatterns = [
    path('reports/favseller', favseller_list),
]