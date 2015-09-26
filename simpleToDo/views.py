from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import models, datetime
#from datetime import datetime
# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def signin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			#return render(request, 'index.html', {})
			return HttpResponseRedirect('userDashboard')
		else: 
			'''TODO: return appropriate response for unsuccessfull login'''
			return HttpResponse("Na na") 

def signup(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=username):
			return render(request, 'index.html', {'message':'User already exist!'})
		else:
			user = User.objects.create_user(username=password, password=password)
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect('userDashboard')

#@login_required
def userDashboard_view(request):
	#if request.method == 'POST':
	if request.user.is_authenticated():
		allTasks = models.Task.objects.filter(user=request.user)
		context = {'allTasks':allTasks, 'user':request.user.username}
		return render(request, 'dashboard2.html', context)
	else:
		return render(request, 'index.html', {})


#@login_required
def addTask_view(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			task_name = request.POST['task_name']
			task_description = request.POST['task_description']
			due_date = datetime.datetime.strptime(request.POST['due_date'], '%m/%d/%Y')
			user = request.user
			'''TODO: take selected date instead of datetime.datetime.now()'''
			taskData = models.Task(task_name = task_name, task_description=task_description, 
									task_created=datetime.datetime.now(), due_date=due_date, user=user)
			taskData.save()
			return HttpResponseRedirect('userDashboard')
		return HttpResponse("Not a post method, so error!!")
	else:
		return HttpResponseRedirect('signin')
		
def logout_view(request):
	logout(request)
	return render(request, 'index.html', {})

'''TODO: deleting task and handling deleted ones'''
def deleteTask_view(request, task_Id):
	deletedTask = models.Task.objects.get(id = task_Id)
	deletedTask.delete()
	return HttpResponseRedirect('userDashboard')
	#return HttpResponse(deletedTask.task_name)