from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('',views.profiles,name="profiles"),
    path('profiles/<str:i>',views.user_profile,name="user-profile"),
    path('login/',views.LoginUser,name="LoginUser"),
    path('logout/',views.LogoutUser,name="LogoutUser"),
    path('account/',views.account,name="Account"),
    path('registerUser/',views.registerUser,name="registerUser"),
]
