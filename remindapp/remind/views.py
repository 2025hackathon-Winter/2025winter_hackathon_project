from django.shortcuts import render
from pathlib import Path
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import CustomUsers
from .forms import CustomUsersCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


# def helloworldfunction(reqest):
#     returnedobject = HttpResponse('<h1>hello world</h1>')
#     return returnedobject

# 2025/2/1 うっちゃん追加　ログイン成功後ルーティング
def index(request):    # ブラウザからアクセスがあった時の処理
    return HttpResponse("Hello, world. You're at the polls index.")

# ログイン機能　2025/2/16 うっちゃん追加 
User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get("username")  # フォームの入力を `email` に変更
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(mailaddress=email)
            except User.DoesNotExist:
                self.add_error("username", "このメールアドレスは登録されていません。")
                return
            
            user = authenticate(mailaddress=email, password=password)
            if user is None:
                self.add_error("password", "パスワードが間違っています。")
            else:
                # ユーザーが認証された場合のみ、ログインを進める
                if user.is_active:  # 必要に応じて有効なユーザーか確認
                    auth_login(self.request, user)
                else:
                    self.add_error("username", "このユーザーは無効です。")

        return self.cleaned_data

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = '/login/'

# メニュー画面　2025/2/16 うっちゃん追加
def menuview(request):
  return render(request,'menu.html') 

# 新規物品登録　2025/2/16 うっちゃん追加
def MyitemsAdd(request):
  return render(request,'new-item-add.html') 

# 設定画面　2025/2/16 うっちゃん追加
def Settings(request):
    return render(request,'setting.html')

def Inquiry(request):
    return render(request,'inquiry.html')

# サインアップ　2025/2/13 MANA追記
class UserCreateView(CreateView):
    model = CustomUsers
    form_class = CustomUsersCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('remind:login')
    

class HelloWorldClass(TemplateView):
    template_name = 'base.html'

