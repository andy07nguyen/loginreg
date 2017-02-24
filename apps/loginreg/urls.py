from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^userlogin$', views.loginProcess),
    url(r'^travels$', views.travels),
    url(r'^add$', views.addplan),
    url(r'^addProcess$', views.addProcess),
    url(r'^destroy/(?P<id>\d+)/$', views.destroy, name="remove_url"),
    url(r'^remove/(?P<id>\d+)/$', views.remove, name="delete"),
    url(r'^logout$', views.logout),
    url(r'^.+$', views.index)
]
