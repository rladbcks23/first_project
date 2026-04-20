from django.urls import path
from . import views

app_name = 'testimg'

urlpatterns = [
    path('', views.image, name='image')
]
