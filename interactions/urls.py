from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    # Interaction CRUD operations
    path('', views.InteractionListView.as_view(), name='interaction_list'),
    path('create/', views.InteractionCreateView.as_view(), name='interaction_create'),
    path('create/<int:customer_id>/', views.InteractionCreateView.as_view(), name='interaction_create_for_customer'),
    path('<int:pk>/', views.InteractionDetailView.as_view(), name='interaction_detail'),
    path('<int:pk>/edit/', views.InteractionUpdateView.as_view(), name='interaction_update'),
    path('<int:pk>/delete/', views.InteractionDeleteView.as_view(), name='interaction_delete'),
    
    # Analytics and reporting
    path('summary/', views.summary_view, name='summary'),
    
    # Legacy URLs for backward compatibility
    path('legacy/<int:cid>/', views.interact, name='legacy_interact'),
    path('legacy/summary/', views.summary, name='legacy_summary'),
]