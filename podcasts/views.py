from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Podcast, Saved_podcasts
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def podcast_list(request):
    podcasts = Podcast.objects.all().order_by('-date_published', 'title')
    context = {'podcasts':podcasts}

    return render(request, 'podcasts/podcast_list.html', context)

def podcast_detail(request, pk):
    podcast = get_object_or_404(Podcast, id = pk)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = Saved_podcasts.objects.filter(user=request.user, podcast=podcast).exists()
    context = {'podcast':podcast, 'is_saved':is_saved}
    return render(request, 'podcasts/podcast_detail.html', context)

@login_required


        # Unsave logic here
        
def save_podcast(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk)
    # Get or create a SavedPodcast instance for the user

    saved_podcasts, created = Saved_podcasts.objects.get_or_create(user=request.user)

# Check if the podcast is already saved, and add it if not
    if podcast not in saved_podcasts.podcast.all():
        saved_podcasts.podcast.add(podcast)
        messages.success(request, "Podcast added to your saved list.")


    return redirect('podcast-detail', pk=pk)

@login_required
def unsave_podcast(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk)
    # Retrieve the Saved_podcasts instance for the user
    try:
        saved_podcasts = Saved_podcasts.objects.get(user=request.user)
        if podcast in saved_podcasts.podcast.all():
            saved_podcasts.podcast.remove(podcast)
            
        
            
    except Saved_podcasts.DoesNotExist:
        messages.error(request, "You do not have any saved podcasts.")
    
    return redirect('podcast-detail', pk=pk)


@login_required
def saved_podcasts(request):
    # Assuming you only have one saved_podcasts instance per user
    saved_podcast_instance = Saved_podcasts.objects.filter(user=request.user).first()
    if saved_podcast_instance:
        podcasts = saved_podcast_instance.podcast.all()
    else:
        podcasts = []
    context = {'podcasts': podcasts}
    return render(request, 'podcasts/saved.html', context)
# Create your views here.
