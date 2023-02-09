
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

def get_report(file):
    filename =file.name
    full_path_file = os.path.join('tmp', filename)
    fs = FileSystemStorage(location='tmp')
    fs.save(filename, file)
    Texto_Informe=Datos_Texto_Informe(full_path_file)
    Texto_Informe.Ordenar_Datos()
    Texto_Informe.Informacion_de_las_Tablas()
    
    data = []
    data.append(Texto_Informe.Verificar_Elementos_de_Red_Existentes())
    data.extend(Texto_Informe.Verificar_Tramos_de_Canalizacion())
    data.append(Texto_Informe.Verificar_Metros_de_Cable())   
    data.extend(Texto_Informe.Detectar_caras(54,filename))   
            
    
    del Texto_Informe
    #aqui meter código
    
    return data

###########Funciones######################
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
def remove_img(self, path, img_name):
    os.remove(path + '/' + img_name)
# check if file exists or not
    if os.path.exists(path + '/' + img_name) is false:
        # file did not exists
        return True


def Contador_de_Codigo_Colegio(codigo_colegio,cantidad_en_tabla_resumen,Tabla_Revisar,Nombre_Elemento):#Cuenta las filas de las distintas tablas dentro del informe
    count=0
    for i in Tabla_Revisar[0]:
        if i==codigo_colegio:
            count+=1
    if count==round(float(cantidad_en_tabla_resumen),1):
            return (f"Cantidad de {Nombre_Elemento} <font color=green><b>coinciden</b></font> con la tabla resumen. Esta es de <b>{cantidad_en_tabla_resumen}</b>.<br>")
    else:
        return (f"Cantidad de {Nombre_Elemento} <font color=red><b>no coinciden</b></font> con la tabla resumen. En el resumen son <b>{cantidad_en_tabla_resumen}</b> y se contaron <b>{count}</b>.<br>")

def Contador_de_Tramos_de_Canalizacion(tipo_canalizacion,cantidad_en_tabla_resumen,metros_tabla_resumen,Tabla_Revisar,Nombre_Elemento):#De la tabla de tramos, cuenta la cantidad de tramos que son de distintas canalizaciones
    count=0
    a=[]
    metros=0
    tramos=[]
    for i in range(len(Tabla_Revisar[0])):
        if Tabla_Revisar[0][i]==tipo_canalizacion:
            count+=1
            if Tabla_Revisar[0][i-5]=="Hormigón < " or Tabla_Revisar[0][i-5]=="Hormigón > ":
                a.append(round(float(Tabla_Revisar[0][i-6].replace(',','.')),1))
            else:
                a.append(round(float(Tabla_Revisar[0][i-5].replace(',','.')),1))
    for i in a:
        metros+=round(float(i),1)
    if count==round(float(cantidad_en_tabla_resumen),1) and metros==round(float(metros_tabla_resumen.replace(',','.')),1):
        return (f"Cantidad de <b>{Nombre_Elemento}</b> y metros <font color=green><b>coinciden</b></font> con la tabla resumen y los metros tambien. Estos son: <b>{cantidad_en_tabla_resumen}</b> y <b>{metros_tabla_resumen}</b>.")
    elif count==round(float(cantidad_en_tabla_resumen),1) and metros!=round(float(metros_tabla_resumen.replace(',','.')),1):
        return (f"Cantidad de <b>{Nombre_Elemento}</b> es <font color=green><b>correcta</b></font> pero los metros <font color=red><b>no coinciden</b></font>. La cantidad es: <b>{cantidad_en_tabla_resumen}</b> y metros son <b>{metros}</b>.")
    elif count!=round(float(cantidad_en_tabla_resumen),1) and metros==round(float(metros_tabla_resumen.replace(',','.')),1):
        return (f"Cantidad de <b>{Nombre_Elemento}</b> es <font color=red><b>incorrecta</b></font> pero los metros <font color=green><b>coinciden</b></font>. La cantidad es: <b>{count}</b> y los metros son: <b>{metros_tabla_resumen}</b>.")
    else:
        return (f"Cantidad de <b>{Nombre_Elemento}</b> y metros <font color=red><b>no coinciden</b></font> con la tabla resumen. Segun el texto son: <b>{count}</b> y <b>{metros}</b> metros.")
     
def Generar_Tabla_Resumen_Cables_Tramos(Tramos_Proyectados,codigo_colegio):#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
    resumen=[]
    materialidad=["Pasillo","Vertical","Exterior","Entretecho","Aereo","Soterrado"]#las distintas posibilidades de este campo en la tabla
    for i in range(len(Tramos_Proyectados[0])):
        if Tramos_Proyectados[0][i]==codigo_colegio:
            for v in materialidad:
                if v ==Tramos_Proyectados[0][i+4]:
                    if "Hormigón < "==Tramos_Proyectados[0][i+6] or "Hormigón > "==Tramos_Proyectados[0][i+6]:
                        resumen.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+8],Tramos_Proyectados[0][i+9]])
                        break
                    else:
                        resumen.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+7],Tramos_Proyectados[0][i+8]])
                        break
            else:
                if "Hormigón < "==Tramos_Proyectados[0][i+7] or "Hormigón > "==Tramos_Proyectados[0][i+7]:
                    resumen.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+9],Tramos_Proyectados[0][i+10]])
                else:
                    resumen.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+8],Tramos_Proyectados[0][i+9]])
    return resumen

def Generar_Tabla_Resumen_Cables_Puntos(Puntos_Proyectados,codigo_colegio):#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
    resumen=[]
    materialidad=["Tabique","Fierro","Ladrillo","Hormigón < ","Hormigón > ","Ninguna"]
    for i in range(len(Puntos_Proyectados[0])):
        if Puntos_Proyectados[0][i]==codigo_colegio:
            for v in materialidad:
                if v ==Puntos_Proyectados[0][i+7]:
                    if "Hormigón < "==Puntos_Proyectados[0][i+7] or "Hormigón > "==Puntos_Proyectados[0][i+7] :
                        if Puntos_Proyectados[0][i+12]=="20cm":
                            resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
                            break
                        else:
                            resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])
                            break
                    else:
                        if Puntos_Proyectados[0][i+11]=="20cm":
                            
                            resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+12]])
                            break
                        else:
                            
                            resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
                            break
            else:
                if "Hormigón < "==Puntos_Proyectados[0][i+8] or "Hormigón > "==Puntos_Proyectados[0][i+8] :
                    
                    resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12],Puntos_Proyectados[0][i+13]])
                elif Puntos_Proyectados[0][i+11]=="20cm":
                
                    resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+8],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10]])
                
                elif Puntos_Proyectados[0][i+9]=="100 cm (+-10)":
                
                    resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])
                elif Puntos_Proyectados[0][i+8] in b :
                    resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])   
                else:
                    
                    resumen.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
    return resumen

def Generar_Tabla_Resumen_Cables_Fibra(Rack_proyectados,codigo_colegio):#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
    resumen=[]
    materialidad=["Tabique","Fierro","Ladrillo","Hormigón < ","Hormigón > ","Ninguna","Cielo (wifi)","Hormigón <","Hormigón >"]
    for i in range(len(Rack_proyectados[0])):
        if Rack_proyectados[0][i]==codigo_colegio:
            for v in materialidad: 
                if v ==Rack_proyectados[0][i+8]:
                    if "Hormigón < "==Rack_proyectados[0][i+8] or "Hormigón > "==Rack_proyectados[0][i+8] :   
                        resumen.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+6],Rack_proyectados[0][i+7],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12]])
                        break
                    else:
                        resumen.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+6],Rack_proyectados[0][i+7],Rack_proyectados[0][i+9],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11]])
                        break
            else:
                if "Hormigón < "==Rack_proyectados[0][i+9] or "Hormigón > "==Rack_proyectados[0][i+9]:
                    resumen.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+7],Rack_proyectados[0][i+8],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12],Rack_proyectados[0][i+13]])
                else:
                    resumen.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+7],Rack_proyectados[0][i+8],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12]])

    return resumen
def Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,x):#Para calcular los metros de cable de los tramos, ya que estos se conectan en cadena.
    for j in range(len(tabla_resumen_cables_tramos)):    
        if tabla_resumen_cables_tramos[j][0]==tabla_resumen_cables_tramos[x][1]:
            revisar_total+=Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,j)
            revisar_total+=round(float(tabla_resumen_cables_tramos[j][2].replace(',','.')),1)

    return revisar_total
def Revisar_Total_de_metros(tabla_resumen,tabla_resumen_cables_tramos):#Revisa el total de metros de cable UTP-6 o Fibra
    revisar_total_suma=0
    estado=[]
    for i in range(len(tabla_resumen)):
        revisar_total=0
        for v in range(len(tabla_resumen_cables_tramos)):
            if tabla_resumen[i][1]==tabla_resumen_cables_tramos[v][0]:
                revisar_total+=Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,v)
                revisar_total+=round(float(tabla_resumen_cables_tramos[v][2].replace(',','.')),1)+round(float(tabla_resumen[i][2].replace(',','.')),1)+round(float(tabla_resumen[i][3].replace(',','.')),1)+round(float(tabla_resumen[i][4].replace(',','.')),1)
        revisar_total_suma+=revisar_total
        if revisar_total==round(float(tabla_resumen[i][5].replace(',','.')),1):
            estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=green><b> esta bien </b></font> {revisar_total} m")
        else: estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=red><b> no esta bien </b></font> {revisar_total} m")
    return (revisar_total_suma,estado)

#######################Objetos######################

class Datos_Texto_Informe:#Es donde se encuentra toda la data importante del informe
    def __init__(self,file):
        self.paginas=[13,43,44,45,46,47,48,49,50]#el numero de la pagina dentro del informe que posee la información importante
        self.pathfile=file
        

    def __del__(self):
        print("listo")

    def Ordenar_Datos(self):
        self.informe=[]
        doc= fitz.open(self.pathfile)
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

    def Informacion_de_las_Tablas(self):
        self.Actividad_asesoria=self.informe[:9]#Pagina que tiene la información de asesoria
        self.Elementos_red=self.informe[12:18]#Tabla resumen de elementos de red
        self.Tramos_canalización=self.informe[25:46]#Tabla resumen de tramos de canalización
        self.Cables=self.informe[49:53]#Tabla resumen de Cables
        self.Enlaces_existentes=Extraer_Datos_Tablas_Rango_Variable(self.informe,56)#Tabla resumen de Enlaces Existentes
        self.Rack_existentes=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Enlaces_existentes[1]+3)#Tabla resumen de Racks Existentes
        self.Rack_proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Rack_existentes[1]+3)#Tabla resumen de Racks Proyectados
        self.Puntos_Proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Rack_proyectados[1]+3)#Tabla resumen de Puntos Proyectados
        self.Tramos_Proyectados=Extraer_Datos_Tablas_Rango_Variable(self.informe,self.Puntos_Proyectados[1]+3)#Tabla resumen de Tramos Proyectados

    
    def Verificar_Elementos_de_Red_Existentes(self):#Verifica si los datos de elementos de red en la tabla resumen estan correctos
        #print("########Elementos de Red ############")
        self.codigo_colegio=self.informe[71]
        self.nombre_colegio=self.informe[55]
        #print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        self.cantidad_enlaces=self.Elementos_red[1]
        self.cantidad_racks_proyectados=self.Elementos_red[3]
        self.cantidad_puntos_proyectados=self.Elementos_red[5]
        cant_enlaces = Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_enlaces,self.Enlaces_existentes,"Enlaces")
        cant_racks = Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_racks_proyectados,self.Rack_proyectados,"Racks Proyectados")
        cant_puntos = Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_puntos_proyectados,self.Puntos_Proyectados,"Puntos Proyectados")
        return (f"Nombre es <b>{self.nombre_colegio}</b> <br>Codigo <b>{self.codigo_colegio}</b>.<br>  {cant_enlaces} {cant_racks} {cant_puntos}")
    def Verificar_Tramos_de_Canalizacion(self):#Verifica si los datos de tramos de canalización en la tabla resumen estan correctos
        #print("#######Tramos de Canalizacion#############")
        #print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        cantidad_tramos_canalizacion=[self.Tramos_canalización[1],self.Tramos_canalización[4],self.Tramos_canalización[7],self.Tramos_canalización[10],self.Tramos_canalización[13],self.Tramos_canalización[16],self.Tramos_canalización[19]]
        nombre_canalizacion=[self.Tramos_canalización[0],self.Tramos_canalización[3],self.Tramos_canalización[6],self.Tramos_canalización[9],self.Tramos_canalización[12],self.Tramos_canalización[15],self.Tramos_canalización[18]]
        tipo_canalizacion=["3/4\"","1\"","1 1/4\"","1 1/2\"","2\"","2 1/2\"","Escalerilla "]
        metros_canalizacion=[self.Tramos_canalización[2],self.Tramos_canalización[5],self.Tramos_canalización[8],self.Tramos_canalización[11],self.Tramos_canalización[14],self.Tramos_canalización[17],self.Tramos_canalización[20]]
        verificar=[]
        for i in range(len(tipo_canalizacion)):
            verificar.append(Contador_de_Tramos_de_Canalizacion(tipo_canalizacion[i],cantidad_tramos_canalizacion[i],metros_canalizacion[i],self.Tramos_Proyectados,nombre_canalizacion[i]))
        return verificar
    def Verificar_Metros_de_Cable(self):#Verifica si los datos de los metros de cable UTP-6 y Fibra en la tabla resumen estan correctos
        #print("#######Metros de Cables#############")
        tabla_resumen_cables_tramos = Generar_Tabla_Resumen_Cables_Tramos(self.Tramos_Proyectados,self.codigo_colegio)
        tabla_resumen_cables_puntos = Generar_Tabla_Resumen_Cables_Puntos(self.Puntos_Proyectados,self.codigo_colegio)
        tabla_resumen_cables_fibra = Generar_Tabla_Resumen_Cables_Fibra(self.Rack_proyectados,self.codigo_colegio)
        total_metros_fibra = Revisar_Total_de_metros(tabla_resumen_cables_fibra,tabla_resumen_cables_tramos)
        total_metros_puntos = Revisar_Total_de_metros(tabla_resumen_cables_puntos,tabla_resumen_cables_tramos)
        #print(f"El total de fibra es {total_metros_fibra} m")
        #print(f"El total de UTP-6 es {total_metros_puntos} m")
        return (f"El total de fibra es <b>{total_metros_fibra[0]}</b> m.<br> Los puntos de fibra son : <br> &nbsp; &nbsp;{total_metros_fibra[1]}. <br> El total de UTP-6 es <b>{total_metros_puntos[0]}</b> m. <br>Los puntos UTP-6 son: <br> &nbsp; &nbsp;{total_metros_puntos[1]}")

    def Detectar_caras(self,numero_pagina,file_name):#Numero de la pagina donde comienzan las fotos
        doc= fitz.open(self.pathfile)
        caras=[]
        image_path = f"static/tmp/images{file_name}"
        try:
            os.mkdir(image_path)
        except:
            pass
        app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))
        for page_index in range(numero_pagina,len(doc)):

            # get the page itself
            page = doc.load_page(page_index)
            image_list = page.get_images()
            # printing number of images found in this page
            #if image_list:
                #print(
                #f"[+] Found a total of {len(image_list)} images in page {page_index}")
            #else:
                #print("[!] No images found on page", page_index)

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
                
                image.save(open(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))
                
                #imagen = ins_get_image(f"{image_path}/image{page_index+1}_{image_index}")
                image = cv2.imread(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}")
                image_name = f"image{page_index+1}_{image_index}"
                faces = app.get(image)
                
                if len(faces) > 0: caras.append(f"Encontrada cara en <img src=\"/static/tmp/images{file_name}/image{page_index+1}_{image_index}.{image_ext}\"></img><b>{page_index+1}_{image_index}</b>")
                # save it to local disk
                #image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
                #remove_img(image_path, image_name)
                #image.save(open(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))
        return caras





###############Main###################



#f_list = filter(lambda f: f.endswith(('.pdf','.PDF')), f_list)#filtra la lista para que solo sean pdf}
 
#file_path=os.path.abspath("579InformeFinal.pdf")

#get_report(file_path)


#Extraer_Imagenes_del_Informe(Datos_del_Informe.file_path,Datos_del_Informe.nombre_archivo, 54) 

#Extraer_Imagenes_del_Informe(file_path,54)

