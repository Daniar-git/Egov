from . import views
from django.urls import path

urlpatterns = [
    path('forma2/', views.FormaView.as_view()),
    # path('forma2/credentials/', views.FormaCredentialsView.as_view()),
    path('forma2/code/', views.FormaCodeView.as_view()),
]
