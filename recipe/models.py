from django.db import models

from ingredient.models import Ingredient
# Create your models here.


class Recipe(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    portions = models.PositiveIntegerField()
    preparation_time = models.CharField(max_length=30)
    category = models.CharField(max_length=100)
    img_url = models.URLField()

    kcal_portion = models.FloatField()
    kj_portion = models.FloatField()
    fat_portion = models.FloatField()
    protein_portion = models.FloatField()
    carbohydrate_portion = models.FloatField()

    instruction = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    k_url = models.URLField()

    # price = models.CharField(max_length=10)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)



