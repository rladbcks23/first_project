from django.urls import path
from . import views

app_name = 'notebooks'

urlpatterns = [
    path('', views.index , name='index'),
    path('create/', views.create , name='create'),
    path('update/<int:pk>', views.update , name='update'),
    path('update/<int:pk>', views.delete , name='delete'),
]
