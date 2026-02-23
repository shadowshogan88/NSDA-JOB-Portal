from django.contrib import admin
from jobportal.models import *


admin.site.register([AuthUserModel, RecuriterProfileModel, SeekerProfileModel, JobPostModel, ApplicantModel])
