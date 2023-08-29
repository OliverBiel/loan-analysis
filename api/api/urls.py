"""
URL configuration for api project.

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
from django.urls import path
from core.views import CoreViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fields/', CoreViewSet.as_view({'get': 'get_fields'}), name='get_fields'),
    path('loan/', CoreViewSet.as_view({'post': 'save_loan'}), name='save_loan'),
    path('uuid/', CoreViewSet.as_view({'get': 'get_uuid'}), name='get_uuid'),
    path('loans/<str:uuid>', CoreViewSet.as_view({'get': 'get_loans'}), name='get_my_loans'),
]
