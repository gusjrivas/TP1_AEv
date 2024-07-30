####################################################################
# CEIA - 16Co2024 - Algoritmos Evolutivos - TP1 - Ejercicio 3
# Gustavo J. Rivas (a1620) | Myrna L. Degano (a1618)
####################################################################
# Algoritmo genético con representación de individuos binarios
# y operador de selección por torneo
####################################################################

import numpy as np
import matplotlib.pyplot as plt
import random
from tabulate import tabulate

#############################################
# Parámetros del algoritmo genético
#############################################

print("\nSELECCIÓN POR TORNEO")
PROB_CRUCE = 0.85
PROB_MUTACION = 0.07
print("Probabilidad de cruce: " + str(PROB_CRUCE))
print("Probabilidad de mutación: " + str(PROB_MUTACION))

print("\nINGRESE LOS PARÁMETROS PARA LA EJECUCIÓN DEL ALGORITMO (O <ENTER> PARA TOMAR LOS VALORES POR DEFAULT)\n")

TAMANIO_POBLACION = input("TAMAÑO DE LA POBLACIÓN (DEFAULT: 50): ").strip()
TAMANIO_POBLACION = int(TAMANIO_POBLACION) if TAMANIO_POBLACION else 50

NUM_GENERACIONES = input("CANTIDAD DE GENERACIONES (DEFAULT: 100): ").strip()
NUM_GENERACIONES = int(NUM_GENERACIONES) if NUM_GENERACIONES else 100

CANDIDATOS = input("CANTIDAD DE CANDIDATOS A SELECCIONAR POR ITERACIÓN (DEFAULT: 3): ").strip()
CANDIDATOS = int(CANDIDATOS) if CANDIDATOS else 3

LIMITE_INF_c = 0.00
LIMITE_SUP_c = 10.00
# g(c) con c en el intervalo [0, 10]
# Precisión de 2 decimales
# Rango de c = 10.00 => 1000 => 2**9 < 1000 < 2**10
# Longitud necesaria del cromosoma = 10 bits
LONGITUD_CROMOSOMA = 10

############################################################################
# Definición de la función de objetivo (A maximizar) = función de aptitud
############################################################################
def funcion_g(c):
    return 2 * c / (4 + 0.8 * c + c**2 + 0.2 * c**3)

#####################################################################################
# Función para inicializar la población
# La función inicializar_poblacion genera una lista de individuos binarios aleatorios.
#####################################################################################
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma):
    poblacion = []
    for _ in range(tamanio_poblacion):
        cromosoma = ''.join(random.choice('01') for _ in range(longitud_cromosoma))
        poblacion.append(cromosoma)
    return poblacion

######################################################################################################
# Función para decodificar un cromosoma
# La función decodificar_cromosoma convierte un cromosoma binario en un valor real en el rango [0, 10].
#######################################################################################################
def decodificar_cromosoma(cromosoma):
    return LIMITE_INF_c + int(cromosoma, 2) * (LIMITE_SUP_c - LIMITE_INF_c)/ (2 ** LONGITUD_CROMOSOMA - 1)

###################################################################################################
# Función para evaluar la población
# La función evaluar_poblacion calcula la aptitud de un individuo utilizando la función funcion_g.
##################################################################################################
def evaluar_poblacion(poblacion):
    aptitudes = []
    for cromosoma in poblacion:
        c = decodificar_cromosoma(cromosoma)
        aptitudes.append(funcion_g(c))
    return aptitudes


################################################################################################
# Función para selección por torneo
# La función seleccion_torneo selecciona individuos para el cruce mediante el método de torneo.
################################################################################################
def seleccion_torneo(poblacion, aptitudes, k=CANDIDATOS):
    seleccionados = []
    for _ in range(len(poblacion)):
        aspirantes = random.sample(list(zip(poblacion, aptitudes)), k)
        seleccionados.append(max(aspirantes, key=lambda x: x[1])[0])
    return seleccionados

##########################################################################################
# Función para cruce
# La función cruce realiza el cruce entre dos individuos con una probabilidad pc de 0.85.
##########################################################################################
def cruce(padre1, padre2):
    if random.random() < PROB_CRUCE:
        punto_cruce = random.randint(1, LONGITUD_CROMOSOMA - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2
    return padre1, padre2


##########################################################################
# Función para mutación
# La función mutacion muta los individuos con una probabilidad pm de 0.07.
##########################################################################

def mutacion(cromosoma):
    cromosoma_mutado = ''.join(
        bit if random.random() > PROB_MUTACION else '1' if bit == '0' else '0'
        for bit in cromosoma
    )
    return cromosoma_mutado


################################################
# Algoritmo genético
################################################
def algoritmo_genetico():
    poblacion = inicializar_poblacion(TAMANIO_POBLACION, LONGITUD_CROMOSOMA)
    mejores_aptitudes = []
    resultados = []

    for generacion in range(NUM_GENERACIONES):
        aptitudes = evaluar_poblacion(poblacion)
        mejor_aptitud = max(aptitudes)
        mejor_indice = np.argmax(aptitudes)
        mejores_aptitudes.append(mejor_aptitud)

        seleccionados = seleccion_torneo(poblacion, aptitudes)
        nueva_poblacion = []

        for i in range(0, len(seleccionados), 2):
            padre1 = seleccionados[i]
            padre2 = seleccionados[i + 1 if i + 1 < len(seleccionados) else 0]
            hijo1, hijo2 = cruce(padre1, padre2)
            nueva_poblacion.append(mutacion(hijo1))
            nueva_poblacion.append(mutacion(hijo2))

        resultados.append([generacion + 1, round(mejor_aptitud, 2), poblacion[mejor_indice], round(decodificar_cromosoma(poblacion[mejor_indice]), 2)])

        poblacion = nueva_poblacion[:TAMANIO_POBLACION]

    aptitudes = evaluar_poblacion(poblacion)
    mejor_indice = np.argmax(aptitudes)
    mejor_c = decodificar_cromosoma(poblacion[mejor_indice])

    headers = ["Generación #", "Mejor Aptitud", "Mejor individuo", "Fenotipo"]
    print(tabulate(resultados, headers=headers, tablefmt="grid"))

    return mejor_c, mejores_aptitudes


# Ejecución del algoritmo
mejor_c, mejores_aptitudes = algoritmo_genetico()

mejor_c = round(mejor_c, 2)
mejor_g = round(funcion_g(mejor_c), 2)

print(f"El valor aproximado de c que maximiza g es: {mejor_c}")

#############################################################
# Gráficos
##############################################################

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Graficar g en función de c

c_values = np.linspace(-1, 20, 400)
g_values = funcion_g(c_values)

ax1.plot(c_values, g_values, label='Función de crecimiento g(c)')
ax1.scatter([mejor_c], [funcion_g(mejor_c)], color='red', zorder=5)
ax1.set_title('Función de crecimiento g(c) y máximo encontrado')
ax1.set_xlabel('Nivel de concentración del alimento c')
ax1.set_ylabel('Crecimiento g')
label_text = f'Máximo encontrado\ng({mejor_c})={mejor_g}'
ax1.legend([label_text])
ax1.grid(True)


# Graficar mejores aptitudes en función de cada generación
ax2.plot(range(NUM_GENERACIONES), mejores_aptitudes, label='Mejor aptitud por generación')
ax2.set_title('Mejor aptitud encontrada por generación')
ax2.set_xlabel('Generación')
ax2.set_ylabel('Mejor aptitud')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
