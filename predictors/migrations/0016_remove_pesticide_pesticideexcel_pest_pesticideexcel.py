# Generated by Django 4.1 on 2024-06-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictors', '0015_alter_pest_pestinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesticide',
            name='pesticideExcel',
        ),
        migrations.AddField(
            model_name='pest',
            name='pesticideExcel',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
