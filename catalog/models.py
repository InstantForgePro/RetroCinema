from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField()
    country = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    synopsis = models.TextField(blank=True)

    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    video_file = models.FileField(upload_to='movies/')  # MP4 o HLS master si quieres

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

    movie = models.ForeignKey(Movie, related_name='audio_tracks', on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    label = models.CharField(max_length=100, help_text="Ej: 'Doblaje original', 'Doblaje IA 2025'")
    is_ai_generated = models.BooleanField(default=False)
    audio_file = models.FileField(upload_to='audio_tracks/')

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

    movie = models.ForeignKey(Movie, related_name='ad_slots', on_delete=models.CASCADE)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    timestamp_seconds = models.PositiveIntegerField(default=0, help_text="Para mid-roll, segundo donde lanzar el anuncio")
    ad = models.ForeignKey(Ad, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.movie.title} - {self.position} - {self.ad.name}"
from django.db import models

# Create your models here.
