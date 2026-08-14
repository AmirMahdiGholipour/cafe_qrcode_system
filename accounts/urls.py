from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CafeAddView


urlpatterns = [
    path('cafe/add/', CafeAddView.as_view(), name='cafe-add'),
]