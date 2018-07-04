
from django.urls import path,include
from appfour import views


app_name= 'appfour'

urlpatterns = [
    path('registration/',views.register, name='registration'),
    path('login/',views.user_login, name='login'),
    path('my_profile/',views.my_profile, name='my_profile'),
]
