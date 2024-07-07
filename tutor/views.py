from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutoring, Review, SavedTutorial
from .forms import TutoringForm, ReviewForm
# Create your views here.
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

def tag_list(request, tag_slug = None):
    tutoring = Tutoring.objects.filter(status = 'posted').order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        tutoring_tags = tutoring.filter(tags__in = [tag])
    context = {'tutoring':tutoring_tags}
    return render(request, 'tutor/t_tags.html', context)

def tutors_list(request):
    query = request.GET.get('q', '')  # Get the search query from GET request
    tutoring = Tutoring.objects.filter(status='posted').order_by('-date', 'title')

    if query:  # If a query is present, filter by the search term in the title
        tutoring = tutoring.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        

    context = {'tutoring': tutoring, 'query': query}
    return render(request, 'tutor/tutoring_list.html', context)



def tutors_detail(request, pk):
    tutorial = get_object_or_404(Tutoring, id=pk)
    user_reviews = Review.objects.filter(tutorial=tutorial).order_by('-date')
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedTutorial.objects.filter(user=request.user, tutorial=tutorial).exists()
    if request.method == 'POST' and request.user.is_authenticated:
        user_review = user_reviews.filter(reviewer=request.user).first()

        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.tutorial = tutorial
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('tutor-detail', pk=pk)
    else:
        form = ReviewForm()

    context = {
        'tutor': tutorial,
        'form': form,
        'user_review': user_reviews,
        'is_saved':is_saved
    }
    return render(request, 'tutor/tutor_detail.html', context)



@login_required
def tutors_create(request):
    print("Method:", request.method)  # Check the method
    if request.method == 'POST':
        forms = TutoringForm(request.POST)
        print("Form received:", forms.is_bound)  # Check if form is bound
        if forms.is_valid():
            print("Form is valid")
            form = forms.save(commit=False)
            form.author = request.user  # Manually assign the author
            form.save()
            forms.save_m2m()
            messages.success(request, 'Tutorial created successfully and in Review')
            return redirect('tutors-list')
        else:
            forms = TutoringForm() 
            messages.error(request, 'Some of the fields are not filled correctly')

            print("Form errors:", forms.errors)  # Log form errors
    else:
        forms = TutoringForm()
    
    context = {'forms': forms}
    return render(request, 'tutor/tutoring_create.html', context)


@login_required
def tutor_update(request, pk):
    tutor = get_object_or_404(Tutoring, id = pk)
    if request.user == tutor.author and request.method == 'POST':

        form = TutoringForm(request.POST, instance=tutor)
        if form.is_valid():
            form = form.save(commit = False)
            form.status = 'submitted'
            form.save()
            messages.success(request, 'Tutorial updated successfully and in Review')
            return redirect('tutor-detail', pk = tutor.pk)
    else:
        form = TutoringForm(instance=tutor)
    context = {'form':form}
    return render(request, 'tutor/tutor_update.html',context)


def tutor_delete(request, pk):
    tutor = get_object_or_404(Tutoring, id = pk)
    if request.user == tutor.author and request.method == 'POST':
        tutor.delete()
        messages.success(request, 'Tutorial deleted')
        return redirect('tutors-list')
    context = {'tutor':tutor}
    return render(request, 'tutor/tutor_delete.html', context)



@login_required
def save_tutorial(request, pk):
    tutorial = get_object_or_404(Tutoring, id=pk)
    SavedTutorial.objects.get_or_create(user=request.user, tutorial=tutorial)
    
    return redirect('tutor-detail', pk=pk)

@login_required
def saved_tutorials_list(request):
    saved_tutorials = SavedTutorial.objects.filter(user=request.user).select_related('tutorial')    
    context = {'saved_tutorials': saved_tutorials}
    return render(request, 'tutor/saved_tutorials.html', context)

@login_required
def unsave_tutorial(request, pk):
    tutorial = get_object_or_404(Tutoring, id=pk)
    saved_tutorial = SavedTutorial.objects.filter(user=request.user, tutorial=tutorial)
    if saved_tutorial.exists():
        saved_tutorial.delete()
    return redirect('tutor-detail', pk=pk)