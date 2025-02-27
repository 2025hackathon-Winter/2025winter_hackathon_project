from django.contrib import admin
from django.urls import path
# from .views import HelloWorldClass
from .views import CustomLoginView, UserCreateView,CustomLogoutView,MenuView,MyitemsAdd,BoughtItem,ExtendItem
from . import views # 2025/1/31　うっちゃん追加
from django.contrib.auth import views as auth_views # 2025/1/31　うっちゃん追加

app_name = 'remind'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("signup/", UserCreateView.as_view(), name='signup'), # 2025/2/13 MANA追記
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',CustomLogoutView.as_view(),name='logout'),
    # path('menu/', views.MenuView, name='menu'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('myitems/add/', MyitemsAdd.as_view(), name='myitems-add'), # 2025/2/16 うっちゃん追記 新規登録画面
    path('settings/', views.settings_page, name='settings'),
    path('settings/default_term', views.update_default_term, name='default_term'),
    # 2/26　うっちゃん 手こずっているのでコメントアウト
    path('settings/reset_default_term/', views.reset_default_term, name='reset_default_term'),
    path('settings/change_personal_info/', views.change_personal_info, name='change_personal_info'),
    path('inquiry/',views.Inquiry,name='inquiry'),
    path('editmodal/', views.editmodal, name='editmodal'),
    path('bought-item/', BoughtItem.as_view(), name='bought-item'), 
    path('extend-item/', ExtendItem.as_view(), name='extend-item'),
    path('menu/delete', views.delete_item, name='delete-item'),
    path('menu/delete/item', views.delete, name='delete')
]