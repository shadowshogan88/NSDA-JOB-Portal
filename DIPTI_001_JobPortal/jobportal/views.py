from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from jobportal.models import *
from jobportal.forms import *

def register_page(request):
    if request.method == 'POST':
        display_name = request.POST.get('display_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        user_exists = AuthUserModel.objects.filter(username=username).exists()
        if user_exists:
            messages.warning(request,'User already exists.')
            return redirect('register_page')
        if password == confirm_password:
            user = AuthUserModel.objects.create_user(
                username=username, 
                email = email,
                user_type=user_type, 
                display_name=display_name,
                password=password
            )
            if user:
                if user_type == 'Recruiters':
                    RecuriterProfileModel.objects.create(
                        recuriter = user
                    )
                else:
                    SeekerProfileModel.objects.create(
                        seeker = user
                    )
            messages.success(request, 'User created successfully.')
            return redirect('login_page')
        else:
            messages.warning(request,'Password not matched.')
            return redirect('register_page')
    
    
    return render(request, 'auth/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')
        else:
            messages.warning(request,'Invalid credentials.')
            return redirect('login_page')
        
    return render(request, 'auth/login.html')

def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def home_page(request):
    
    return render(request, 'home.html')

@login_required
def profile_page(request):
    
    return render(request, 'profile.html')

def profile_update(request):
    current_user = request.user
    
    if current_user.user_type == 'Recruiters':
        rec_data = RecuriterProfileModel.objects.get(recuriter=current_user)
        if request.method == 'POST':
            info_form_data = RecProfileForm(request.POST, request.FILES,instance=rec_data)
            if info_form_data.is_valid():
                info_form_data.save()
                return redirect('profile_page')

        info_form_data = RecProfileForm(instance=rec_data)
    else:
        sec_data = SeekerProfileModel.objects.get(seeker=current_user)
        if request.method == 'POST':
            info_form_data = SeekerProfileForm(request.POST, request.FILES, instance=sec_data)
            if info_form_data.is_valid():
                info_form_data.save()
                return redirect('profile_page')
            
        info_form_data = SeekerProfileForm()
    
    context = {
        'title': 'Update Profile',
        'info_form_data':info_form_data,
    }
    return render(request, 'master/info-form.html',context)



#-------------Job Post
def job_list(request):
    job_data = JobPostModel.objects.all()
    context = {
        'job_data': job_data
    }
    
    return render(request, 'job-list.html', context)

def post_job(request):
    current_user = request.user.recuriter_profile
    if request.method == 'POST':
        info_form_data = JobPostForm(request.POST)
        if info_form_data.is_valid():
            info_form_data = info_form_data.save(commit=False)
            info_form_data.posted_by = current_user
            info_form_data.is_published = True
            info_form_data.save()
            return redirect('job_list')
        
    info_form_data = JobPostForm()
    
    context = {
        'info_form_data':info_form_data,
        'title': 'Job Post Information'
    }
    return render(request, 'master/info-form.html',context)

def edit_job(request, job_id):
    job_data = JobPostModel.objects.get(id = job_id)
    if request.method == 'POST':
        info_form_data = JobPostForm(request.POST, instance=job_data)
        if info_form_data.is_valid():
            info_form_data.save()
            return redirect('job_list')
        
    info_form_data = JobPostForm(instance=job_data)
    
    context = {
        'info_form_data':info_form_data,
        'title': 'Update Job Information'
    }
    return render(request, 'master/info-form.html',context)

def delete_job(request, job_id):
    JobPostModel.objects.get(id = job_id).delete()
    return redirect('job_list')

def applied_job_list(request):
    current_user = request.user
    applied_job = ApplicantModel.objects.filter(applicant = current_user)
    context = {
        'applied_job':applied_job
    }
    
    return render(request, 'applied-job-list.html',context)

def apply_job(request, job_id):
    job_data = JobPostModel.objects.get(id=job_id)
    current_user = request.user
    if request.method == 'POST':
        info_form_data = AppliedForm(request.POST, request.FILES)
        
        if info_form_data.is_valid():
            info_form_data = info_form_data.save(commit=False)
            info_form_data.job = job_data
            info_form_data.applicant = current_user
            info_form_data.status= 'Pending'
            info_form_data.save()
            return redirect('applied_job_list')
        
    info_form_data = AppliedForm()
    context = {
        'info_form_data': info_form_data,
        'title':'Apply on: ',
        'job_data':job_data,
        
    }
    return render(request, 'master/info-form.html',context)