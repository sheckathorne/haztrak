# Generated by Django 4.0.4 on 2022-05-20 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trak', '0030_alter_wasteline_epa_waste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteline',
            name='discrepancy_info',
            field=models.JSONField(blank=True, null=True, verbose_name='Discrepancy-Residue information'),
        ),
    ]