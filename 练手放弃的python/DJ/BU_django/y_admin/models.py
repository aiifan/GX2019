from django.db import models

# Create your models here.
class Superadmin(models.Model):
    adminid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=40)
    role = models.CharField(max_length=300)
    customrole = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=300)
    ctime = models.CharField(max_length=100)


class Rolemanage(models.Model):
    roleid = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=30)
    power = models.CharField(max_length=300)
