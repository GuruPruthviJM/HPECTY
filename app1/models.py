from django.db import models

# Create your models here.
class Query(models.Model):
    useremail = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    userquery = models.TextField(default="NULL")
