import fitz
from pathlib import Path
import os
import io
from PIL import Image

def Datos_pagina(file_name,paginas):
    datos_paginas=[]
    doc= fitz.open(file_name)
    for i in paginas:
        numero=i-1  
        page= doc.load_page(numero) #pagina que se quiere revisar del informe
        text = page.get_text("text")
        palabra=""
        for i in range(len(text)):
            if text[i]=='\n':
                datos_paginas.append(palabra)
                palabra=""
            else: 
                palabra+=text[i]
    return(datos_paginas)

def extraer_tabla_variable(resultado,limite):
    count=0
    a=[]
    for i in range(limite,len(resultado)):
        if resultado[i]==resultado[53]:
            count=i
            break
        else:   
            a.append(resultado[i])
    return(a,count)
def extraer_imagen(file_name,num_pag):
    doc= fitz.open(file_name)
    for page_index in range(num_pag,len(doc)):
 
        # get the page itself
        page = doc.load_page(page_index)
        image_list = page.get_images()
 
        # printing number of images found in this page
        if image_list:
            print(
             f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            rint("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):
 
            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
 
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            #image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
        
    return
#enlaces=text[50]
#print(enlaces)
f_list = os.listdir("./InformesPdf/Diciembre_adelante")
file_name="./InformesPdf/Diciembre_adelante/%s"%(f_list[1])
paginas=[13,43,44,45,46,47,48,49]
resultado=Datos_pagina(file_name, paginas)
###########Datos de las paginas############
#print(resultado[:9])
Actividad_asesoria=resultado[:9]
#print(Actividad_asesoria)
Elementos_red=resultado[12:18]
#print(Elementos_red)
Tramos_canalización=resultado[25:46]
#print(Tramos_canalización)
Cables=resultado[49:53]
#print(Cables)
###########Datos de las Tablas############
#Enlaces_existentes=extraer_tabla_variable(resultado,56)
#print(Enlaces_existentes[0])
#print(Enlaces_existentes[1])

#Rack_existentes=extraer_tabla_variable(resultado,Enlaces_existentes[1]+3)
#print(Rack_existentes[0])
#print(Rack_existentes[1])

#Rack_proyectados=extraer_tabla_variable(resultado,Rack_existentes[1]+3)
#print(Rack_proyectados[0])
#print(Rack_proyectados[1])

#Puntos_Proyectados=extraer_tabla_variable(resultado,Rack_proyectados[1]+3)
#print(Puntos_Proyectados[0])
#print(Puntos_Proyectados[1])

#Tramos_Proyectados=extraer_tabla_variable(resultado,Puntos_Proyectados[1]+3)
#print(Tramos_Proyectados[0])
#print(Tramos_Proyectados[1])
###########Extraccion de Imagenes#######
extraer_imagen(file_name,54)
