# Generated by Django 4.1 on 2024-05-31 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("predictors", "0008_rename_percentage_riskforecast_percentages_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="riskforecast",
            name="pest",
        ),
        migrations.AlterField(
            model_name="riskforecast",
            name="percentages",
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="riskforecast",
            name="riskLevels",
            field=models.JSONField(),
        ),
    ]
