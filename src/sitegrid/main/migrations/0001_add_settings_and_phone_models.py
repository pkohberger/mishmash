# Generated by Django 2.0.4 on 2018-05-11 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=80, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e164_number', models.CharField(max_length=32, unique=True)),
                ('number_type', models.CharField(blank=True, choices=[('fax', 'Fax Number'), ('home', 'Home Number'), ('work', 'Work Number'), ('cell', 'Mobile Number')], max_length=8, null=True)),
                ('ext', models.CharField(blank=True, max_length=8, null=True)),
            ],
        ),
    ]
