from django.contrib import admin
from .models import Movie, AudioTrack, Ad, AdSlot


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "country", "genre", "is_public_domain", "created_at")
    search_fields = ("title", "original_title")
    list_filter = ("year", "country", "genre", "is_public_domain")


@admin.register(AudioTrack)
class AudioTrackAdmin(admin.ModelAdmin):
    list_display = ("movie", "language", "label", "is_ai_generated")
    list_filter = ("language", "is_ai_generated")
    search_fields = ("movie__title", "label")


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = ("movie", "position", "timestamp_seconds", "ad")
    list_filter = ("position",)
