from django.urls import path

from . import views

urlpatterns = [
    path("mainApp/", views.index, name="index"),
]