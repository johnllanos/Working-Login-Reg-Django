from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name + ' | ' + self.last_name + ' | ' + self.email

class Job(models.Model):
    job = models.TextField(max_length=1000)
    description = models.TextField(max_length=400)
    location = models.TextField(max_length=400)
    job_creater = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,related_name='jobs')


    def __str__(self):
        return self.job  + ' | ' 