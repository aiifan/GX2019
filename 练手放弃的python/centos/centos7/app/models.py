from django.db import models

# Create your models here.


class Servers(models.Model):
    server_ip = models.GenericIPAddressField("ip")
    server_port = models.IntegerField('PORT')
    server_user = models.CharField("user", max_length=100)
    server_pwd = models.CharField('password', max_length=256)

    class Meta:
        verbose_name = 'IP ADDR'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.server_ip
