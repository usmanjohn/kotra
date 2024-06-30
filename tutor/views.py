from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutoring
from .forms import TutoringForm
# Create your views here.
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def tag_list(request, tag_slug = None):
    tutoring = Tutoring.objects.filter(status = 'posted').order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = tutoring.filter(tags__in = [tag])
    context = {'tutoring':tutoring}
    return render(request, 'tutor/t_tags.html', context)

def tutors_list(request):
    tutoring = Tutoring.objects.filter(status = 'posted').order_by('-date','title')
    context = {'tutoring':tutoring}
    return render(request, 'tutor/tutoring_list.html',context )


def tutors_detail(request, pk):
    tutor = get_object_or_404(Tutoring, id = pk)
    context = {'tutor':tutor}
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
