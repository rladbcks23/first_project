from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 기본화면으로 이동
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('notebooks/', include('notebook.urls')),
    path('accounts/', include('account.urls'))
]
