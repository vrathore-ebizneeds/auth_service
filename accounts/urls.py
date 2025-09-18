from collections import UserList
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
]