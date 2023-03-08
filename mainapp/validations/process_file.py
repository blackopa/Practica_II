
from pathlib import Path
import os
import io
from django.core.files.storage import FileSystemStorage
from .Informe_datos import DatosTextoInforme


#Funcion que obtiene el reporte que se muestra en la pagina. El reporte es un gran string con sus distintas secciones.
def get_report(file):
    #Obtiene el archivo Pdf
    filename = file.name
    full_path_file = os.path.join('tmp', filename)
    fs = FileSystemStorage(location='tmp')
    #Se guarda en tmp
    fs.save(filename, file)
    #Se revisa el informe, esto funciona para informes con el formato actualizado
    try:
        TextoInforme = DatosTextoInforme(full_path_file)
    except:
        data.append("Error en la lectura, asegure que el archivo pdf sea el correcto")
    try:
        TextoInforme.ordenar_datos()
    except:
        data.append("Error, revíselo manualmente")
   
    TextoInforme.informacion_de_las_tablas()
    
    try:
        TextoInforme.ordenar_datos_planos()
    except:
        data.append("Error, revíselo manualmente")
    datos = TextoInforme.datos_colegio()
    data_informe = dict()
    data_informe["Codigo Colegio"] = datos[0]
    data_informe["Nombre Colegio"] = datos[1]
    
    #Se guarda la información importante que se mostrara
    data = []
    data.append("<h2>Elementos de Red</h2>")
    try:
        data.append(TextoInforme.verificar_elementos_de_red_existentes())
    except:
        data.append("Error en lectura de Elementos de Red, revíselo manualmente")
    data.append("<h2>Tramos de Canalización</h2>")
    try:
        data.extend(TextoInforme.verificar_tramos_de_canalizacion())
    except:
        data.append("Error en lectura de Tramos de Canalización, revíselo manualmente")
    data.append("<hr><h2>Puntos de Fibra y cable UTP-6</h2>")
    data.append(TextoInforme.verificar_metros_de_cable()) 
    data.append("<h2>Sección Planos</h2>")
    try:
        planos = TextoInforme.contar_puntos_en_plano(TextoInforme.separar_en_los_nuemros())
        data.append(planos)
    except:
        data.append("Error de lectura en contador de puntos de los planos, revíselo manualmente")
    try:
        tramos = TextoInforme.contar_tramos_en_planos(TextoInforme.separar_los_tramos())
        data.append(tramos)
    except:
        data.append("Error de lectura en contador de tramos de los planos, revíselo manualmente")
    
    try:
        data.append(TextoInforme.contar_puntos_cuadro_resumen())
    except:
        data.append("Error en lectura de cuadro Resumen de los planos, revíselo manualmente")
    #El numero 54 representa el comienzo promedio de los informes en que se encuentran las fotos   
    data.append("<h2>Caras Detectadas</h2>")
    try:
        data.extend(TextoInforme.detectar_caras(54,filename))  
    except:
        data.append("Error en detección de caras, revíselo manualmente")
    #Se borra el objeto, ya que no se necesita mas
    del TextoInforme
    return data,data_informe





