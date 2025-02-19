from django.contrib import admin
from django.urls import path
# from .views import HelloWorldClass
from .views import CustomLoginView, UserCreateView
from .views import CustomLogoutView
from .views import menuview
from . import views # 2025/1/31　うっちゃん追加
from django.contrib.auth import views as auth_views # 2025/1/31　うっちゃん追加

app_name = 'remind'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("signup/", UserCreateView.as_view(), name='signup'), # 2025/2/13 MANA追記
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',CustomLogoutView.as_view(),name='logout'),
    path('menu/', views.menuview, name='menu'),
    path('myitems/add/', views.MyitemsAdd, name='myitems-add'), # 2025/2/16 うっちゃん追記 新規登録画面
    path('setting',views.Settings,name='settings'),
    path('inquiry/',views.Inquiry,name='inquiry'),
    path('', views.index, name='index'), 
    # path('admin/', admin.site.urls),
    # path('hello/', HelloWorldClass.as_view())
]