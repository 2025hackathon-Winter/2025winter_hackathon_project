from django.shortcuts import render
from pathlib import Path
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import CustomUsers
from .forms import CustomUsersCreationForm


# def helloworldfunction(reqest):
#     returnedobject = HttpResponse('<h1>hello world</h1>')
#     return returnedobject

# 2025/2/1 うっちゃん追加　ログイン成功後ルーティング
def index(request):    # ブラウザからアクセスがあった時の処理
    return HttpResponse("Hello, world. You're at the polls index.")

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    # def form_valid(self, form):
    #     user = form.get_user()
    #     print(user)

    #     # 入力値がDBにいるか検証
    next_page = 'logout'

class CustomLogoutView(LogoutView):
    next_page = '/login/'

    
def menuview(request):
  return render(request,'menu.html') 

# サインアップ　2025/2/13 MANA追記
class UserCreateView(CreateView):
    model = CustomUsers
    form_class = CustomUsersCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('remind:login')
    

class HelloWorldClass(TemplateView):
    template_name = 'base.html'

