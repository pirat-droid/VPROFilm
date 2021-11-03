from django.urls import path
from .views import *

urlpatterns = [
    path('', FilmListView.as_view(), name='home'),
]