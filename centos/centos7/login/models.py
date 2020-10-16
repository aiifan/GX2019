from django.db import models
# Create your models here.

class Stu(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    stu_name = models.CharField("学生姓名",max_length=100)
    stu_sex = models.CharField('性别',choices=gender,max_length=6, default='男')
    stu_password = models.CharField('密码',max_length=256,default='')
    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stu_name

class Cla(models.Model):
    cla_name = models.CharField('班级名称',max_length=100)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
    def __str__(self):
        self.cla_name

class Course(models.Model):
    course_name = models.CharField('课程名称',max_length=100)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_name


class Tea(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    tea_name = models.CharField('教师名称',max_length=100)
    tea_sex = models.CharField('性别',choices=gender, max_length=6,default='男')
    tea_tel = models.CharField('手机号',max_length=11)
    tes_password = models.CharField('密码',max_length=256, default='')

    class Meta:
        verbose_name = '老师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stu_name