from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from .models import Job,Application
from django.db.models import Q
from .models import Job
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
def home(request):
    query = request.GET.get('q')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(company_name__icontains=query)
        )

    paginator = Paginator(jobs, 4)

    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'home.html', {'jobs': jobs})
@login_required
def create_job(request):
    form = JobForm(request.POST or None)

    if form.is_valid():
        job = form.save(commit=False)
        job.created_by = request.user
        job.save()
        messages.success(request, "Job created successfully")

        return redirect('home')

    return render(request, 'create_job.html', {'form': form})

@login_required
def employer_dashboard(request):
    jobs = Job.objects.all()
    
    return render(
        request,
        'employer_dashboard.html',
        {'jobs': jobs}
    )

@login_required
def candidate_dashboard(request):
    applications = Application.objects.filter(user=request.user)

    return render(
        request,
        'candidate_dashboard.html',
        {'applications': applications}
    )

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        resume = request.FILES['resume']

        Application.objects.create(
            user=request.user,
            job=job,
            resume=resume
        )
        send_mail(
            'Application Submitted',
            'Your application was submitted successfully.',
            'admin@gmail.com',
            ['user@gmail.com'],
        )

        return redirect('candidate_dashboard')

    return render(request, 'apply.html', {'job': job})

@login_required
def update_job(request, id):
    job = Job.objects.get(id=id)

    form = JobForm(request.POST or None, instance=job)

    if form.is_valid():
        form.save()
        messages.success(request, "Job updated successfully")
        return redirect('dashboard')

    return render(request, 'update_job.html', {'form': form})

@login_required
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    messages.success(request, "Job deleted successfully")

    return redirect('dashboard')

@login_required
def update_resume(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        user=request.user
    )

    if request.method == 'POST':
        application.resume = request.FILES['resume']
        application.save()

        messages.success(request, "Resume updated successfully")
        return redirect('candidate_dashboard')

    return render(
        request,
        'update_resume.html',
        {'application': application}
    )
