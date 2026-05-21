from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("hotel", views.hotel_detail, name="hotel_detail")
]