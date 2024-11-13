# Generated by Django 5.1.3 on 2024-11-12 20:19

import core.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_franchise_created_by_and_more'),
        ('core', '0003_lead_phone_number_alter_lead_assigned_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_amount', models.FloatField()),
                ('discount', models.FloatField()),
                ('discount_amount', models.FloatField()),
                ('gst', models.FloatField()),
                ('gst_amount', models.FloatField()),
                ('status', models.CharField(choices=[('approval', 'Approval Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='approval', max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='quotations/', validators=[core.models.validate_pdf])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_created_by', to='accounts.employee')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lead')),
                ('products', models.ManyToManyField(related_name='quotations', to='core.product')),
            ],
        ),
    ]