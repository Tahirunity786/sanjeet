from datetime import timezone
from django.db import models
from django.utils.timezone import now
class ipaddresshandle(models.Model):
    ip = models.CharField(max_length=100, db_index=True, default='')
class contact(models.Model):
    job_title = models.CharField(max_length=200,default='', db_index=True)
    email = models.EmailField(default='', db_index=True)
    phone_no = models.CharField(max_length=20,default='', db_index=True)
    first_name = models.CharField(max_length=200,default='', db_index=True)
    last_name = models.CharField(max_length=200,default='', db_index=True)
    subject = models.CharField(max_length=200,default='', db_index=True)
    message = models.TextField(default='', db_index=True)

class Black_token(models.Model):
    token1 = models.CharField(max_length=100, default='', db_index=True)

class UserReport(models.Model):
    user_token = models.ForeignKey(Black_token, on_delete=models.CASCADE)
    email = models.EmailField(db_index=True, default='', blank=True, null=True)
    clinic_name = models.CharField(max_length=100, default="BackupDoc", db_index=True)
    media = models.TextField(default='', db_index=True)
    tmedia = models.TextField(default='', db_index=True, null=True, blank=True)
    report = models.TextField(db_index=True)
    date = models.DateTimeField(default=now, db_index=True)
    
    # expiration_time = models.DateTimeField()


from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class TrafficData(models.Model):
    device_info = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    visit_timestamp = models.DateTimeField()
    leave_timestamp = models.DateTimeField(null=True, blank=True)
    is_old_user = models.BooleanField(default=False)