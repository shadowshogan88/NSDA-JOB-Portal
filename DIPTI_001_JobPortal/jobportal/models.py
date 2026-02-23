from django.db import models
from django.contrib.auth.models import AbstractUser

class AuthUserModel(AbstractUser):
    USER_TYPES = [
        ('Jobseekers','Jobseekers'),
        ('Recruiters','Recruiters'),
    ]
    display_name = models.CharField(max_length=200, null=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=10, null=True)
    
    def __str__(self):
        return f'{self.display_name}-{self.user_type}'
    
class RecuriterProfileModel(models.Model):
    recuriter = models.OneToOneField(
        AuthUserModel,
        on_delete=models.CASCADE,
        related_name='recuriter_profile',
        null=True
    )
    company_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='media/company_image', null=True)
    
    def __str__(self):
        return f'{self.recuriter.display_name}'
    
class SeekerProfileModel(models.Model):
    seeker = models.OneToOneField(
        AuthUserModel,
        on_delete=models.CASCADE,
        related_name='seeker_profile',
        null=True
    )
    contact_number = models.CharField(max_length=20, null=True)
    skill_set = models.TextField(null=True)
    resume = models.FileField(upload_to='media/resume', null=True)

    def __str__(self):
        return f'{self.seeker.display_name}'
    
class JobPostModel(models.Model):
    posted_by = models.ForeignKey(
        RecuriterProfileModel,
        on_delete=models.CASCADE,
        related_name='seeker_job',
        null=True
    )
    title = models.CharField(max_length=200, null=True)
    openings = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=200, null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    job_description = models.TextField(null=True)
    skill_set = models.TextField(null=True)
    is_published = models.BooleanField(default=True, null=True)
    deadline = models.DateField(null=True)
    posted_at = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.title}'

class ApplicantModel(models.Model):
    STATUS = [
        ('Pending','Pending'),
        ('Shortlisted','Shortlisted'),
        ('Confirmed','Confirmed'),
        ('Rejected','Rejected'),
    ]
    applicant = models.ForeignKey(
        AuthUserModel,
        on_delete=models.CASCADE,
        related_name='applicant_job',
        null=True
    )
    job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name='applied_job',
        null=True
    )
    status = models.CharField(choices=STATUS, max_length=20, null=True)
    year_of_experience = models.PositiveIntegerField(null=True)
    resume = models.FileField(upload_to='media/applicant_resume', null=True)
    applied_at = models.DateField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        return f'{self.applicant.display_name}-{self.job.title}'