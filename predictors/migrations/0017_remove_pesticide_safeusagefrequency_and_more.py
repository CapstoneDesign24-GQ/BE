# Generated by Django 4.1 on 2024-06-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictors', '0016_remove_pesticide_pesticideexcel_pest_pesticideexcel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesticide',
            name='safeUsageFrequency',
        ),
        migrations.RemoveField(
            model_name='pesticide',
            name='safeUsagePeriod',
        ),
        migrations.AddField(
            model_name='croppesticide',
            name='safeUsageFrequency',
            field=models.CharField(default='몇회', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='croppesticide',
            name='safeUsagePeriod',
            field=models.CharField(default='후', max_length=100),
            preserve_default=False,
        ),
    ]