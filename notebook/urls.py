from django.urls import path
from . import views

app_name = 'notebooks'

urlpatterns = [
    path('', views.index, name='index'),

    # notebook 생성, 세부정보, 수정, 삭제
    path('notebooks/create/', views.notebook_create, name='notebook_create'),
    path('notebooks/<int:notebook_id>/', views.notebook_detail, name='notebook_detail'),
    path('notebooks/<int:notebook_id>/update/', views.notebook_update, name='notebook_update'),
    path('notebooks/<int:notebook_id>/delete/', views.notebook_delete, name='notebook_delete'),

    # post 생성, 세부정보, 수정, 삭제
    path('notebooks/<int:notebook_id>/posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/update/', views.post_update, name='post_update'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),

]
