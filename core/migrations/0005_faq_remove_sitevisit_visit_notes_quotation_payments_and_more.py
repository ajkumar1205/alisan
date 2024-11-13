# Generated by Django 5.1.3 on 2024-11-13 04:41

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_quotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sitevisit',
            name='visit_notes',
        ),
        migrations.AddField(
            model_name='quotation',
            name='payments',
            field=models.ManyToManyField(related_name='payments', to='core.payment'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='products',
            field=models.ManyToManyField(related_name='products', to='core.product'),
        ),
        migrations.AlterField(
            model_name='sitevisit',
            name='visit_date',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='SitePicAndNotes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pic', models.ImageField(upload_to='site_pics/')),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('site_visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sitevisit')),
            ],
        ),
        migrations.AddField(
            model_name='sitevisit',
            name='site_pic_notes',
            field=models.ManyToManyField(blank=True, related_name='site_pic_notes', to='core.sitepicandnotes'),
        ),
    ]
