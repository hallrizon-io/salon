# Generated by Django 3.0.8 on 2020-08-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20200807_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktypes',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]
