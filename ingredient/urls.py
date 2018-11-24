
from django.conf.urls import url

from .views import IngredientsApiView

urlpatterns = [
    url(r'^', IngredientsApiView.as_view()),

]
