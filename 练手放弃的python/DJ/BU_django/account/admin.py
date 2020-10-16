from django.contrib import admin
from .models import Accounts, User, Postage, Ball, Business, DetailBall

# Register your models here.
admin.site.register(Accounts)
admin.site.register(User)
admin.site.register(Postage)
admin.site.register(Ball)
admin.site.register(Business)
admin.site.register(DetailBall)
