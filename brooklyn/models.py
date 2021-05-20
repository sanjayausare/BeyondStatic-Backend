from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator

# Create your models here.
from django.db.models import OneToOneField

# Create your models here.
class Project(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    ProjectName = models.CharField(max_length=100)
    endpointURL = models.CharField(max_length=14000)
    field1Name = models.CharField(max_length=50, default=' ')
    field2Name = models.CharField(max_length=50, default=' ')
    field3Name = models.CharField(max_length=50, default=' ')
    field4Name = models.CharField(max_length=50, default=' ')
    field5Name = models.CharField(max_length=50, default=' ')
    
    def __str__(self):
        return self.user.username + " " + self.ProjectName
    
class ProjectObject(models.Model):
    project: OneToOneField = models.OneToOneField(Project, on_delete=models.CASCADE)
    field1 = models.CharField(max_length=10000000, default=' ')
    field2 = models.CharField(max_length=10000000, default=' ')
    field3 = models.CharField(max_length=10000000, default=' ')
    field4 = models.CharField(max_length=10000000, default=' ')
    field5 = models.CharField(max_length=10000000, default=' ')
    dateTime = models.DateTimeField(default=datetime.now())