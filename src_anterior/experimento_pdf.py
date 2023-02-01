from PyPDF2 import PdfReader
import re

def contador_de_palabras(file_name: str,search: str):    
    doc = PdfReader(file_name)
    #Numero de paginas
    pages = len(doc.pages)
    #lista de tuplas (ocurrencias, numero de pagina)
    list_pages = []
    for i in range(pages):
        current_page = doc.pages[i]
        text = current_page.extract_text()
        if re.findall(search, text):
            count_page= len(re.findall(search, text))
            list_pages.append((count_page,i+1))
    #Resultado
    print(list_pages)
    #Numero de paginas que contiene la palabra buscada al menos una vez
    count= len(list_pages)
    #total de palabras contadas 
    total = sum([tup[0] for tup in list_pages])
    return(total,count)  
def contador_imagenes(file_name:str):
    reader = PdfReader(file_name)
    page = reader.pages[0]
    count = 0

    for image_file_object in page.images:
        with open(str(count) + image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1
    return count
#elegir archivo
file_name = "informeFinal5393.pdf"
#Buscar un termino
search = 'RESUMEN'
result= contador_de_palabras(file_name,search)
cont_im= contador_imagenes(file_name)
print(f"la palabra '{search}' fuen encontrada un total de {result[0]} veces en {result[1]} paginas.")
#print(f"La cantidad de imagenes son {cont_im}")