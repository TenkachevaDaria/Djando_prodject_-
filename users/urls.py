from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path("login/", views.LogIn, name="LogIn"),
    path("registration/", views.registration, name="registration"),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('save-payment-method/', views.save_payment_method, name='save_payment_method'),
]
