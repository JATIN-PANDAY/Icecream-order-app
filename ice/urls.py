from django.contrib import admin
from django.urls import path,include
from ice import views
urlpatterns = [
    path('', views.index,name='index'),
    path('contact', views.contact,name='contact'),
    path('services', views.services,name='services'),
    path('about', views.about,name='about'),
    # path('order/<int:pk>', views.order,name='order'),
    path('payment_process/<int:pk>',views.payment_process,name='payment_process'),
    # path('userorderpage/<int:pk>', views.userorderpage,name='userorderpage'),    
    path('register', views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('userpage',views.userpage,name='userpage'),
    path('icecream_name/<int:pk>',views.icecream_name,name='icecream_name'),
    path('success',views.success,name='success'),
    path('cart/<int:pk>',views.cart,name='cart'),
    path('showcart',views.showcart,name='showcart'),
    path('deleteitems/<int:pk>',views.deleteitems,name='deleteitems'),

    





]
