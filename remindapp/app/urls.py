from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('remind/', include('remind.urls')), 
    path('', include('remind.urls')),  # remind アプリのURLを統合
]
