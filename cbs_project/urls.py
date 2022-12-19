from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name="register"),
    path("add/", views.add_book, name="add"),
    path("read/", views.read_book, name="read"),
    path("unread/", views.unread_book, name="unread")
]
