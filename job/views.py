from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, SavedJobs
from .forms import JobForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def job_list(request):
    jobs = Job.objects.all()
    context = {'jobs':jobs}
    return render(request, 'job/job_list.html', context)

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST,  request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.uploader = request.user
            form.save()
            return redirect('job-list')
    else:
        form = JobForm()
    context = {'form':form}
    return render(request, 'job/create_job.html', context)

def job_detail(request, pk):
    job = get_object_or_404(Job, id = pk)
    is_saved = SavedJobs.objects.filter(user=request.user, job=job).exists() if request.user.is_authenticated else False
    context= {'job':job, 'is_saved':is_saved}
    return render(request, 'job/job_detail.html', context)

@login_required
def job_update(request, pk):

    job = get_object_or_404(Job, id = pk)
    
    if request.method == 'POST' and job.uploader == request.user:
        form = JobForm(request.POST, request.FILES, instance=job )
        if form.is_valid():
            form.save()
            return redirect('job-detail', pk = pk)
    else:
        form = JobForm(instance=job)
    context= {'form':form}
    return render(request, 'job/update_job.html', context)

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, id = pk)
    if job.uploader == request.user:
        if request.method == 'POST':
            job.delete()
            return redirect('job-list')
    else:
        print('You are not allowed')
    context = {'job':job}
    return render(request, "job/job_delete.html", context)


@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(Job, pk = pk)
    saved_job, created = SavedJobs.objects.get_or_create(user = request.user, job = job)
    if not created:
        saved_job.delete()
        is_saved=False
        message = 'Job removed from your saved list.'
    else:
        is_saved = True
        message = 'Job adder to your saved list.'
    messages.success(request, message)
    return JsonResponse({'is_saved':is_saved, 'message':message})

@login_required
def saved_jobs(request):
    saved = SavedJobs.objects.filter(user = request.user).select_related('job')
    paginator = Paginator(saved, 10)  # Show 10 podcasts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'job/saved.html', {'page_obj': page_obj}) 
   