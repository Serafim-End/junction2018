# Generated by Django 2.1.3 on 2018-11-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]