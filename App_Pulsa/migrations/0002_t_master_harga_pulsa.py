# Generated by Django 2.1.2 on 2018-10-17 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Pulsa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_master_harga_pulsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harga_beli', models.IntegerField()),
                ('harga_jual', models.IntegerField()),
                ('periode_mulai', models.DateField()),
                ('periode_akhir', models.DateField()),
                ('created_by', models.CharField(max_length=30)),
                ('created_date', models.DateField()),
                ('updated_by', models.CharField(max_length=30)),
                ('update_date', models.DateField()),
                ('id_jenis_pulsa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Pulsa.t_master_jenis_pulsa')),
            ],
        ),
    ]
