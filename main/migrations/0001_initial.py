# Generated by Django 3.0.3 on 2020-06-26 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departmens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('department_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('status', models.BooleanField()),
                ('is_employee', models.BooleanField()),
                ('departmen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Departmens')),
            ],
        ),
    ]
