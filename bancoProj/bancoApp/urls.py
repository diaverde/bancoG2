from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    #path('home', views.home, name='Home'),
    #path('login', views.login, name='login'),
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('newCustomer', views.newCustomer, name='newCustomer'),
    path('getAllCustomers', views.getAllCustomers, name='getAllCustomers'),
    path('getOneCustomer/<int:id>', views.getOneCustomer, name='getOneCustomer'),
    path('updateCustomer/<int:id>', views.updateCustomer, name='updateCustomer'),
    path('deleteCustomer/<int:id>', views.deleteCustomer, name='deleteCustomer'),
    path('account/newAccount', views.newAccount, name='newAccount'),
    path('account/updateAccount/<int:id>', views.updateAccount, name='updateAccount'),
    path('account/deleteAccount/<int:id>', views.deleteAccount, name='deleteAccount'),
]