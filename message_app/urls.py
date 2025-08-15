from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('display/', views.display, name='display'),
    path('api/current-message/', views.get_message_api, name='get_message_api'),
]
