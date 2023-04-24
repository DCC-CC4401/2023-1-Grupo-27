from django.urls import path

from . import views

urlpatterns = [
    path("mainApp/", views.index, name="index"),
    path('register/', views.register_user, name='register_user'), # Registro de usuario
    path('login/',views.login_user, name='login'), # Login de usuario
    path('mainApp/',views.logout_user, name='logout'), # Logout
]