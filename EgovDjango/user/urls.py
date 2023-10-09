from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.UserLogin.as_view()),
    path('login/code/', views.LoginCode.as_view()),
]
