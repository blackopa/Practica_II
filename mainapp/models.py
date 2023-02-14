from django.db import models
from django.utils import timezone 
# Create your models here.


class Persona(models.Model):
    rut = models.CharField(max_length=18, primary_key=True)
    nombre = models.CharField(max_length=64)
    
class Informe(models.Model):
    informe_id = models.AutoField(primary_key=True)
    nombre_informe = models.CharField(max_length=255, default="test")
    nombre_colegio = models.CharField(max_length=255)
    codigo_colegio = models.IntegerField()

    
class Report(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    reportestr = models.CharField(max_length=20000)
    decision = models.CharField(max_length=32)
    comentario = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now=True)
    rut_persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    id_informe = models.ForeignKey(Informe, on_delete=models.CASCADE)
    