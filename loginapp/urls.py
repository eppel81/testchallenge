from django.conf.urls import url

from loginapp import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.register_confirm),
]
