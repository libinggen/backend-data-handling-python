# Generated by Django 3.2.5 on 2023-12-21 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0003_auto_20231221_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]