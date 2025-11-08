from django.urls import path
from . import views

app_name = 'customer_management'

urlpatterns = [
    # Customer CRUD operations
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # API endpoints
    path('api/search/', views.customer_search_api, name='customer_search_api'),
    
    # Legacy URLs for backward compatibility
    path('legacy/', views.index, name='legacy_index'),
    path('legacy/create/', views.create_customer, name='legacy_create'),
]