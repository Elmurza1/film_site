from datetime import date

from django.db import models
from django.forms import SlugField
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    """ модель для котегорий фильма"""
    name = models.CharField(max_length=111)
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'



class Actor(models.Model):
    """моделька для актеров и режиссеров"""
    name = models.CharField(max_length=111)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})


    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """ модель для жанров фильмов """
    title = models.CharField(max_length=21)
    url = models.SlugField(max_length=111, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Movi(models.Model):
    """ моделька для фильма """
    director = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_directors")
    actor = models.ManyToManyField(Actor, verbose_name='актер', related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE, null=True
    )

    title = models.CharField(max_length=111)
    tagline = models.CharField(max_length=200, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to='movies/')
    year = models.PositiveSmallIntegerField("Дата выхода", default=0)
    country = models.CharField(max_length=45)
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField(default=0, help_text="указывать сумму в долларах")
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    url = models.SlugField(max_length=30, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"



class MoviShots(models.Model):
    """ кадры из фильма """
    movi = models.ForeignKey(Movi, on_delete=models.CASCADE)

    title = models.CharField(max_length=111)
    image = models.ImageField("Изображение", upload_to="movie_shots/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'кадр из фильма'
        verbose_name_plural = 'кадры из фильма'


class RatingStar(models.Model):
    """ модель для звезды рейтинга """
    star = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.star}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-star"]


class Rating(models.Model):
    """ модель для рейтинга """
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movi = models.ForeignKey(Movi, on_delete=models.CASCADE)
    ip = models.CharField(max_length=33)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """ модель для отзывов """
    from users.models import CustomUser
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movi, on_delete=models.CASCADE)
    parents = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    email = models.EmailField()
    name = models.CharField(max_length=111)
    text = models.TextField()


    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"