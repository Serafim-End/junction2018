
from django.conf import settings

import requests


def filter_negative_recipes(negative):

    data = None

    try:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY,
            'Content-Type': 'application/json'
        }

        r = requests.post(
            url='https://kesko.azure-api.net/v1/search/recipes',
            json={
                'filters': [
                    {
                        'name': 'ingredientType',
                        'value': [str(e) for e in negative],
                        'operator': 'not'
                    }
                ],
                'view': {
                    'offset': 1500
                }
            },
            headers=headers
        )

        data = r.json()

    except requests.ConnectionError:
        print('connection error during the parser')

    if not data:
        raise Exception('not data exception: {}'.format(data))

    return data
