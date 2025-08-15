from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('delete/<int:pk>/', views.message_delete, name='message_delete'),
    path('display/', views.display, name='display'),
    path('api/current-message/', views.get_message_api, name='get_message_api'),
    path('messages-admin/', views.AdminPage, name='admin_page'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
]
