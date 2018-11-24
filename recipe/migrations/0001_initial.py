# Generated by Django 2.1.3 on 2018-11-24 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('portions', models.PositiveIntegerField()),
                ('preparation_time', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=100)),
                ('img_url', models.URLField()),
                ('kcal_portion', models.FloatField()),
                ('kj_portion', models.FloatField()),
                ('fat_portion', models.FloatField()),
                ('protein_portion', models.FloatField()),
                ('carbohydrate_portion', models.FloatField()),
                ('instruction', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('k_url', models.URLField()),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredient.Ingredient')),
            ],
        ),
    ]
