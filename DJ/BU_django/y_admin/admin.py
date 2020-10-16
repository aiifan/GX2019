from django.contrib import admin
from .models import *

# Register your models here.
admin.site.set_header = 'Y_admin'
admin.site.set_title = 'Y_admin'
admin.site.register(Superadmin)
admin.site.register(Rolemanage)