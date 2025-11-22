from django.urls import path
from bot33.views import *
urlpatterns=[
    path('auth/login',login,name='login'),
    path('auth/createAccount',createAccount,name='createAccount'),
]