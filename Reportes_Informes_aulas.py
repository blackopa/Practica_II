import fitz
from pathlib import Path
import os
import io
from PIL import Image

def Extraer_Datos_Tablas_Rango_Variable(Datos_del_Informe,Comienzo):#Se extrae los datos de tablas que no se conoce la cantidad de filas que posee en el informe
    count=0
    a=[]
    for i in range(Comienzo,len(Datos_del_Informe)):
        if Datos_del_Informe[i]==Datos_del_Informe[53]:
            count=i
            break
        else:   
            a.append(Datos_del_Informe[i])
    return(a,count)
def Extraer_Imagenes_del_Informe(file_path,nombre_archivo,numero_pagina):#Numero de la pagina donde comienzan las fotos
    doc= fitz.open(file_path)
    image_path = f"./face_scrapper/face_scrapper/insightface/data/images/images{nombre_archivo}"
    os.mkdir(image_path)
    for page_index in range(numero_pagina,len(doc)):
 
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
            
            image.save(open(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))
        
    return
def Contador_de_Codigo_Colegio(codigo_colegio,cantidad_en_tabla_resumen,Tabla_Revisar,Nombre_Elemento):
    count=0
    for i in Tabla_Revisar[0]:
        if i==codigo_colegio:
            count+=1
    if count==int(cantidad_en_tabla_resumen):
        return print(f"La cantidad de {Nombre_Elemento} coincide con la tabla resumen")
    else:
        return print(f"La cantidad de {Nombre_Elemento} no coincide con la tabla resumen")
#enlaces=text[50]
#print(enlaces)

class Datos_Texto_Informe:
    def __init__(self,i,paginas,f_list):
        self.paginas=[13,43,44,45,46,47,48,49,50]
        self.nombre_archivo=f_list[i]
        self.file_path="./InformesPdf/Diciembre_adelante/%s"%(f_list[i])
    def __del__(self):
        print("listo")
    
    def Ordenar_Datos(self):
        self.informe=[]
        doc= fitz.open(self.file_path)
        for i in self.paginas:
            numero=i-1  
            page= doc.load_page(numero) #pagina que se quiere revisar del informe
            text = page.get_text("text")
            contenido=""#contenido dentro de la celda
            for i in range(len(text)):
                if text[i]=='\n':
                    self.informe.append(contenido)
                    contenido=""
                else: 
                    contenido+=text[i]
        #return(informe)
    def Informacion_de_las_Tablas(self):
        self.Actividad_asesoria=self.informe[:9]#Pagina que tiene la información de asesoria
        self.Elementos_red=self.informe[12:18]#Tabla resumen de elementos de red
        self.Tramos_canalización=self.informe[25:46]#Tabla resumen de tramos de canalización
        self.Cables=self.informe[49:53]#Tabla resumen de Cables
        self.Enlaces_existentes=Extraer_Datos_Tablas_Rango_Variable(self.informe,56)
        self.Rack_existentes=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Enlaces_existentes[1]+3)
        self.Rack_proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Rack_existentes[1]+3)
        self.Puntos_Proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Rack_proyectados[1]+3)
        self.Tramos_Proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Puntos_Proyectados[1]+3)

    def Verificar_Elementos_de_Red_Existentes(self):
        self.codigo_colegio=self.informe[71]
        self.nombre_colegio=self.informe[55]
        print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        self.cantidad_enlaces=self.Elementos_red[1]
        self.cantidad_racks_proyectados=self.Elementos_red[3]
        self.cantidad_puntos_proyectados=self.Elementos_red[5]
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_enlaces,self.Enlaces_existentes,"Enlaces")
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_racks_proyectados,self.Rack_proyectados,"Racks Proyectados")
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_puntos_proyectados,self.Puntos_Proyectados,"Puntos Proyectados")
        
class Reporte:
    def __init__(self,codigo_colegio,nombre_colegio):#agregar mas campos para el reporte
        self.codigo_colegio=codigo_colegio
        self.nombre_colegio=nombre_colegio
        

path="./InformesPdf/Diciembre_adelante"
f_list = os.listdir(path)#lista de archivos en esa carpeta
#f_list = filter(lambda f: f.endswith(('.pdf','.PDF')), f_list)#filtra la lista para que solo sean pdf}

#file_path="./InformesPdf/Diciembre_adelante/%s"%(f_list[1])
paginas=[13,43,44,45,46,47,48,49]
for i in range(len(f_list)):
    print("###################################")
    Texto_Informe=Datos_Texto_Informe(i,paginas,f_list)
    Texto_Informe.Ordenar_Datos()
    Texto_Informe.Informacion_de_las_Tablas()
    Texto_Informe.Verificar_Elementos_de_Red_Existentes()
    del Texto_Informe
    #tramos_p=Datos_Texto_Informe.Tramos_Proyectados
    #print(tramos_p)

#Extraer_Imagenes_del_Informe(Datos_del_Informe.file_path,Datos_del_Informe.nombre_archivo, 54) 

#Extraer_Imagenes_del_Informe(file_path,54)
