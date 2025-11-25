from django.shortcuts import render, get_object_or_404
from .models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, 'catalog/home.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    audio_tracks = movie.audio_tracks.all()
    ad_slots = movie.ad_slots.select_related('ad').all()

    context = {
        'movie': movie,
        'audio_tracks': audio_tracks,
        'ad_slots': ad_slots,
    }
    return render(request, 'catalog/movie_detail.html', context)
