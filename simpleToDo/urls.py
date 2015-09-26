from django.conf.urls import patterns, include, url
from django.contrib import admin

from simpleToDo import views

urlpatterns = patterns('',
  
  	url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^userDashboard$', views.userDashboard_view, name='userDashboard'),
    url(r'^addTask$', views.addTask_view, name='addTask'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^(?P<task_Id>[0-9]+)$', views.deleteTask_view, name='deleteTask'),
)