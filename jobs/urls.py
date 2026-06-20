from django.urls import path
from .views import home, create_job
from .views import home, create_job, employer_dashboard,candidate_dashboard,apply_job,delete_job
from .views import update_job,update_resume

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_job, name='create_job'),
    path('dashboard/', employer_dashboard, name='dashboard'),
    path('candidate/', candidate_dashboard, name='candidate_dashboard'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('update/<int:id>/', update_job, name='update_job'),
    path('delete/<int:id>/', delete_job, name='delete_job'),
    path('update-resume/<int:application_id>/', update_resume,name='update_resume'),
]