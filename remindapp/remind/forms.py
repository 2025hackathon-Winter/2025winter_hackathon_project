from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUsers

class CustomUsersCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsers
        fields = ("mailaddress",)  #  username を使わず、email だけで登録