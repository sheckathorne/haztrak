# Generated by Django 4.1.3 on 2022-11-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trak', '0009_alter_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='handler',
            name='site_type',
            field=models.CharField(choices=[('Tsdf', 'Tsdf'), ('Generator', 'Generator'), ('Transporter', 'Transporter'), ('Broker', 'Broker')], default='Generator', max_length=20),
            preserve_default=False,
        ),
    ]