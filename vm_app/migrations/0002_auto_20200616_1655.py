# Generated by Django 3.0.5 on 2020-06-16 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('billing_address', models.CharField(max_length=50)),
                ('users', models.ManyToManyField(related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='module1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module1', to='vm_app.HomeModuleNames'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='module2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module2', to='vm_app.HomeModuleNames'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='module3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module3', to='vm_app.HomeModuleNames'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='module4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module4', to='vm_app.HomeModuleNames'),
        ),
        migrations.CreateModel(
            name='Client_user_permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vm_app.Client')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='selected_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET, to='vm_app.Client'),
        ),
    ]
