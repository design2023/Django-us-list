# Generated by Django 4.2.4 on 2023-08-05 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('nationality', models.CharField(max_length=200)),
                ('family_arabic', models.CharField(max_length=200)),
                ('family_english', models.CharField(max_length=200)),
                ('fullname_arabic', models.CharField(max_length=200)),
                ('fullname_english', models.CharField(max_length=200)),
                ('birth_date', models.DateField(max_length=200)),
                ('birth_place', models.CharField(max_length=200)),
                ('nick_name', models.CharField(max_length=200)),
                ('street', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('document_number', models.CharField(max_length=200)),
                ('issuer', models.CharField(max_length=200)),
                ('from_date', models.DateField(max_length=200)),
                ('to_date', models.DateField(max_length=200)),
                ('other_information', models.CharField(max_length=200)),
            ],
        ),
    ]
