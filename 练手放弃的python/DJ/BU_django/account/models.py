from django.db import models

# Create your models here.

class Accounts(models.Model):
    '''
        一个人有一个账务账号，账务账号信息表
    '''
    account_id = models.IntegerField(primary_key=True)
    account_name = models.CharField(max_length=20, null=True, blank=True)  # 账务账号名
    account_pwd = models.CharField(max_length=20, null=True, blank=True)    # 账务账号密码
    state = models.CharField(max_length=10, null=True, blank=True)   # 账号状态
    state_time = models.CharField(max_length=20, null=True, blank=True)  # 账号状态转变时间
    create_time = models.CharField(max_length=20, null=True, blank=True) # 账号创建时间
    prev_time = models.CharField(max_length=20, null=True, blank=True)
    prev_ip = models.CharField(max_length=20, null=True, blank=True)


class User(models.Model):
    '''
        用户基本信息表
    '''
    nickname = models.CharField(max_length=20, null=True, blank=True)  # 用户名
    ident = models.CharField(max_length=30, null=True, blank=True)  # 身份证号
    tel = models.CharField(max_length=20, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    Email = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    occupation = models.CharField(max_length=20, null=True, blank=True) # 职业
    addr = models.CharField(max_length=30, null=True, blank=True)
    youbian = models.CharField(max_length=10, null=True, blank=True)
    qq = models.CharField(max_length=20, null=True, blank=True)
    osname = models.CharField(max_length=20, null=True, blank=True)  # os账户名
    ospwd  =models.CharField(max_length=20, null=True, blank=True)
    osip = models.CharField(max_length=20, null=True, blank=True)
    account = models.ForeignKey(Accounts, models.CASCADE)


class Postage(models.Model):
    '''
        资费管理
    '''
    pg_name = models.CharField(max_length=30, null=True, blank=True)
    pg_code = models.CharField(max_length=20, null=True, blank=True)
    pg_type = models.CharField(max_length=10, null=True, blank=True)
    base_length = models.IntegerField(null=True, blank=True)
    base_cost = models.IntegerField(null=True, blank=True)
    company_cost = models.CharField(max_length=10, null=True, blank=True)
    create_time = models.CharField(max_length=20, null=True, blank=True)
    use_time = models.CharField(max_length=20, null=True, blank=True)
    pg_explain = models.CharField(max_length=100, null=True, blank=True)


class Business(models.Model):
    '''
        业务管理
    '''
    time_length = models.CharField(max_length=10, null=True, blank=True)
    pay_cost = models.FloatField(null=True, blank=True)
    statue = models.CharField(max_length=10, null=True, blank=True)
    create_time = models.CharField(max_length=20, null=True, blank=True)
    postage = models.ForeignKey(Postage, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    account = models.ForeignKey(Accounts, models.CASCADE)


class Ball(models.Model):
    '''
        账单
        用户所有业务花费相加的总值，每个用户都拥有一个总的账单
    '''
    cost = models.FloatField(null=True, blank=True)
    time_length = models.CharField(max_length=20, null=True, blank=True)
    month = models.CharField(max_length=10, null=True, blank=True)
    pay_method = models.CharField(max_length=10, null=True, blank=True)
    pay_code = models.CharField(max_length=10, null=True, blank=True)
    user = models.ForeignKey(User, models.CASCADE)

class DetailBall(models.Model):
    '''
    每个业务都会产生花费，每次花费产生的小的账单，
    一个业务会有很多小的账单详情
    '''
    login_ip = models.CharField(max_length=20, null=True, blank=True)
    login_time = models.CharField(max_length=20, null=True, blank=True)
    leave_time = models.CharField(max_length=20, null=True, blank=True)
    length_time = models.IntegerField(null=True, blank=True)
    fee = models.FloatField(null=True, blank=True)
    business = models.ForeignKey(Business, models.CASCADE)


