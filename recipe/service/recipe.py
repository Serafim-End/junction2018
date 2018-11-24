
from .net import filter_negative_recipes


def filter_recipes(ingredient_type_ids):
    not_, plus_ = [], []
    for e in ingredient_type_ids:
        if e == -1:
            not_.append(e)
        else:
            plus_.append(e)

    recipes = filter_negative_recipes(not_)

    recipes_map = {}
    categories_map = {}
    for recipe in recipes.get('results'):
        recipe_id = recipe.get('Id')
        recipes_map[recipe_id] = recipe
        recipe['weight'] = 0

        ing_recipe_ids = set()
        ingredients = recipe.get('Ingredients')
        sub_section_ingredients = ingredients[0].get('SubSectionIngredients')
        for sub_section_ingredient in sub_section_ingredients:
            for sub_sub_section_ingredient in sub_section_ingredient:
                ing_recipe_ids.add(
                    sub_sub_section_ingredient.get('IngredientType')
                )

        for ing_type in plus_:
            if ing_type in ing_recipe_ids:
                recipe['weight'] += 1

        categories = recipe.get('Categories')
        if not categories:
            continue

        for cat in categories:
            cat_id = cat.get('SubId')
            if cat_id not in categories_map:
                categories_map[cat_id] = [(recipe_id, recipe['weight'])]
            else:
                categories_map[cat_id].append((recipe_id, recipe['weight']))

    return categories_map, recipes_map


# def get_recipes_data():
#
#     data = None
#
#     try:
#         headers = {
#             'Ocp-Apim-Subscription-Key': settings.K_MARKET_APIKEY,
#             'Content-Type': 'application/json'
#         }
#
#         r = requests.post(
#             url='https://kesko.azure-api.net/v1/search/recipes',
#             json={
#                 'view': {
#                     'offset': 1500
#                 }
#             },
#             headers=headers
#         )
#
#         return r.json()
#
#     except requests.ConnectionError:
#         print('connection error during the parser')
#
#     if not data:
#         raise Exception('not data exception: {}'.format(data))
#
#
# def get_all_recipes():
#
#     data = get_recipes_data()
#     for e in data.get('results'):
#
#         energy = e.get('EnergyAmounts')
#
#         if not isinstance(energy, dict):
#             continue
#
#         ingredients = e.get('Ingredients')
#         ingredients_internal_ids = []
#         for ing in ingredients:
#             sub_ings = ing.get('SubSectionIngredients')
#
#             for sub_ing_l in sub_ings:
#                 for sub_ing in sub_ing_l:
#
#                     ing_type_id = sub_ing.get('IngredientType')
#
#                     if ing_type_id:
#                         ingredient = Ingredient.objects.create(
#                             id=ing_type_id,
#                             name=sub_ing.get('Name')
#                         )
#                         ingredient.save()
#                         ingredients_internal_ids.append(ing_type_id)
#
#         try:
#             recipe = Recipe.objects.create(
#                 id=e.get('Id'),
#                 name=e.get('Name'),
#                 portions=e.get('Portions').get('Amount'),
#                 preparation_time=e.get('PreparationTime').get('Description'),
#                 category=','.join(
#                     [c.get('MainName') for c in e.get('Categories')]
#                 ),
#                 img_url=e.get('PictureUrls').get('Normal'),
#                 kcal_portion=float(energy.get('KcalPerPortion')),
#                 kj_portion=float(energy.get('KJPerPortion')),
#                 fat_portion=float(energy.get('FatPerPortion')),
#                 protein_portion=float(energy.get('ProteinPerPortion')),
#                 carbohydrate_portion=float(
#                     energy.get('CarbohydratePerPortion')
#                 ),
#
#                 instruction=e.get('Instructions'),
#                 description=e.get('Description'),
#                 k_url=e.get('Url'),
#                 ingredients=list(set(ingredients_internal_ids))
#             )
#
#             recipe.save()
#
#         except Exception as e:
#             print('... {}'.format(e))