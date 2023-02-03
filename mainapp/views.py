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
        return render(request, 'mainapp/enviar_resultado.html', {'reporte_strings': report_strings})

def step1(request):
    if request.method == "POST":
        file = request.FILES.get("file", None)
        if file is not None:
            report_strings = get_report(file)
            rs = ""
            for r in report_strings:
                rs += r + "\r"
            id = hashlib.md5(rs.encode('utf-8')).hexdigest()
            rr = models.Report(
                id=id,
                reportestr = rs).save()
            return HttpResponseRedirect(f"/report/{id}")
        else:
            return HttpResponseRedirect("/")

def decision(request):
    if request.method == "POST":
        return HttpResponseRedirect("/exito")

def exito(request):
    if request.method == "GET":
        return render(request, 'mainapp/index.html', {'resultado_anterior': 'Éxito'})