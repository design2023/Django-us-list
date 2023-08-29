# Generated by Django 4.2.4 on 2023-08-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('us_list', '0002_alter_user_from_date_alter_user_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('account_id', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='excels/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]