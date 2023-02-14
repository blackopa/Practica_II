from django.shortcuts import render
from django.http import HttpResponseRedirect

from .validations.process_file import get_report
from . import models
import hashlib
# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')

def enviar_resultado(request, report_id):
    if request.method == "GET":
        rr = models.Report.objects.get(id=report_id)
        report_strings = rr.reportestr.split("\r")
        return render(request, 'mainapp/enviar_resultado.html', {'reporte_strings': report_strings, 'id': report_id})

def step1(request):
    if request.method == "POST":
        file = request.FILES.get("file", None)
        rut_persona = request.POST.get("rut", "")
        nombre_persona = request.POST.get("nombre", "")
        if file is not None:
            report_strings, data_informe= get_report(file)
            rs = ""
            for r in report_strings:
                rs += r + "\r"
            id = hashlib.md5(rs.encode('utf-8')).hexdigest()
            persona = models.Persona(
                rut = rut_persona,
                nombre = nombre_persona
            )
            persona.save()
            di = models.Informe(
                codigo_colegio = data_informe["Codigo Colegio"],
                nombre_colegio = data_informe["Nombre Colegio"])
            di.save()
            print(di)
            rr = models.Report(
                id=id,
                reportestr = rs,
                rut_persona = persona,
                id_informe = di).save()
            
            return HttpResponseRedirect(f"/report/{id}")
        else:
            return HttpResponseRedirect("/")

def decision(request):
    if request.method == "POST":
        id_reporte = request.POST.get("reporte_id",None)
        comentario = request.POST.get("comentario", "")
        decision = request.POST.get("decision", "")
        if decision in ("Aprobado","Rechazado")\
                and id_reporte is not None:
            rr = models.Report.objects.get(id=id_reporte)
            rr.decision = decision
            rr.comentario = comentario
            rr.save()
        return HttpResponseRedirect("/exito")

def exito(request):
    if request.method == "GET":
        return render(request, 'mainapp/index.html', {'resultado_anterior': 'Éxito'})