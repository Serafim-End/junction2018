
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

    for meal_level, v in meal_level_map.items():

        meals = set()
        _recipes = sorted(v, key=lambda x: (x[1], x[0]))

        for diet_level in diet_suggestions.keys():
            approx = DIETS_CUSTOMIZATION[diet_level][meal_level]
            approx_high = approx * 1.4
            approx_low = approx * 0.6
            necessary_kcal = approx * DAYS

            for (recipe_id, weight) in _recipes:

                if recipe_id in meals:
                    continue

                try:
                    portions = int(recipes_map[recipe_id].get('Portions').get('Amount'))
                    kcal_portion = float(recipes_map[recipe_id].get('EnergyAmounts').get('KcalPerPortion'))
                except:
                    continue

                if approx_low <= kcal_portion <= approx_high:

                    # custom_ingridient = []
                    # ingridients = recipes_map[recipe_id].get('Ingredients')
                    # ing = ingridients[0]
                    # sub_ingridients = ing.get('SubSectionIngredients')
                    # for sub_ing in sub_ingridients:
                    #     for sub_sub_ing in sub_ing:
                    #         try:
                    #             custom_ingridient.append(sub_sub_ing)
                    #         except:
                    #             continue
                    # custom_ingridient = list(custom_ingridient)
                    # recipes_map[recipe_id]['products'] = get_products_list(custom_ingridient)

                    diet_suggestions[diet_level][meal_level].append(
                        recipes_map[recipe_id]
                    )

                    meals.add(recipe_id)
                    # necessary_kcal -= portions * kcal_portion
                    necessary_kcal -= kcal_portion
                    if necessary_kcal * (1 - 0.2 / DAYS) <= 0:
                        break

    return diet_suggestions
