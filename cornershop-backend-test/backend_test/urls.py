"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from menus.views import CreateMenuView
from menus.views import ListMenuView
from menus.views import PublishMenuView
from menus.views import DetailMenuView
from menus.views import ListEmployeesSelectionView
from menus.views import Index

from employees.views import EmployeeSelectionsList

from .utils.healthz import healthz


urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path('', Index.as_view(), name="index"),
    path('menus/add/', CreateMenuView.as_view(), name="create_menu"),
    path('menus/', ListMenuView.as_view(), name="list_menus"),
    path('menus/<uuid:id>/publish/', PublishMenuView.as_view(), name="publish_menu"),
    path('menus/<uuid:id>/', DetailMenuView.as_view(), name="detail_menu"),
    path('menus/<uuid:id>/employees/', ListEmployeesSelectionView.as_view(), name="selection"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('employee/orders/', EmployeeSelectionsList.as_view(), name='employee_selection')
]
