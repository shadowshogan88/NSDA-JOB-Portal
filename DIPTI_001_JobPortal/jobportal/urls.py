from django.urls import path
from jobportal.views import *

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('', login_page, name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('home/',home_page, name='home_page'),
    path('profile/',profile_page, name='profile_page'),
    
    path('update-profile/',profile_update, name='profile_update'),
    path('job-list/',job_list,name='job_list'),
    path('post-job/',post_job, name='post_job'),
    
    path('edit-job/<int:job_id>/',edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/',delete_job, name='delete_job'),
    
    path('apply-job/<int:job_id>/',apply_job,name='apply_job'),
    path('applied-job-list/',applied_job_list,name='applied_job_list'),
    
]
