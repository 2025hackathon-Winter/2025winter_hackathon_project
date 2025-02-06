from django.db import models

# Create your models here.
class RemindModel(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

class users(models.Model):
    uid = models.CharField(max_length=36)
    mailaddress =models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    default_term = models.PositiveSmallIntegerField()

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