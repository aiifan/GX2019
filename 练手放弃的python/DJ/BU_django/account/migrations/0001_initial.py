# Generated by Django 2.1.1 on 2018-09-29 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('account_id', models.IntegerField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(blank=True, max_length=20, null=True)),
                ('account_pwd', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=10, null=True)),
                ('state_time', models.CharField(blank=True, max_length=20, null=True)),
                ('create_time', models.CharField(blank=True, max_length=20, null=True)),
                ('prev_time', models.CharField(blank=True, max_length=20, null=True)),
                ('prev_ip', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ball',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(blank=True, null=True)),
                ('time_length', models.CharField(blank=True, max_length=20, null=True)),
                ('month', models.CharField(blank=True, max_length=10, null=True)),
                ('pay_method', models.CharField(blank=True, max_length=10, null=True)),
                ('pay_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_length', models.CharField(blank=True, max_length=10, null=True)),
                ('pay_cost', models.FloatField(blank=True, null=True)),
                ('statue', models.CharField(blank=True, max_length=10, null=True)),
                ('create_time', models.CharField(blank=True, max_length=20, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Accounts')),
            ],
        ),
        migrations.CreateModel(
            name='DetailBall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_ip', models.CharField(blank=True, max_length=20, null=True)),
                ('login_time', models.CharField(blank=True, max_length=20, null=True)),
                ('leave_time', models.CharField(blank=True, max_length=20, null=True)),
                ('length_time', models.IntegerField(blank=True, null=True)),
                ('fee', models.FloatField(blank=True, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Postage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pg_name', models.CharField(blank=True, max_length=30, null=True)),
                ('pg_code', models.CharField(blank=True, max_length=20, null=True)),
                ('pg_type', models.CharField(blank=True, max_length=10, null=True)),
                ('base_length', models.IntegerField(blank=True, null=True)),
                ('base_cost', models.IntegerField(blank=True, null=True)),
                ('company_cost', models.CharField(blank=True, max_length=10, null=True)),
                ('create_time', models.CharField(blank=True, max_length=20, null=True)),
                ('use_time', models.CharField(blank=True, max_length=20, null=True)),
                ('pg_explain', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('ident', models.CharField(blank=True, max_length=30, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('birth', models.CharField(blank=True, max_length=20, null=True)),
                ('Email', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('occupation', models.CharField(blank=True, max_length=20, null=True)),
                ('addr', models.CharField(blank=True, max_length=30, null=True)),
                ('youbian', models.CharField(blank=True, max_length=10, null=True)),
                ('qq', models.CharField(blank=True, max_length=20, null=True)),
                ('osname', models.CharField(blank=True, max_length=20, null=True)),
                ('ospwd', models.CharField(blank=True, max_length=20, null=True)),
                ('osip', models.CharField(blank=True, max_length=20, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Accounts')),
            ],
        ),
        migrations.AddField(
            model_name='business',
            name='postage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Postage'),
        ),
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
        migrations.AddField(
            model_name='ball',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
    ]
