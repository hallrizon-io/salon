# Generated by Django 3.0.8 on 2020-08-07 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master', '0002_auto_20200801_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Work Type',
                'verbose_name_plural': 'Work Types',
            },
        ),
        migrations.RemoveField(
            model_name='master',
            name='age',
        ),
        migrations.RemoveField(
            model_name='master',
            name='name',
        ),
        migrations.RemoveField(
            model_name='master',
            name='surname',
        ),
        migrations.AddField(
            model_name='master',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='master',
            name='work_types',
            field=models.ManyToManyField(to='master.WorkTypes'),
        ),
    ]
