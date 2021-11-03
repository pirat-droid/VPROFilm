from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class FilmListView(ListView):
    model = FilmModel
    template_name = 'film/home.html'
    context_object_name = 'films'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = GenreModel.objects.all()
        context['title'] = 'VIP Film'
        return context


class FilmDetailView(DetailView):
    model = FilmModel
    context_object_name = 'film'
    slug_url_kwarg = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'VIP Film %s'
        return context