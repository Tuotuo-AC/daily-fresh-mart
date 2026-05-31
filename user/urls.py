from django.urls import path
from . import views

app_name = 'user'   # 命名空间

urlpatterns = [
    path('send_verify_code/', views.send_verify_code, name='send_verify_code'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address_list, name='address_list'),
    path('address/add/', views.address_add, name='address_add'),
    path('address/edit/<int:pk>/', views.address_edit, name='address_edit'),
    path('address/delete/<int:pk>/', views.address_delete, name='address_delete'),
    path('address/default/<int:pk>/', views.set_default_address, name='set_default'),
]