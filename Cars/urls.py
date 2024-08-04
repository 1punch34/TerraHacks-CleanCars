"""
URL configuration for Cars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from .API import get_data, query_data, query_by_brand, query_by_model, get_brands, get_fuel_types, index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('fuel-types/', get_fuel_types, name='get_fuel_types'),
    path('get_data/', get_data, name='get_data'),
    path('query/', query_data, name='query_data'),
    path('brand/<str:brand>/', query_by_brand, name='query_by_brand'),
    path('model/<str:model>/', query_by_model, name='query_by_model'),
    path('brands/', get_brands, name='get_brands'),
    path('', index, name='index'),
]
