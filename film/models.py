from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.urls import reverse
from django.utils.safestring import mark_safe
from unidecode import unidecode


class UserProfileModel(models.Model):
    """Модель профиля пользователя"""
    GENDER_CHOICES = [
        ('man', 'мужчина'),
        ('woman', 'женщина'),
        ('other', 'другое')
    ]
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=5)
    birthday = models.DateField(null=True,
                                blank=True,
                                verbose_name='День рождение')
    country = models.ForeignKey('CountryModel',
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True,
                                verbose_name='Страна')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Время изменения')
    published = models.BooleanField(default=True,
                                    verbose_name='Опубликован')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d',
                               verbose_name='Аватар')
    point = models.IntegerField(default=0,
                                verbose_name='Очки пользователя')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['date_create', ]

    def __str__(self):
        return self.user


class PersonModel(models.Model):
    """Модель персона обобщает в себе актеров, режиссеров, сценаристов и т.д."""
    name = models.CharField(max_length=150,
                            verbose_name='ФИО')
    biography = models.TextField(max_length=2000,
                                 verbose_name='Биография')
    birthday = models.DateField(verbose_name='День рождение')
    death_day = models.DateField(null=True,
                                 blank=True,
                                 verbose_name='День смерти')
    career = models.ManyToManyField('CareerModel',
                                    blank=False,
                                    verbose_name='Карьера')
    country = models.ForeignKey('CountryModel',
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True,
                                verbose_name='Страна')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Время изменения')
    published = models.BooleanField(default=True,
                                    verbose_name='Опубликован')
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='URL')
    photo = models.ImageField(upload_to='person/%Y/%m/%d',
                              verbose_name='Фото')

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
        ordering = ['name', 'date_create']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_person', args={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def photo_tag(self):
        return mark_safe('<img src="%s" style="max-height: 50px;">' % self.photo.url)

    photo_tag.short_description = 'Фото'


class FilmModel(models.Model):
    """Модель фильмов"""
    name = models.CharField(max_length=100,
                            verbose_name='Название фильма')
    world_premiere = models.DateField(null=True,
                                      verbose_name='Премьера в мире')
    russian_premiere = models.DateField(null=True,
                                        verbose_name='Премьера в России')
    budget = models.IntegerField(verbose_name='Бюджет')
    poster = models.ImageField(upload_to='poster/%Y/%m/%d',
                               verbose_name='Постер')
    director = models.ManyToManyField(PersonModel,
                                      verbose_name='Режиссер',
                                      related_name='director_film')
    scenario = models.ManyToManyField(PersonModel,
                                      verbose_name='Сценарист',
                                      related_name='scenario_film')
    producer = models.ManyToManyField(PersonModel,
                                      verbose_name='Продюсер',
                                      related_name='producer_film')
    composer = models.ManyToManyField(PersonModel,
                                      verbose_name='Композитор',
                                      related_name='composer_film')
    actor = models.ManyToManyField(PersonModel,
                                   verbose_name='Актер',
                                   related_name='actor_film')
    genre = models.ManyToManyField('GenreModel',
                                   verbose_name='Жанры')
    country = models.ForeignKey('CountryModel',
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True,
                                verbose_name='Страна')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Время изменения')
    published = models.BooleanField(default=True,
                                    verbose_name='Опубликован')
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='URL')
    rating = models.FloatField(verbose_name='Рейтинг фильма',
                               null=True,
                               blank=True)
    views = models.IntegerField(verbose_name='Количество просмотров',
                                null=True,
                                blank=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['name', 'date_create']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('film_detail', args={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def poster_tag(self):
        return mark_safe('<img src="%s" style="max-height: 50 px">' % self.poster.url)

    poster_tag.short_description = 'Постер'


class ImageFilmModel(models.Model):
    """Модель кадров из фильмов"""
    film = models.ForeignKey(FilmModel,
                             on_delete=models.CASCADE,
                             verbose_name='Фильм')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Время изменения')
    image = models.ImageField(null=True,
                              upload_to='film/%Y/%m/%d')

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'
        ordering = ['date_create', ]

    def __str__(self):
        return self.film


class CommentModel(models.Model):
    """Модель комментариев пользователей"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор поста')
    film = models.ForeignKey(FilmModel,
                             on_delete=models.CASCADE,
                             verbose_name='Комментируемый фильм')
    text = models.TextField(max_length=500,
                            verbose_name='Комментарий')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Время изменения')
    published = models.BooleanField(default=True,
                                    verbose_name='Опубликован')
    rating = models.FloatField(verbose_name='Рейтинг комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date_create', ]

    def __str__(self):
        return self.film


class TrailerModel(models.Model):
    """Модель трейлеров фильмов, хранит в себе url адреса с youtube"""
    film = models.ForeignKey(FilmModel,
                             on_delete=models.PROTECT,
                             verbose_name='Фильм')
    url = models.CharField(max_length=250,
                           verbose_name='Ссылка на трейлер')

    class Meta:
        verbose_name = 'Трейлер'
        verbose_name_plural = 'Трейлеры'
        ordering = ['film', ]

    def __str__(self):
        return self.film


class GenreModel(models.Model):
    """Модель жанров фильмов"""
    genre = models.CharField(max_length=50,
                             verbose_name='Жанр')
    slug = models.SlugField(unique=True,
                            db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['genre', ]

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('genre_detail', args={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.genre))
        return super().save(*args, **kwargs)


class CountryModel(models.Model):
    """Модель стран"""
    country = models.CharField(max_length=50,
                               verbose_name='Страна')
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='URL')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['country', ]

    def __str__(self):
        return self.country

    def get_absolute_url(self):
        return reverse('country_detail', args={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.country))
        return super().save(*args, **kwargs)


class CareerModel(models.Model):
    """Модель название карьеры например: режисер, актер и т.д."""
    career = models.CharField(max_length=50,
                              verbose_name='Карьера')
    slug = models.SlugField(unique=True,
                            db_index=True)

    class Meta:
        verbose_name = 'Карьера'
        verbose_name_plural = 'Карьеры'
        ordering = ['career', ]

    def __str__(self):
        return self.career

    def get_absolute_url(self):
        return reverse('career_detail', args={'url': self.career})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.career))
        return super().save(*args, **kwargs)
