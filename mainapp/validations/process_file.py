
import fitz
from pathlib import Path
import os
import io
from PIL import Image 
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from .Informe_datos import DatosTextoInforme


#Funcion que obtiene el reporte que se muestra en la pagina.
def get_report(file):
    filename = file.name
    full_path_file = os.path.join('tmp', filename)
    fs = FileSystemStorage(location='tmp')
    fs.save(filename, file)
    TextoInforme = DatosTextoInforme(full_path_file)
    TextoInforme.ordenar_datos()
    TextoInforme.informacion_de_las_tablas()
    
    data = []
    data.append(TextoInforme.verificar_elementos_de_red_existentes())
    data.extend(TextoInforme.verificar_tramos_de_canalizacion())
    data.append(TextoInforme.verificar_metros_de_cable())   
    data.extend(TextoInforme.detectar_caras(54,filename))#El numero 54 representa el comienzo promedio de los informes en que se encuentran las fotos   
    del TextoInforme
    return data





