from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(UserProfileModel)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'point', 'date_update', 'date_create']
    list_filter = ['country', ]
    search_fields = ['user', ]


@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_tag', 'country', 'published', 'date_update', 'date_create']
    search_fields = ['name', ]
    list_filter = ['career', 'country']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['published', ]
    readonly_fields = ['photo_tag']



@admin.register(FilmModel)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['name', 'poster', 'country', 'published', 'date_update', 'date_create']
    search_fields = ['name', 'director', 'scenario', 'producer', 'composer', 'actor', 'genre', 'country']
    list_filter = ['genre', 'country']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['published', ]


@admin.register(ImageFilmModel)
class FilmImageFilmAdmin(admin.ModelAdmin):
    list_display = ['film', 'image', 'date_update', 'date_create']
    search_fields = ['film', ]
    # readonly_fields = ['preview']

    # def preview(self, obj):
    #     return mark_safe(f'<img src="{obj.image.url}">')


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'film', 'published', 'rating', 'date_update', 'date_create']
    search_fields = ['author', 'film']
    list_filter = ['published', ]
    list_editable = ['published', ]


@admin.register(TrailerModel)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ['film', 'url']
    search_fields = ['film', ]


@admin.register(GenreModel)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre', 'slug']
    search_fields = ['genre', ]
    prepopulated_fields = {'slug': ('genre',)}


@admin.register(CountryModel)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country', 'slug']
    search_fields = ['country', ]
    prepopulated_fields = {'slug': ('country',)}


@admin.register(CareerModel)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['career', 'slug']
    search_fields = ['career', ]
    prepopulated_fields = {'slug': ('career',)}