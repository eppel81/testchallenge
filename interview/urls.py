from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.list_interviews, name='list_interviews'),
    url(r'^(?P<interview_id>[0-9]*)/$', views.pass_interview, name='pass_interview'),
    url(r'^(?P<interview_id>[0-9]*)/results/$', views.interview_results, name='interview_results'),
    url(r'^(?P<interview_id>[0-9]*)/edit/$', views.edit_interview, name='edit_interview'),
    url(r'^add_interview/', views.add_interview, name='add_interview'),
    url(r'^message', views.message, name='message'),
]
