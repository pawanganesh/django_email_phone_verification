from django.urls import path

from .views import home_view, login_attempt, register_attempt

app_name = 'accounts'
urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_attempt, name='login_attempt'),
    path('register/', register_attempt, name='register_attempt'),
]
