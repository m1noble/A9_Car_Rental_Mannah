from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),  # main menu

    # rubric actions: create / drop / populate / query
    path('create_tables/', views.create_tables, name='create_tables'),
    path('drop_tables/', views.drop_tables, name='drop_tables'),
    path('populate_tables/', views.populate_tables, name='populate_tables'),

    # query pages
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/search/', views.customer_search, name='customer_search'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/search/', views.vehicle_search, name='vehicle_search'),
]
