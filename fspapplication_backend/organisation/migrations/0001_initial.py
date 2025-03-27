# Generated by Django 5.1.7 on 2025-03-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company', verbose_name='Company Logo')),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 1')),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal/Zip Code')),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Contact Email')),
                ('website', models.URLField(blank=True, null=True)),
                ('tax_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tax Number')),
                ('abn_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Business Registration Number')),
                ('primary_color', models.CharField(default='#3B82F6', max_length=7, verbose_name='Primary Brand Color')),
                ('secondary_color', models.CharField(default='#1E40AF', max_length=7, verbose_name='Secondary Brand Color')),
                ('established_date', models.DateField(blank=True, null=True, verbose_name='Established Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Company',
            },
        ),
    ]
