from django.db import models
from django.utils import timezone 
# Create your models here.


class Persona(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    nombre = models.CharField(max_length=64)
    rut = models.CharField(max_length=18)


    
class Report(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    reportestr = models.CharField(max_length=20000)
    decision = models.CharField(max_length=32, default='revisar')
    comentario = models.CharField(max_length=255, default='')
    fecha = models.DateTimeField('date published', default=timezone.now)
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, default=0)
    