# Generated by Django 4.0.4 on 2022-05-20 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trak', '0029_rename_br_provided_wasteline_br_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteline',
            name='epa_waste',
            field=models.BooleanField(verbose_name='EPA waste'),
        ),
    ]