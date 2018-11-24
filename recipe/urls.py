
from django.conf.urls import url

from .views import SubCategoryApiView

urlpatterns = [
    url(r'^sub/', SubCategoryApiView.as_view()),
]
