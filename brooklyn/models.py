from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator
from django.utils import timezone

# Create your models here.
from django.db.models import OneToOneField

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ProjectName = models.CharField(max_length=100)
    EndpointURL = models.CharField(max_length=14000)
    Field1Name = models.CharField(max_length=50, default=' ')
    Field2Name = models.CharField(max_length=50, default=' ')
    Field3Name = models.CharField(max_length=50, default=' ')
    Field4Name = models.CharField(max_length=50, default=' ')
    Field5Name = models.CharField(max_length=50, default=' ')
    
    def __str__(self):
        return self.user.username + " " + self.ProjectName
    
class ProjectObject(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Field1 = models.CharField(max_length=10000000, default=' ')
    Field2 = models.CharField(max_length=10000000, default=' ')
    Field3 = models.CharField(max_length=10000000, default=' ')
    Field4 = models.CharField(max_length=10000000, default=' ')
    Field5 = models.CharField(max_length=10000000, default=' ')
    DateTime = models.DateTimeField(default=timezone.now())