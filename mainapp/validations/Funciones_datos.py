from pathlib import Path
import os
import io
from PIL import Image 




#Se extrae los datos de tablas que no se conoce la cantidad de filas que posee en el informe
def tablas_rango_variable(datos_del_informe,comienzo):
    posicion_final = 0
    a = []
    for i in range(comienzo,len(datos_del_informe)):
        if datos_del_informe[i] == datos_del_informe[53]:#El codigo de el Colegio sea el mismo
            posicion_final = i
            break
        else:   
            a.append(datos_del_informe[i])
    return(a,posicion_final)

#Cuenta las filas de las distintas tablas dentro del informe
def contador_de_codigo_colegio(codigo_colegio,cantidad_en_tabla_resumen,tabla_revisar,nombre_elemento):
    count = 0
    for i in tabla_revisar[0]:
        if i == codigo_colegio:
            count += 1
    #Si lo que se muestra en la tabla resumen es igual a lo contado
    if count == round(float(cantidad_en_tabla_resumen),1):
            return (f"Cantidad de {nombre_elemento} <font color=green><b>coinciden</b></font> con la tabla resumen. Esta es de <b>{cantidad_en_tabla_resumen}</b>.<br>")
    else:
        return (f"Cantidad de {nombre_elemento} <font color=red><b>no coinciden</b></font> con la tabla resumen. En el resumen son <b>{cantidad_en_tabla_resumen}</b> y se contaron <b>{count}</b>.<br>")

#De la tabla de tramos, cuenta la cantidad de tramos que son de distintas canalizaciones
def contador_de_tramos_de_canalizacion(tipo_canalizacion,cantidad_en_tabla_resumen,metros_tabla_resumen,tabla_revisar,nombre_elemento):
    count = 0
    tramos = []
    metros = 0
    for i in range(len(tabla_revisar[0])):
        if tabla_revisar[0][i] == tipo_canalizacion:
            count += 1
            if (tabla_revisar[0][i-5] == "Hormigón < " 
                    or tabla_revisar[0][i-5] == "Hormigón > "):
                tramos.append(round(float(tabla_revisar[0][i-6].replace(',','.')),1))
            try:
                if (tabla_revisar[0][i+1]== "20cm"):
                    tramos.append(round(float(tabla_revisar[0][i-4].replace(',','.')),1))
            except:
                tramos.append(round(float(tabla_revisar[0][i-5].replace(',','.')),1))
            else:
                tramos.append(round(float(tabla_revisar[0][i-5].replace(',','.')),1))
    #Para los distintos tramos, si los metros de las tablas coinciden con la tabla resumen
    for i in tramos:
        metros += round(float(i),1)
    if (count == round(float(cantidad_en_tabla_resumen),1) 
            and metros == round(float(metros_tabla_resumen.replace(',','.')),1)):
        return (f"Cantidad de <b>{nombre_elemento}</b> y metros <font color=green><b>coinciden</b></font> con la tabla resumen. Estos son: <b>{cantidad_en_tabla_resumen}</b> y <b>{metros_tabla_resumen}</b>.")
    elif (count == round(float(cantidad_en_tabla_resumen),1) 
            and metros != round(float(metros_tabla_resumen.replace(',','.')),1)):
        return (f"Cantidad de <b>{nombre_elemento}</b> es <font color=green><b>correcta</b></font> pero los metros <font color=red><b>no coinciden</b></font>. La cantidad es: <b>{cantidad_en_tabla_resumen}</b> y metros son <b>{metros}</b>.")
    elif (count != round(float(cantidad_en_tabla_resumen),1) 
            and metros == round(float(metros_tabla_resumen.replace(',','.')),1)):
        return (f"Cantidad de <b>{nombre_elemento}</b> es <font color=red><b>incorrecta</b></font> pero los metros <font color=green><b>coinciden</b></font>. La cantidad es: <b>{count}</b> y los metros son: <b>{metros_tabla_resumen}</b>.")
    else:
        return (f"Cantidad de <b>{nombre_elemento}</b> y metros <font color=red><b>no coinciden</b></font> con la tabla resumen. Segun el texto son: <b>{count}</b> y <b>{metros}</b> metros.")
     
#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
def generar_tabla_resumen_cables_tramos(tramos_proyectados,codigo_colegio):
    resumen = []
    #las distintas posibilidades de este campo en la tabla
    TIPOCANALIZACION = [
        "Pasillo","Vertical","Exterior",
        "Entretecho","Aereo","Soterrado"
    ]
    for i in range(len(tramos_proyectados[0])):
        if tramos_proyectados[0][i] == codigo_colegio:
            for v in TIPOCANALIZACION:
                if v == tramos_proyectados[0][i+4]:
                    if ("Hormigón < "== tramos_proyectados[0][i+6] 
                            or "Hormigón > "== tramos_proyectados[0][i+6]):
                        resumen.append([
                            tramos_proyectados[0][i+1],
                            tramos_proyectados[0][i+8],
                            tramos_proyectados[0][i+9]
                        ])
                        break
                    else:
                        resumen.append([
                            tramos_proyectados[0][i+1],
                            tramos_proyectados[0][i+7],
                            tramos_proyectados[0][i+8]
                        ])
                        break
            else:
                if ("Hormigón < "==tramos_proyectados[0][i+7] 
                        or "Hormigón > "==tramos_proyectados[0][i+7]):
                    resumen.append([
                        tramos_proyectados[0][i+1],
                        tramos_proyectados[0][i+9],
                        tramos_proyectados[0][i+10]
                    ])
                else:
                    resumen.append([
                        tramos_proyectados[0][i+1],
                        tramos_proyectados[0][i+8],
                        tramos_proyectados[0][i+9]
                    ])
    return resumen

#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
def generar_tabla_resumen_cables_puntos(puntos_proyectados,codigo_colegio):
    resumen = []
    #las distintas posibilidades de este campo en la tabla
    MATERIALIDAD = [
        "Tabique","Fierro","Ladrillo",
        "Hormigón < ","Hormigón > ","Ninguna",
        "Vidrio"
    ]
    for i in range(len(puntos_proyectados[0])):
        if puntos_proyectados[0][i] == codigo_colegio:
            for v in MATERIALIDAD:
                if v == puntos_proyectados[0][i+7]:
                    if ("Hormigón < "== puntos_proyectados[0][i+7] 
                            or "Hormigón > "== puntos_proyectados[0][i+7]):
                        if (puntos_proyectados[0][i+12] =="20cm"
                                or puntos_proyectados[0][i+13] =="20cm"):
                            resumen.append([
                                puntos_proyectados[0][i+1],puntos_proyectados[0][i+5],
                                puntos_proyectados[0][i+6],puntos_proyectados[0][i+9],
                                puntos_proyectados[0][i+10],puntos_proyectados[0][i+11]
                            ])
                            break
                        else:
                            resumen.append([
                                puntos_proyectados[0][i+1],puntos_proyectados[0][i+5],
                                puntos_proyectados[0][i+6],puntos_proyectados[0][i+10],
                                puntos_proyectados[0][i+11],puntos_proyectados[0][i+12]
                            ])
                            break
                    else:
                        if puntos_proyectados[0][i+11] == "20cm":
                            
                            resumen.append([
                                puntos_proyectados[0][i+1],puntos_proyectados[0][i+5],
                                puntos_proyectados[0][i+6],puntos_proyectados[0][i+9],
                                puntos_proyectados[0][i+10],puntos_proyectados[0][i+12]
                            ])
                            break
                        else:
                            
                            resumen.append([
                                puntos_proyectados[0][i+1],puntos_proyectados[0][i+5],
                                puntos_proyectados[0][i+6],puntos_proyectados[0][i+9],
                                puntos_proyectados[0][i+10],puntos_proyectados[0][i+11]
                            ])
                            break
            else:
                if ("Hormigón < "== puntos_proyectados[0][i+8] 
                        or "Hormigón > "== puntos_proyectados[0][i+8]):
                    resumen.append([
                        puntos_proyectados[0][i+1],puntos_proyectados[0][i+6],
                        puntos_proyectados[0][i+7],puntos_proyectados[0][i+11],
                        puntos_proyectados[0][i+12],puntos_proyectados[0][i+13]
                    ])
                elif puntos_proyectados[0][i+11] == "20cm":
                
                    resumen.append([
                        puntos_proyectados[0][i+1],puntos_proyectados[0][i+5],
                        puntos_proyectados[0][i+6],puntos_proyectados[0][i+8],
                        puntos_proyectados[0][i+9],puntos_proyectados[0][i+10]
                        ])
                
                elif puntos_proyectados[0][i+9] == "100 cm (+-10)":
                
                    resumen.append([
                        puntos_proyectados[0][i+1],puntos_proyectados[0][i+6],
                        puntos_proyectados[0][i+7],puntos_proyectados[0][i+10],
                        puntos_proyectados[0][i+11],puntos_proyectados[0][i+12]
                    ])
                elif puntos_proyectados[0][i+8] in MATERIALIDAD :
                    resumen.append([
                    puntos_proyectados[0][i+1],puntos_proyectados[0][i+6],
                    puntos_proyectados[0][i+7],puntos_proyectados[0][i+10],
                    puntos_proyectados[0][i+11],puntos_proyectados[0][i+12]
                ])   
                else:
                    
                    resumen.append([
                        puntos_proyectados[0][i+1],puntos_proyectados[0][i+6],
                        puntos_proyectados[0][i+7],puntos_proyectados[0][i+9],
                        puntos_proyectados[0][i+10],puntos_proyectados[0][i+11]
                    ])
    return resumen

#Para facilitar la revision de las tablas, se resume la tabla en un arreglo mas pequeño.
def generar_tabla_resumen_cables_fibra(rack_proyectados,codigo_colegio):
    resumen = []
    #las distintas posibilidades de este campo en la tabla
    MATERIALIDAD = [
        "Tabique","Fierro","Ladrillo",
        "Hormigón < ","Hormigón > ","Ninguna",
        "Cielo (wifi)","Hormigón <","Hormigón >",
        "Vidrio"
    ]
    for i in range(len(rack_proyectados[0])):
        if rack_proyectados[0][i] == codigo_colegio:
            for v in MATERIALIDAD: 
                if v == rack_proyectados[0][i+8]:
                    if ("Hormigón < "== rack_proyectados[0][i+8] 
                            or "Hormigón > "== rack_proyectados[0][i+8]):   
                        resumen.append([
                            rack_proyectados[0][i+1],rack_proyectados[0][i+6],
                            rack_proyectados[0][i+7],rack_proyectados[0][i+10],
                            rack_proyectados[0][i+11],rack_proyectados[0][i+12]
                        ])
                        break
                    else:
                        resumen.append([
                            rack_proyectados[0][i+1],rack_proyectados[0][i+6],
                            rack_proyectados[0][i+7],rack_proyectados[0][i+9],
                            rack_proyectados[0][i+10],rack_proyectados[0][i+11]
                        ])
                        break
            else:
                if ("Hormigón < "== rack_proyectados[0][i+9] 
                        or "Hormigón > "== rack_proyectados[0][i+9]):
                    resumen.append([
                        rack_proyectados[0][i+1],rack_proyectados[0][i+7],
                        rack_proyectados[0][i+8],rack_proyectados[0][i+11],
                        rack_proyectados[0][i+12],rack_proyectados[0][i+13]
                    ])
                else:
                    resumen.append([
                        rack_proyectados[0][i+1],rack_proyectados[0][i+7],
                        rack_proyectados[0][i+8],rack_proyectados[0][i+10],
                        rack_proyectados[0][i+11],rack_proyectados[0][i+12]
                    ])

    return resumen

#Para calcular los metros de cable de los tramos, ya que estos se conectan en cadena.
def tramos_recursivos(tabla_resumen_cables_tramos,revisar_total,x):
    for j in range(len(tabla_resumen_cables_tramos)):    
        if tabla_resumen_cables_tramos[j][0] == tabla_resumen_cables_tramos[x][1]:
            revisar_total += tramos_recursivos(tabla_resumen_cables_tramos,revisar_total,j)
            revisar_total += round(float(tabla_resumen_cables_tramos[j][2].replace(',','.')),1)

    return revisar_total

#Revisa el total de metros de cable UTP-6 o Fibra
def revisar_total_de_metros(tabla_resumen,tabla_resumen_cables_tramos):
    revisar_total_suma = 0
    estado = []
    for i in range(len(tabla_resumen)):
        revisar_total = 0
        for v in range(len(tabla_resumen_cables_tramos)):
            if tabla_resumen[i][1] == tabla_resumen_cables_tramos[v][0]:
                revisar_total += tramos_recursivos(tabla_resumen_cables_tramos,revisar_total,v)
                revisar_total += (
                    round(float(tabla_resumen_cables_tramos[v][2].replace(',','.')),1)+
                    round(float(tabla_resumen[i][2].replace(',','.')),1) +
                    round(float(tabla_resumen[i][3].replace(',','.')),1) +
                    round(float(tabla_resumen[i][4].replace(',','.')),1)
                )
        revisar_total_suma += revisar_total
        if revisar_total == round(float(tabla_resumen[i][5].replace(',','.')),1):
            if (revisar_total + 2.1 + 0.9 > 90 
                    and revisar_total + 2.1 + 0.9 <= 100):
                estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=blue><b> esta bien </b></font> {revisar_total} m")
            elif (revisar_total + 2.1 + 0.9 > 100):
                estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=orange><b> esta bien </b></font> {revisar_total} m")
            else: 
                estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=green><b> esta bien </b></font> {revisar_total} m")
        else: estado.append(f"<b>{tabla_resumen[i][0].replace(',','.')}</b> <font color=red><b> no esta bien </b></font> {revisar_total} m")
    return (revisar_total_suma,estado)


def string_to_int(palabra):
        try:
            return int(palabra)
        except:
            return 0

