from django.contrib import admin
from django.urls import path
from .views import HelloWorldClass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloWorldClass.as_view())
]