from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Podcast, SavedPodcast

def podcast_list(request):
    podcasts = Podcast.objects.all().order_by('-date_published')
    paginator = Paginator(podcasts, 10)  # Show 10 podcasts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'podcasts/podcast_list.html', {'page_obj': page_obj})

def podcast_detail(request, pk):
    podcast = get_object_or_404(Podcast, id=pk)
    is_saved = SavedPodcast.objects.filter(user=request.user, podcast=podcast).exists() if request.user.is_authenticated else False
    return render(request, 'podcasts/podcast_detail.html', {'podcast': podcast, 'is_saved': is_saved})

@login_required
def toggle_save_podcast(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk)
    saved_podcast, created = SavedPodcast.objects.get_or_create(user=request.user, podcast=podcast)
    
    if not created:
        saved_podcast.delete()
        is_saved = False
        message = "Podcast removed from your saved list."
    else:
        is_saved = True
        message = "Podcast added to your saved list."
    
    messages.success(request, message)
    return JsonResponse({'is_saved': is_saved, 'message': message})

@login_required
def saved_podcasts(request):
    saved = SavedPodcast.objects.filter(user=request.user).select_related('podcast').order_by('date_saved')
    
    paginator = Paginator(saved, 10)
      # Show 10 podcasts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'podcasts/saved.html', {'page_obj': page_obj}) 