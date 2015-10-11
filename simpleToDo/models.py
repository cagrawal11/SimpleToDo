from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.
class Task(models.Model):
	user = models.ForeignKey(User)
	task_name = models.CharField(max_length=50)
	task_created = models.DateTimeField(default=datetime.now)
	task_description = models.TextField()
	due_date = models.DateTimeField(default=None)
	deleted_flag = models.IntegerField(default=0)
	done_flag = models.IntegerField(default=0)
	#dueOn = models.DateField(default=None)
