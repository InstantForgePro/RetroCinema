from django.db import models
from django.utils.text import slugify


# --------- Helpers de rutas ---------

def movie_slug(instance):
    """
    Usa slug si lo tienes, si no, el título slugificado.
    Así no revienta aunque aún no hayas añadido el campo slug.
    """
    if hasattr(instance, "slug") and instance.slug:
        return instance.slug
    return slugify(instance.title)


def movie_poster_path(instance, filename):
    # media/movies/<pelicula>/poster/archivo.jpg
    slug = movie_slug(instance)
    return f"movies/{slug}/poster/{filename}"


def movie_video_path(instance, filename):
    # media/movies/<pelicula>/video/archivo.mp4
    slug = movie_slug(instance)
    return f"movies/{slug}/video/{filename}"


def audio_track_path(instance, filename):
    # media/movies/<pelicula>/audio/archivo.wav
    slug = movie_slug(instance.movie)
    return f"movies/{slug}/audio/{filename}"


# --------- Modelos ---------


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField()
    country = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    synopsis = models.TextField(blank=True)

    # Antes: upload_to='posters/' y 'movies/'
    poster = models.ImageField(
        upload_to=movie_poster_path,
        blank=True,
        null=True
    )
    video_file = models.FileField(
        upload_to=movie_video_path
    )  # MP4 o lo que quieras

    is_public_domain = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"


class AudioTrack(models.Model):
    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('ca', 'Catalán'),
        # añade lo que quieras
    ]

    movie = models.ForeignKey(
        Movie,
        related_name='audio_tracks',
        on_delete=models.CASCADE
    )
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    label = models.CharField(
        max_length=100,
        help_text="Ej: 'Doblaje original', 'Doblaje IA 2025'"
    )
    is_ai_generated = models.BooleanField(default=False)

    # Antes: upload_to='audio_tracks/'
    audio_file = models.FileField(upload_to=audio_track_path)

    # Para marcar cuál es la pista por defecto de esa peli / idioma
    is_default = models.BooleanField(default=False)

    class Meta:
        # Si quieres permitir varias pistas en el mismo idioma
        # (original + IA), mejor que la unicidad sea por label también.
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'language', 'label'],
                name='unique_label_per_movie_language'
            )
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.label}"


class Ad(models.Model):
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='ads/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AdSlot(models.Model):
    POSITION_CHOICES = [
        ('pre', 'Pre-roll'),
        ('mid', 'Mid-roll'),
    ]

    movie = models.ForeignKey(
        Movie,
        related_name='ad_slots',
        on_delete=models.CASCADE
    )
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    timestamp_seconds = models.PositiveIntegerField(
        default=0,
        help_text="Para mid-roll, segundo donde lanzar el anuncio"
    )
    ad = models.ForeignKey(Ad, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.movie.title} - {self.position} - {self.ad.name}"
