import numpy as np
import matplotlib.pyplot as plt
import random
##############################################
# Definición de la función de aptitud
##############################################

def funcion_g(c):
    return 2 * c / (4 + 0.8 * c + c**2 + 0.2 * c**3)


#############################################
# Parámetros del algoritmo genético
#############################################

TAMANIO_POBLACION = 50
LONGITUD_CROMOSOMA = 10  # precisión de 2 decimales -> 10 bits
NUM_GENERACIONES = 100
PROB_CRUCE = 0.85
PROB_MUTACION = 0.07
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
    return int(cromosoma, 2) / (2**LONGITUD_CROMOSOMA - 1) * 10

###################################################################################################
# Función para evaluar la población
#La función evaluar_poblacion calcula la aptitud de un individuo utilizando la función funcion_g.
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

def seleccion_torneo(poblacion, aptitudes, k=3):
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

    for _ in range(NUM_GENERACIONES):
        aptitudes = evaluar_poblacion(poblacion)
        mejores_aptitudes.append(max(aptitudes))
        
        seleccionados = seleccion_torneo(poblacion, aptitudes)
        nueva_poblacion = []
        
        for i in range(0, len(seleccionados), 2):
            padre1 = seleccionados[i]
            padre2 = seleccionados[i + 1 if i + 1 < len(seleccionados) else 0]
            hijo1, hijo2 = cruce(padre1, padre2)
            nueva_poblacion.append(mutacion(hijo1))
            nueva_poblacion.append(mutacion(hijo2))
        
        poblacion = nueva_poblacion[:TAMANIO_POBLACION]
    
    aptitudes = evaluar_poblacion(poblacion)
    mejor_indice = np.argmax(aptitudes)
    mejor_c = decodificar_cromosoma(poblacion[mejor_indice])
    return mejor_c, mejores_aptitudes

# Ejecución del algoritmo
mejor_c, mejores_aptitudes = algoritmo_genetico()
print(f"El valor de c que maximiza g es: {mejor_c:.2f}")

#############################################################
# Graficar g en función de c
##############################################################

c_values = np.linspace(-1, 20, 400)
g_values = funcion_g(c_values)

plt.figure(figsize=(10, 5))
plt.plot(c_values, g_values, label='Función de crecimiento g(c)')
plt.scatter([mejor_c], [funcion_g(mejor_c)], color='red', zorder=5)
plt.title('Función de crecimiento g(c) y máximo encontrado')
plt.xlabel('Nivel de concentración del alimento c')
plt.ylabel('Crecimiento g')
plt.legend()
plt.grid(True)
plt.show()

# Graficar mejores aptitudes en función de cada generación
plt.figure(figsize=(10, 5))
plt.plot(range(NUM_GENERACIONES), mejores_aptitudes, label='Mejor aptitud por generación')
plt.title('Mejor aptitud encontrada por generación')
plt.xlabel('Generación')
plt.ylabel('Mejor aptitud')
plt.legend()
plt.grid(True)
plt.show()


