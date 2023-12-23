"""
URL configuration for backend project.

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
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
import category.views
import currency.views
import transaction.views
import budget.views
import fileupload.views

router = routers.DefaultRouter()
router.register(r"categories", category.views.CategoryView, "categories")
router.register(r"currencies", currency.views.CurrencyView, "currencies")
router.register(r"transactions", transaction.views.TransactionView, "transactions")
router.register(r"budgets", budget.views.BudgetView, "budgets")
router.register(r"uploads", fileupload.views.FileUploadView, "uploads")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", include("django.contrib.auth.urls")),
    path("api/", include(router.urls)),
    path("api/token/", obtain_auth_token, name="token_obtain_pair"),
]
