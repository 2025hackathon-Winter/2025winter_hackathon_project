from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
import uuid

# Create your models here.
class RemindModel(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

# class users(models.Model):
#     uid = models.CharField(max_length=36)
#     mailaddress =models.EmailField(max_length=255)
#     password = models.CharField(max_length=255)
#     default_term = models.PositiveSmallIntegerField()

class UsersManager(BaseUserManager):
    # 普通のユーザー作成
    def create_user(self, mailaddress, password=None, **extra_fields):
        if not mailaddress:
            raise ValueError("メールアドレスは必須です")
        mailaddress = self.normalize_email(mailaddress)
        user = self.model(mailaddress=mailaddress, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # スーパーユーザー作成
    def create_superuser(self, mailaddress, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(mailaddress, password, **extra_fields)

# カスタムユーザーモデル
class CustomUsers(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailaddress = models.EmailField(
        unique=True, 
        verbose_name="メールアドレス",
        error_messages={
            "unique": "このメールアドレスは既に登録されています。",
        },
    )  # メールアドレスを必須にする　verbose_name=""→adminの管理画面での表記を変更できる
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(8, message="パスワードは8文字以上で入力してください。")]
    )
    default_term = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = UsersManager()

    USERNAME_FIELD = "mailaddress"  # ログイン時の識別子を email に変更
    REQUIRED_FIELDS = []  # スーパーユーザー作成時に必要なフィールド（emailとpasswordは自動）
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permission_set',
        blank=True,
    )

    def __str__(self):
        return self.mailaddress
    
class DefaultGoods(models.Model):
    CATEGORY_CHOICES = [
        ("1","日用品"),
        ("2","食品"),
        ("3", "その他"),
        ]
    id = models.SmallAutoField(primary_key=True) # 2025/2/22 うっちゃん追加
    name = models.CharField(max_length=255, verbose_name="物品名")
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, verbose_name="カテゴリ名")
    default_term = models.SmallIntegerField(default=0, verbose_name="通知期間") # 2025/2/22 うっちゃん追加
    is_default = models.BooleanField(default=False, verbose_name="デフォルト物品フラグ") # 2025/2/22 うっちゃん追加

    def __str__(self):
        return self.name

class MyGoods(models.Model):
    id=models.SmallAutoField(primary_key=True) # 2025/2/22 うっちゃん追加
    uid=models.ForeignKey(CustomUsers, on_delete=models. CASCADE) # 2025/2/22 うっちゃん追加
    goods=models.ForeignKey (DefaultGoods,on_delete=models.CASCADE)
    goods_name=models.CharField(max_length=255, verbose_name="管理物品名") #←管理画面で見やすくするために追記 アナザー
    category=models.CharField(max_length=255, verbose_name="カテゴリ")
    purchase_date=models.DateField(verbose_name="購入日")
    next_purchase_date=models.DateField(verbose_name="次回購入日")
    expire_date=models.DateField(blank=True, null=True, verbose_name="賞味期限")
    next_purchase_term=models.SmallIntegerField(verbose_name="次回購入期間") 
    first_term=models.SmallIntegerField(verbose_name="初回期間")#2025/2/16 ΜΑNA記述

    def __str__(self):
        return self.goods_name
