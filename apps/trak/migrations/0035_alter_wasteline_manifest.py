# Generated by Django 4.0.4 on 2022-05-20 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trak', '0034_wasteline_manifest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteline',
            name='manifest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wastes', to='trak.manifest'),
        ),
    ]