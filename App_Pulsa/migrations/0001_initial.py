# Generated by Django 2.1.2 on 2018-10-14 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='t_master_jenis_pulsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_voucher', models.CharField(max_length=30)),
                ('kode_voucher', models.CharField(max_length=30)),
                ('tipe_voucher', models.CharField(max_length=30)),
                ('created_by', models.CharField(max_length=30)),
                ('created_date', models.DateField()),
                ('updated_by', models.CharField(max_length=30)),
                ('update_date', models.DateField()),
            ],
        ),
    ]
