# Generated by Django 5.0 on 2023-12-19 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'currencies',
            },
        ),
    ]
