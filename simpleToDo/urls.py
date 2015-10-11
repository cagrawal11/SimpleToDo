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
    url(r'^task/doneTask/(?P<task_id>[0-9]+)$', views.doneTask_view, name='doneTask_view'),
    url(r'^task/deleteTask/(?P<task_id>[0-9]+)$', views.deleteTask_view, name='deleteTask'),
    url(r'^showDeleted$', views.show_deleted_view, name='showDeleted'),
    url(r'^showDoneTask$', views.show_doneTask_view, name='showDoneTask'),
    url(r'^showToday$', views.show_today_view, name='showToday'),
)