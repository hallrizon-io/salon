# Generated by Django 3.1 on 2020-08-31 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20200831_1354'),
        ('reception', '0006_auto_20200814_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reception',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receptions', to='service.service'),
        ),
    ]