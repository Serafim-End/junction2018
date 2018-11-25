
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Recipe
from .serializers import RecipeSerializer
from .service.recipe import filter_recipes
from .service.diet import (
    create_diet, full_default_category_map
)


class RecommendRecipe(APIView):

    def post(self, request, format=None):
        """
        RecommendRecipe
        ---
        post:
            omit_serializer: true
            parameters_strategy:
            form: replace
        parameters:
            - name: preferences
              description: preferences of products
              required: true
              type: dict
            - name: diet
              type: int
              required: False

        responseMessages:
        - code: 200
          message: OK

        {
            IngredientType: 1 or -1
        }, ...

        """
        data = request.data

        preferences = data.get('preferences')
        diet = data.get('diet')

        categories_map, recipes_map = filter_recipes(preferences)
        diet_category_mapper = full_default_category_map(categories_map.keys())
        diet_suggestions = create_diet(
            diet_category_mapper=diet_category_mapper,
            categories_map=categories_map,
            recipes_map=recipes_map
        )
        return Response(
            diet_suggestions,
            status=status.HTTP_200_OK
        )


class RecipesViewSet(ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
