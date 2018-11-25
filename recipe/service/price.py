import requests
import json

from django.conf import settings

ENDPOINT_SEARCH_PRODUCTS = "https://kesko.azure-api.net/v1/search/products"


def get_in_type_by_ean(ean):

    hs = {
        'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY,
        'Content-Type': 'application/json'
    }

    ds = {
        'filters': {'ean': str(ean)},
        'view': {'limit': 1, 'offset': 0 }}
    r = requests.post(ENDPOINT_SEARCH_PRODUCTS, headers=hs, data=json.dumps(ds))

    j = r.json()
    if j['totalHits'] > 0:
        product = j['results'][0]
        if 'ingredientType' in product:
            return product['ingredientType'], product['pictureUrls'][0]['original']
    return None, None


def get_ing_ids_by_name(name):

    hs = {
        'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY,
        'Content-Type': 'application/json'
    }
    ds = {
        'query': name
    }
    r = requests.post(ENDPOINT_SEARCH_PRODUCTS, headers=hs, data=json.dumps(ds))

    results = r.json()['results']
    res = []
    for r in results:
        if 'ingredientType' not in r:
            continue
        if r['ingredientType'] not in res:
            res.append(r['ingredientType'])
    return res


def products_search(ds):

    hs = {
        'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY,
        'Content-Type': 'application/json'
    }
    r = requests.post(ENDPOINT_SEARCH_PRODUCTS, headers=hs, data=json.dumps(ds))
    return r.json()['results']


def get_product_for_store(store, ean):

    hs = {'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY}
    r = requests.get('https://kesko.azure-api.net/v4/stores/' + str(store) + '/products?ean=' + str(ean), headers=hs)
    return r.json()[str(ean)]


def get_stores():
    hs = {'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY}
    ds = {
        'filters': {
            'locationDistance':{
                'location': {
                    'lon': 60,
                    'lat': 24
                },
                'distance': 5000
            }
        }
    }
    r = requests.post(
        url='https://kesko.azure-api.net/v1/search/stores',
        headers=hs,
        json=ds
    )
    data = r.json()
    return [e.get('Id') for e in data.get('results')]


STORE = get_stores()
STORE[1] = STORE[61]

__i_type_to_ean = {}


def get_ean_by_type(i_type, offset=0):
    if i_type not in __i_type_to_ean:
        r = products_search({
            'filters': { 'ingredientType': [str(i_type)] },
            'view': { 'limit': 1, 'offset': offset } })
        if len(r) == 0:
            return None
        ean = r[0]['ean']
        __i_type_to_ean[i_type] = ean
    return __i_type_to_ean[i_type]


def get_store_by_ean(ean):
    hs = {'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY}
    r = requests.get('https://kesko.azure-api.net/v2/products?ean=' + str(ean), headers=hs).json()
    if len(r[0]['stores']) == 0:
        return None
    else:
        return r[0]['stores'][0]['id']


__ean_to_product = {}


def get_product(ean):
    if ean in __ean_to_product:
        return __ean_to_product[ean]

    # store = get_store_by_ean(ean)
    # if store is None:
    #     return None

    for s in STORE[:3]:
        product = get_product_for_store(s, ean)
        if product is not None:
            __ean_to_product[ean] = product
            return product

    store = get_store_by_ean(ean)
    if store is None:
        return None

    product = get_product_for_store(store, ean)
    if product is not None:
        __ean_to_product[ean] = product
        return product
    return None


def normalize_units(unit):
    u = unit.lower()
    m = 1 # multiplier
    if u == 'tl':
        m = 0.005
    elif u == 'rkl':
        m = 0.015
    elif u == 'l':
        m = 1.0
    elif u == 'kg':
        m = 1.0
    elif u == 'g':
        m = 0.001
    return m


def normalize_amount(amount):
    data = amount
    main = ""
    frac = ""
    if '-' in data:
        data = data.split('-')[-1]

    if ' ' in data:
        main, frac = data.split(' ')
    else:
        frac = data

    if len(main) > 0:
        main = int(main)
    else:
        main = 0

    if '/' in frac:
        q, r = frac.split('/')
        frac = float(q) / float(r)
    else:
        frac = float(frac)

    return main + frac


def get_products_list(ingridients):

    products = {}
    rem_products = {}

    def add_product(products, ean, count=1.0):
        if ean in products:
            products[ean]['count'] += count
        else:
            product = get_product(ean)
            if product is not None and 'price' in product:
                products[ean] = {
                    'count': count,
                    'item_price': product['price'],
                    'name': product['name']
                }

    for inc, ingridient in enumerate(ingridients):
        if 'Ean' in ingridient:
            ean = ingridient['Ean']
            add_product(products, ean)
        else:
            if 'IngredientType' not in ingridient:
                continue

            ean = get_ean_by_type(ingridient['IngredientType'])
            if ean is None:
                continue

            if get_product(ean) is None:
                continue
                # offset += 1
                # ean = get_ean_by_type(ingridient['IngredientType'], offset=offset)

            if 'AmountInfo' in ingridient:
                add_product(products, ean)
            else:
                # handle weight
                if ean not in rem_products:
                    rem_products[ean] = 0.0

                try:
                    unit_m = normalize_units(ingridient['Unit'])
                except Exception:
                    unit_m = 1.0

                try:
                    amount = normalize_amount(ingridient['Amount'])
                except Exception:
                    amount = 1

                quantity = unit_m * amount

                if rem_products[ean] > quantity:
                    rem_products[ean] -= quantity
                else:
                    product = get_product(ean)
                    p_unit_m = normalize_units(product['packageUnit'])
                    p_size = float(product['packageSize'])

                    if p_size < 0.001:
                        count = quantity / p_unit_m
                        add_product(products, ean, count)
                        continue

                    p_quantity = p_unit_m * float(product['packageSize'])

                    while quantity > 0:
                        add_product(products, ean)
                        rem_products[ean] += p_quantity

                        if quantity > rem_products[ean]:
                            quantity -= rem_products[ean]
                            rem_products[ean] = 0
                        else:
                            rem_products[ean] -= quantity
                            quantity = 0
    return products
