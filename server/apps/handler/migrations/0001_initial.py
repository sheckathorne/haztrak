# Generated by Django 4.2.10 on 2024-02-17 01:25

import django.db.models.deletion
from django.db import migrations, models

import apps.handler.models.contact_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rcrasite", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Handler",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
            options={
                "ordering": ["rcra_site"],
            },
        ),
        migrations.CreateModel(
            name="ManifestPhone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", apps.handler.models.contact_models.ManifestPhoneNumber(max_length=12)),
                ("extension", models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                "ordering": ["number"],
            },
        ),
        migrations.CreateModel(
            name="PaperSignature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("printed_name", models.CharField(max_length=255)),
                ("sign_date", models.DateTimeField()),
            ],
            options={
                "ordering": ["pk"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Transporter",
            fields=[
                ("handler_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="handler.handler")),
                ("order", models.PositiveIntegerField()),
            ],
            options={
                "ordering": ["manifest__mtn"],
            },
            bases=("handler.handler",),
        ),
        migrations.CreateModel(
            name="Signer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rcra_user_id", models.CharField(blank=True, max_length=100, null=True)),
                ("first_name", models.CharField(blank=True, max_length=38, null=True)),
                ("middle_initial", models.CharField(blank=True, max_length=1, null=True)),
                ("last_name", models.CharField(blank=True, max_length=38, null=True)),
                ("email", models.CharField(blank=True, max_length=38, null=True)),
                ("company_name", models.CharField(blank=True, max_length=80, null=True)),
                ("contact_type", models.CharField(blank=True, choices=[("email", "Email"), ("voice", "Voice"), ("text", "Text")], max_length=5, null=True)),
                ("signer_role", models.CharField(choices=[("Industry", "Industry"), ("PPC", "Ppc"), ("EPA", "Epa"), ("State", "State")], max_length=10, null=True)),
                ("phone", models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="handler.manifestphone")),
            ],
            options={
                "ordering": ["first_name"],
            },
        ),
        migrations.AddField(
            model_name="handler",
            name="emergency_phone",
            field=models.ForeignKey(blank=True, help_text="Emergency phone number for the hazardous waste rcra_site", null=True, on_delete=django.db.models.deletion.PROTECT, to="handler.manifestphone"),
        ),
        migrations.AddField(
            model_name="handler",
            name="paper_signature",
            field=models.OneToOneField(blank=True, help_text="The signature associated with hazardous waste custody exchange", null=True, on_delete=django.db.models.deletion.CASCADE, to="handler.papersignature"),
        ),
        migrations.AddField(
            model_name="handler",
            name="rcra_site",
            field=models.ForeignKey(help_text="Hazardous waste rcra_site associated with the manifest", on_delete=django.db.models.deletion.CASCADE, to="rcrasite.rcrasite"),
        ),
        migrations.CreateModel(
            name="ESignature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sign_date", models.DateTimeField(blank=True, null=True)),
                ("cromerr_activity_id", models.CharField(blank=True, max_length=100, null=True)),
                ("cromerr_document_id", models.CharField(blank=True, max_length=100, null=True)),
                ("on_behalf", models.BooleanField(blank=True, default=False, null=True)),
                ("manifest_handler", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="e_signatures", to="handler.handler")),
                ("signer", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="handler.signer")),
            ],
            options={
                "verbose_name": "e-Signature",
                "ordering": ["sign_date"],
            },
        ),
    ]
