
import json

from .models import Ingredient


def parse(filename):

    with open(filename, 'r') as rf:
        data = json.load(rf)

    if not data:
        raise Exception('there are no data')

    for e in data:
        ing = Ingredient.objects.create(
            id=e['id'],
            name=e['name']
        )

        ing.save()
