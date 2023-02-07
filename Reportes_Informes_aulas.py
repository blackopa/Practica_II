import fitz
from pathlib import Path
import os
import io
from PIL import Image

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
    if count==float(cantidad_en_tabla_resumen):
        return print(f"La cantidad de {Nombre_Elemento} coincide con la tabla resumen. Esta es de {cantidad_en_tabla_resumen}")
    else:
        return print(f"La cantidad de {Nombre_Elemento} no coincide con la tabla resumen. En el resumen son {cantidad_en_tabla_resumen} y se contaron {count}")

def Contador_de_Tramos_de_Canalizacion(tipo_canalizacion,cantidad_en_tabla_resumen,metros_tabla_resumen,Tabla_Revisar,Nombre_Elemento):
    count=0
    a=[]
    metros=0

    for i in range(len(Tabla_Revisar[0])):
        if Tabla_Revisar[0][i]==tipo_canalizacion:
            count+=1
            if Tabla_Revisar[0][i-5]=="Hormigón < " or Tabla_Revisar[0][i-5]=="Hormigón > ":
                a.append(float(Tabla_Revisar[0][i-6].replace(',','.')))
            else:
                a.append(float(Tabla_Revisar[0][i-5].replace(',','.')))
    for i in a:
        metros+=float(i)
    if count==float(cantidad_en_tabla_resumen) and metros==float(metros_tabla_resumen.replace(',','.')):
        return print(f"La cantidad de {Nombre_Elemento} y metros coinciden con la tabla resumen y los metros tambien. Estos son: {cantidad_en_tabla_resumen} y {metros_tabla_resumen}")
    elif count==float(cantidad_en_tabla_resumen) and metros!=float(metros_tabla_resumen.replace(',','.')):
        return print(f"La cantidad de {Nombre_Elemento} es correcta pero los metros no coinciden. La cantidad es: {cantidad_en_tabla_resumen}")
    elif count!=float(cantidad_en_tabla_resumen) and metros==float(metros_tabla_resumen.replace(',','.')):
        return print(f"La cantidad de {Nombre_Elemento} es incorrecta pero los metros coinciden. Los metros son: {metros_tabla_resumen}")
    else:
        return print(f"La cantidad de {Nombre_Elemento} y metros no coinciden con la tabla resumen. Segun el texto son: {count} y {metros} metros")

def Generar_Tabla_Resumen_Cables_Tramos(Tramos_Proyectados,codigo_colegio):
    a=[]
    b=["Pasillo","Vertical","Exterior","Entretecho","Aereo","Soterrado"]
    for i in range(len(Tramos_Proyectados[0])):
        if Tramos_Proyectados[0][i]==codigo_colegio:
            for v in b:
                if v ==Tramos_Proyectados[0][i+4]:
                    if "Hormigón < "==Tramos_Proyectados[0][i+6] or "Hormigón > "==Tramos_Proyectados[0][i+6]:
                        a.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+8],Tramos_Proyectados[0][i+9]])
                        break
                    else:
                        a.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+7],Tramos_Proyectados[0][i+8]])
                        break
            else:
                if "Hormigón < "==Tramos_Proyectados[0][i+7] or "Hormigón > "==Tramos_Proyectados[0][i+7]:
                    a.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+9],Tramos_Proyectados[0][i+10]])
                else:
                    a.append([Tramos_Proyectados[0][i+1],Tramos_Proyectados[0][i+8],Tramos_Proyectados[0][i+9]])
    return a

def Generar_Tabla_Resumen_Cables_Puntos(Puntos_Proyectados,codigo_colegio):
    a=[]
    b=["Tabique","Fierro","Ladrillo","Hormigón < ","Hormigón > ","Ninguna"]
    for i in range(len(Puntos_Proyectados[0])):
        if Puntos_Proyectados[0][i]==codigo_colegio:
            for v in b:
                if v ==Puntos_Proyectados[0][i+7]:
                    if "Hormigón < "==Puntos_Proyectados[0][i+7] or "Hormigón > "==Puntos_Proyectados[0][i+7] :
                        if Puntos_Proyectados[0][i+12]=="20cm":
                            a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
                            break
                        else:
                            a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])
                            break
                    else:
                        if Puntos_Proyectados[0][i+11]=="20cm":
                           
                            a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+12]])
                            break
                        else:
                           
                            a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
                            break
            else:
                if "Hormigón < "==Puntos_Proyectados[0][i+8] or "Hormigón > "==Puntos_Proyectados[0][i+8] :
                 
                    a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12],Puntos_Proyectados[0][i+13]])
                elif Puntos_Proyectados[0][i+11]=="20cm":
              
                    a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+5],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+8],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10]])
                
                elif Puntos_Proyectados[0][i+9]=="100 cm (+-10)":
              
                    a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])
                elif Puntos_Proyectados[0][i+8] in b :
                    a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11],Puntos_Proyectados[0][i+12]])   
                else:
                   
                    a.append([Puntos_Proyectados[0][i+1],Puntos_Proyectados[0][i+6],Puntos_Proyectados[0][i+7],Puntos_Proyectados[0][i+9],Puntos_Proyectados[0][i+10],Puntos_Proyectados[0][i+11]])
    return a

def Generar_Tabla_Resumen_Cables_Fibra(Rack_proyectados,codigo_colegio):
    a=[]
    b=["Tabique","Fierro","Ladrillo","Hormigón < ","Hormigón > ","Ninguna","Cielo (wifi)","Hormigón <","Hormigón >"]
    for i in range(len(Rack_proyectados[0])):
        if Rack_proyectados[0][i]==codigo_colegio:
            for v in b: 
                if v ==Rack_proyectados[0][i+8]:
                    if "Hormigón < "==Rack_proyectados[0][i+8] or "Hormigón > "==Rack_proyectados[0][i+8] :   
                        a.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+6],Rack_proyectados[0][i+7],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12]])
                        break
                    else:
                        a.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+6],Rack_proyectados[0][i+7],Rack_proyectados[0][i+9],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11]])
                        break
            else:
                if "Hormigón < "==Rack_proyectados[0][i+9] or "Hormigón > "==Rack_proyectados[0][i+9]:
                    a.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+7],Rack_proyectados[0][i+8],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12],Rack_proyectados[0][i+13]])
                else:
                    a.append([Rack_proyectados[0][i+1],Rack_proyectados[0][i+7],Rack_proyectados[0][i+8],Rack_proyectados[0][i+10],Rack_proyectados[0][i+11],Rack_proyectados[0][i+12]])

    return a
def Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,x):
    for j in range(len(tabla_resumen_cables_tramos)):    
        if tabla_resumen_cables_tramos[j][0]==tabla_resumen_cables_tramos[x][1]:
            revisar_total+=Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,j)
            revisar_total+=float(tabla_resumen_cables_tramos[j][2].replace(',','.'))
            
    return revisar_total
def Revisar_Total_de_metros(tabla_resumen,tabla_resumen_cables_tramos):
    revisar_total_suma=0
    for i in range(len(tabla_resumen)):
            revisar_total=0
            for v in range(len(tabla_resumen_cables_tramos)):
                if tabla_resumen[i][1]==tabla_resumen_cables_tramos[v][0]:
                    revisar_total+=Tramos_Recursivos(tabla_resumen_cables_tramos,revisar_total,v)
                    revisar_total+=float(tabla_resumen_cables_tramos[v][2].replace(',','.'))+float(tabla_resumen[i][2].replace(',','.'))+float(tabla_resumen[i][3].replace(',','.'))+float(tabla_resumen[i][4].replace(',','.'))
            revisar_total_suma+=revisar_total
            if revisar_total==float(tabla_resumen[i][5].replace(',','.')):
                print(f"{tabla_resumen[i][0].replace(',','.')} ok {revisar_total} m")
            else: print(f"{tabla_resumen[i][0].replace(',','.')} not ok {revisar_total} m")
    return revisar_total_suma

#######################Objetos######################

class Datos_Texto_Informe:#Es donde se encuentra toda la data importante del informe
    def __init__(self,i,f_list):
        self.paginas=[13,43,44,45,46,47,48,49,50]#el numero de la pagina dentro del informe que posee la información importante
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

    def Verificar_Elementos_de_Red_Existentes(self):
        print("########Elementos de Red ############")
        self.codigo_colegio=self.informe[71]
        self.nombre_colegio=self.informe[55]
        print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        self.cantidad_enlaces=self.Elementos_red[1]
        self.cantidad_racks_proyectados=self.Elementos_red[3]
        self.cantidad_puntos_proyectados=self.Elementos_red[5]
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_enlaces,self.Enlaces_existentes,"Enlaces")
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_racks_proyectados,self.Rack_proyectados,"Racks Proyectados")
        Contador_de_Codigo_Colegio(self.codigo_colegio,self.cantidad_puntos_proyectados,self.Puntos_Proyectados,"Puntos Proyectados")
    
    def Verificar_Tramos_de_Canalizacion(self):
        print("#######Tramos de Canalizacion#############")
        print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        cantidad_tramos_canalizacion=[self.Tramos_canalización[1],self.Tramos_canalización[4],self.Tramos_canalización[7],self.Tramos_canalización[10],self.Tramos_canalización[13],self.Tramos_canalización[16],self.Tramos_canalización[19]]
        nombre_canalizacion=[self.Tramos_canalización[0],self.Tramos_canalización[3],self.Tramos_canalización[6],self.Tramos_canalización[9],self.Tramos_canalización[12],self.Tramos_canalización[15],self.Tramos_canalización[18]]
        tipo_canalizacion=["3/4\"","1\"","1 1/4\"","1 1/2\"","2\"","2 1/2\"","Escalerilla "]
        metros_canalizacion=[self.Tramos_canalización[2],self.Tramos_canalización[5],self.Tramos_canalización[8],self.Tramos_canalización[11],self.Tramos_canalización[14],self.Tramos_canalización[17],self.Tramos_canalización[20]]
        for i in range(len(tipo_canalizacion)):
            Contador_de_Tramos_de_Canalizacion(tipo_canalizacion[i],cantidad_tramos_canalizacion[i],metros_canalizacion[i],self.Tramos_Proyectados,nombre_canalizacion[i])
    
    def Verificar_Metros_de_Cable(self):
        print("#######Metros de Cables#############")
        tabla_resumen_cables_tramos = Generar_Tabla_Resumen_Cables_Tramos(self.Tramos_Proyectados,self.codigo_colegio)
        tabla_resumen_cables_puntos = Generar_Tabla_Resumen_Cables_Puntos(self.Puntos_Proyectados,self.codigo_colegio)
        tabla_resumen_cables_fibra = Generar_Tabla_Resumen_Cables_Fibra(self.Rack_proyectados,self.codigo_colegio)
        total_metros_fibra = Revisar_Total_de_metros(tabla_resumen_cables_fibra,tabla_resumen_cables_tramos)
        total_metros_puntos = Revisar_Total_de_metros(tabla_resumen_cables_puntos,tabla_resumen_cables_tramos)
        print(f"El total de fibra es {total_metros_fibra} m")
        print(f"El total de UTP-6 es {total_metros_puntos} m")
        


class Reporte:
    def __init__(self,codigo_colegio,nombre_colegio):#agregar mas campos para el reporte
        self.codigo_colegio=codigo_colegio
        self.nombre_colegio=nombre_colegio
        


###############Main###################

path="./InformesPdf/Diciembre_adelante"#La ruta a donde estan los archivos, idealmente en la misma carpeta base donde esta este codigo
f_list = os.listdir(path)#lista de archivos en esa carpeta

#f_list = filter(lambda f: f.endswith(('.pdf','.PDF')), f_list)#filtra la lista para que solo sean pdf}
#file_path="./InformesPdf/Diciembre_adelante/%s"%(f_list[1])

for i in range(len(f_list)): #Esto revisa Informe po Informe dentro de la carpeta
    Texto_Informe=Datos_Texto_Informe(i,f_list)
    Texto_Informe.Ordenar_Datos()
    Texto_Informe.Informacion_de_las_Tablas()
    Texto_Informe.Verificar_Elementos_de_Red_Existentes()
    Texto_Informe.Verificar_Tramos_de_Canalizacion()
    Texto_Informe.Verificar_Metros_de_Cable()
    del Texto_Informe

#Extraer_Imagenes_del_Informe(Datos_del_Informe.file_path,Datos_del_Informe.nombre_archivo, 54) 

#Extraer_Imagenes_del_Informe(file_path,54)
