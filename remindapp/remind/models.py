from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator

# Create your models here.
class RemindModel(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

# class users(models.Model):
#     uid = models.CharField(max_length=36)
#     mailaddress =models.EmailField(max_length=255)
#     password = models.CharField(max_length=255)
#     default_term = models.PositiveSmallIntegerField()

class defaultgoods(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

class mygoods(models.Model):
    CATEGORY_CHOICES = [
        ("日用品","日用品"),
        ("食料","食料"),
        ("その他","その他")
        ]
    
    id = models.CharField(max_length=255,primary_key=True)
    uid = models.CharField(max_length=36)
    goods_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,choices=CATEGORY_CHOICES)
    purchase_date = models.DateTimeField()
    next_purchase_date = models.DateTimeField()
    expire_date = models.DateTimeField()
    next_purchase_term = models.CharField(max_length=255)
    first_term = models.CharField(max_length=255)

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
    mailaddress = models.EmailField(unique=True, verbose_name="メールアドレス")  # メールアドレスを必須にする　verbose_name=""→adminの管理画面での表記を変更できる
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