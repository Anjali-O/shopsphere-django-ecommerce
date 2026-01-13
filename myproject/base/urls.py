from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>',remove,name='remove'),
    path('details/<int:pk>',details,name='details'),
    path('csub/<int:pk>',csub,name='csub'),
    path('cadd/<int:pk>',cadd,name='cadd'),
    path('support/',support, name='support'),
    path('knowus/',knowus, name='knowus'),
    path('payment/',payment,name='payment')


]
