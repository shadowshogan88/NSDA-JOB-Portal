from django import forms
from jobportal.models import *

class RecProfileForm(forms.ModelForm):
    class Meta:
        model = RecuriterProfileModel
        fields = '__all__'
        exclude = ['recuriter']
        
class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfileModel
        fields = '__all__'
        exclude = ['seeker']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['is_published','posted_by']
        
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'date'})
        }
        
class AppliedForm(forms.ModelForm):
    class Meta:
        model = ApplicantModel
        fields = ['year_of_experience','resume']