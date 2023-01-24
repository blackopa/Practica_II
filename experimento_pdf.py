import PyPDF2
import re

def contador_de_palabras(file_name: str,search: str):    
    doc = PyPDF2.PdfReader(file_name)
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

#elegir archivo
file_name = "RBD 25198 - INFORME FINAL FASE 1 - ASESORÍA DISEÑO DE RED - AULAS CONECTADAS 2022.pdf"
#Buscar un termino
search = 'RESUMEN'
result= contador_de_palabras(file_name,search)
print(f"la palabra '{search}' fuen encontrada un total de {result[0]} veces en {result[1]} paginas.")