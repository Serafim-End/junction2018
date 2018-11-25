
from ..settings import DIETS_CUSTOMIZATION, DAYS
from .price import get_products_list


def default_category_map():
    return {
        0: [110, 33, 39],
        1: [115, 110, 33, 39],
        2: [17, 27],
        3: [21, 23, 20, 24, 22, 32, 31, 29, 30, 116, 117, 111, 114, 113],
        4: [72, 28, 31, 20, 116, 117, 111, 114, 113]
    }


def full_default_category_map(category_keys):
    return {i: category_keys for i in range(5)}


def create_diet(diet_category_mapper, categories_map, recipes_map):

    diet_suggestions = {
        k: {
            kk: [] for kk, vv in v.items()
        } for k, v in DIETS_CUSTOMIZATION.items()
    }

    meal_level_map = {i: [] for i in range(len(diet_category_mapper))}
    for meal_level, meal_categories in diet_category_mapper.items():

        for category_id in meal_categories:
            category_id = str(category_id)
            if category_id in categories_map:
                meal_level_map[meal_level] += categories_map[category_id]

    for diet_level in diet_suggestions.keys():
        custom_ingredient_new = []

        meals = set()
        for meal_level, v in meal_level_map.items():

            _recipes = sorted(v, key=lambda x: (x[1], x[0]))
            approx = DIETS_CUSTOMIZATION[diet_level][meal_level]
            approx_high = approx * 1.6
            approx_low = approx * 0.4

            for (recipe_id, weight) in _recipes:

                if recipe_id in meals:
                    continue

                try:
                    portions = int(recipes_map[recipe_id].get('Portions').get('Amount'))
                    kcal_portion = float(recipes_map[recipe_id].get('EnergyAmounts').get('KcalPerPortion'))
                except:
                    continue

                if approx_low <= kcal_portion <= approx_high:

                    custom_ingridient = []
                    ingridients = recipes_map[recipe_id].get('Ingredients')
                    ing = ingridients[0]
                    sub_ingridients = ing.get('SubSectionIngredients')
                    for sub_ing in sub_ingridients:
                        for sub_sub_ing in sub_ing:
                            try:
                                custom_ingridient.append(sub_sub_ing)
                            except:
                                continue
                    custom_ingridient = list(custom_ingridient)

                    e = recipes_map[recipe_id]
                    energy = e.get('EnergyAmounts')

                    new_recipe = {
                        'name': e.get('Name'),
                        'portions': e.get('Portions').get('Amount'),
                        'preparation_time': e.get('PreparationTime').get('Description'),
                        'category': ', '.join(
                            [c.get('MainName') for c in e.get('Categories')]
                        ),
                        'img_url': [
                            ee.get('Normal') for ee in e.get('PictureUrls')
                        ],
                        'kcal_portion': float(kcal_portion),
                        'kj_portion': float(energy.get('KJPerPortion')),
                        'fat_portion': float(energy.get('FatPerPortion')),
                        'protein_portion': float(
                            energy.get('ProteinPerPortion')
                        ),
                        'carbohydrate_portion': float(
                            energy.get('CarbohydratePerPortion')
                        ),
                        'instruction': e.get('Instructions'),
                        'description': e.get('Description'),
                        'k_url': e.get('Url'),
                        'ingredients': ', '.join(
                            [ee.get('Name') for ee in custom_ingridient]
                        )
                    }

                    custom_ingredient_new += custom_ingridient
                    diet_suggestions[diet_level][meal_level].append(
                        new_recipe
                    )

                    meals.add(recipe_id)
                    if len(diet_suggestions[diet_level][meal_level]) == DAYS:
                        break

            diet_suggestions[diet_level]['products'] = get_products_list(
                custom_ingredient_new
            )

    return diet_suggestions


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
