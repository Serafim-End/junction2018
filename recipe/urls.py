
from django.conf.urls import url

from .views import RecommendRecipe

urlpatterns = [
    url(r'^recommend/', RecommendRecipe.as_view()),

]
