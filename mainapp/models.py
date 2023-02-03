from django.db import models

# Create your models here.
class Report(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    reportestr = models.CharField(max_length=20000)
