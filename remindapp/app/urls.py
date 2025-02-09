from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('remind/', include('remind.urls')), 
    path('', include('remind.urls')),  # remind アプリのURLを統合
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
