from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required

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
    context= {'job':job}
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
