from django.contrib import admin
from .models import Movie, AudioTrack, Ad, AdSlot

class AudioTrackInline(admin.TabularInline):
    model = AudioTrack
    extra = 1


class AdSlotInline(admin.TabularInline):
    model = AdSlot
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'country', 'is_public_domain')
    list_filter = ('year', 'country', 'is_public_domain')
    search_fields = ('title', 'original_title')
    inlines = [AudioTrackInline, AdSlotInline]


@admin.register(AudioTrack)
class AudioTrackAdmin(admin.ModelAdmin):
    list_display = ('movie', 'language', 'label', 'is_ai_generated')
    list_filter = ('language', 'is_ai_generated')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = ('movie', 'position', 'timestamp_seconds', 'ad')
    list_filter = ('position',)
