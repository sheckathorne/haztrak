# Generated by Django 4.2.7 on 2023-11-09 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_alter_haztraksite_admin_rcrainfo_profile_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rcrasitepermissions',
            options={'ordering': ['site__epa_id'], 'verbose_name': 'RCRAInfo Site Permission'},
        ),
        migrations.AlterModelOptions(
            name='sitepermissions',
            options={'verbose_name': 'Haztrak Site Permissions'},
        ),
    ]
