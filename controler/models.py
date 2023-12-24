from django.db import models
from django.utils.timezone import now
# Create your models here.
class About_Page(models.Model):
    title = models.CharField(db_index=True, default='',max_length=100)
    content = models.TextField(db_index=True, default='')
    date = models.DateTimeField(default=now, db_index=True)
    image = models.FileField(upload_to='e-pages/about', default='', db_index=True)

class Privacy_Edit(models.Model):
    title = models.CharField(db_index=True, default='',max_length=100)
    content = models.TextField(db_index=True, default='')
    date = models.DateTimeField(default=now, db_index=True)
    
    image = models.FileField(upload_to='e-pages/privacy', default='', db_index=True)
    