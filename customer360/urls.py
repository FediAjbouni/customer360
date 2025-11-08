"""
URL configuration for customer360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

def redirect_to_customers(request):
    return redirect('customer_management:customer_list')

def redirect_to_create(request):
    return redirect('customer_management:customer_create')

def redirect_to_summary(request):
    return redirect('interactions:summary')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # New app URLs
    path('', include('customer_management.urls')),
    path('interactions/', include('interactions.urls')),
    
    # Redirect old URLs to new structure
    path('create/', redirect_to_create, name="old_create"),
    path('summary/', redirect_to_summary, name="old_summary"),
    
    # Legacy URLs for backward compatibility
    path('legacy/', views.index, name="legacy_index"),
    path('legacy/create/', views.create_customer, name="legacy_create_customer"),
    path('legacy/interact/<int:cid>/', views.interact, name="legacy_interact"),
    path('legacy/summary/', views.summary, name="legacy_summary"),
]
