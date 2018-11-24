
from rest_framework.viewsets import ModelViewSet

from .serializers import IngredientSerializer
from .models import Ingredient


class IngredientsApiView(ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
