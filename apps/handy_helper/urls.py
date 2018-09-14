from django.conf.urls import url
from . import views           

urlpatterns = [
    url(r'^$', views.sign_in),
    url(r'^reg_process$', views.reg_process),
    url(r'^sign_in_process$', views.sign_in_process),
    url(r'^jobs$', views.jobs),
    url(r'^job_post$', views.job_post),
    url(r'^logout$', views.logout),
    url(r'^back$', views.back),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^add_job$', views.add_job),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^show_job/(?P<id>\d+)$', views.show_job),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
    url(r'^done/(?P<id>\d+)$', views.done),
    url(r'^edit_job/(?P<id>\d+)$', views.edit_job),
    url(r'^edit_job_process/(?P<id>\d+)$', views.edit_job_process),
]                            
