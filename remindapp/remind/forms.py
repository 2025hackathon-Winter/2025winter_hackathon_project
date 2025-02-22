from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib.auth import authenticate, login

class CustomUsersCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsers
        fields = ("mailaddress",)  #  username を使わず、email だけで登録

    # フィールドに対して widget を設定してクラスやプレースホルダを追加
    mailaddress = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'registration-input', 'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'registration-input', 'placeholder': 'パスワード'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'registration-input', 'placeholder': 'パスワード確認用'})
    )

# 設定画面の期間一括設定フォーム
class DefaultTermForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = ('default_term',)