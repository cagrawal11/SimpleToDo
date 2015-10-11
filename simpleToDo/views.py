from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
			messages.success(request, "logged In success")
			return HttpResponseRedirect('userDashboard')
		else: 
			messages.error(request, "Invalid Username or Password")
			return render(request, 'index.html', {})

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
'''
def userDashboard_view(request):
	#if request.method == 'POST':
	if request.user.is_authenticated():
		#allTasks = models.Task.objects.filter(user=request.user).exclude(done_flag=1, deleted_flag=1)
		allTasks = models.Task.objects.filter(user=request.user, done_flag=0, deleted_flag=0)
		context = {'allTasks':allTasks, 'user':request.user.username}
		return render(request, 'home.html', context)
		#return HttpResponseRedirect('userDashboard')
	else:
		#redirect with user not logged in message
		messages.error(request, "User not logged in")
		return render(request, 'index.html', {})
'''
def userDashboard_view(request):
	if request.user.is_authenticated():
		#allTasks = models.Task.objects.filter(user=request.user).exclude(done_flag=1, deleted_flag=1)
		allTasks = models.Task.objects.filter(user=request.user, done_flag=0, deleted_flag=0)
		context = {'TaskList':allTasks, 'user':request.user.username, 'allTasks':'allTasks'}
		return render(request, 'home.html', context)
	else:
		#redirect with user not logged in message
		messages.error(request, "User not logged in")
		return render(request, 'index.html', {})

#@login_required
def addTask_view(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			task_name = request.POST['task_name']
			task_description = request.POST['task_description']
			due_date = datetime.datetime.strptime(request.POST['due_date'], '%m/%d/%Y')
			user = request.user
			#dueOn = datetime.datetime.strptime(request.POST['due_date'], '%m/%d')
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

def deleteTask_view(request, task_id):
	deletedTask = models.Task.objects.get(id = task_id)
	deletedTask.deleted_flag = 1
	deletedTask.save()
	return HttpResponseRedirect('/userDashboard')
	#return HttpResponse(deletedTask.task_name)

def doneTask_view(request, task_id):
	doneTask = models.Task.objects.get(id = task_id)
	doneTask.done_flag = 1
	doneTask.save()
	#return render(request, 'home.html', {})
	return HttpResponseRedirect('/userDashboard')

def show_deleted_view(request):
	deletedTask = models.Task.objects.filter(deleted_flag = 1, user=request.user)
	context = {'TaskList':deletedTask, 'deleted':'deleted' }
	"""ToDo: handle case for no deleted task"""
	return render(request, 'home.html', context)

def show_today_view(request):
	todayDate = datetime.datetime.now()
	str(todayDate)
	todayDate.strftime('%m/%d/%Y')
	todaysTask = models.Task.objects.get(due_date=todayDate)
	if todaysTask == None:
		return render(request, 'home.html', {})
	context = { 'todaysTask':todaysTask }
	return render(request, 'home.html', context)

def show_doneTask_view(request):
	doneTask = models.Task.objects.filter(done_flag=1, user=request.user)
	context = {'TaskList': doneTask, 'done':'done'}
	return render(request, 'home.html', context)