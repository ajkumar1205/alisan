# Generated by Django 5.1.3 on 2024-11-16 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_franchise_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='neighbours',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='neighbours', to='accounts.neighbours'),
            preserve_default=False,
        ),
    ]
