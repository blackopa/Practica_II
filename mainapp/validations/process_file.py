
from pathlib import Path
import os
import io
from django.core.files.storage import FileSystemStorage
from .Informe_datos import DatosTextoInforme


#Funcion que obtiene el reporte que se muestra en la pagina.
def get_report(file):
    #Obtiene el archivo Pdf
    filename = file.name
    full_path_file = os.path.join('tmp', filename)
    fs = FileSystemStorage(location='tmp')
    #Se guarda en tmp
    fs.save(filename, file)
    #Se revisa el informe, esto funciona para informes con el formato actualizado
    TextoInforme = DatosTextoInforme(full_path_file)
    TextoInforme.ordenar_datos()
    TextoInforme.informacion_de_las_tablas()
    datos = TextoInforme.datos_colegio()
    data_informe = dict()
    data_informe["Codigo Colegio"] = datos[0]
    data_informe["Nombre Colegio"] = datos[1]
    #Se guarda la información importante que se mostrara
    data = []
    data.append(TextoInforme.verificar_elementos_de_red_existentes())
    data.extend(TextoInforme.verificar_tramos_de_canalizacion())
    data.append(TextoInforme.verificar_metros_de_cable()) 
    #El numero 54 representa el comienzo promedio de los informes en que se encuentran las fotos   
    data.extend(TextoInforme.detectar_caras(54,filename))  
    #Se borra el objeto, ya que no se necesita mas
    del TextoInforme
    return data,data_informe





