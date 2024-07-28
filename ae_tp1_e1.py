#######################################################################################
# CEIA - 16Co2024 - Algoritmos Evolutivos - TP1 - Ejercicio 1
# Gustavo J. Rivas (a1620) | Myrna L. Degano (a1618)
#######################################################################################
# Algoritmo para mutar un alelo aleatorio a aquellos genes pertenecientes a los 
# cromosomas de A que tengan en su i-ésima fila un correspondiente de B inferior a 0.09 
#  Guarda los resultados en un vector C y los muestra por pantalla
#######################################################################################

import random
from tabulate import tabulate

##################################################################
# Parámetros
##################################################################

print("\nINGRESE LOS PARÁMETROS PARA LA EJECUCIÓN DEL ALGORITMO (O <ENTER> PARA TOMAR LOS VALORES POR DEFAULT)\n")

TAMANIO_POBLACION = input("TAMAÑO DE LA POBLACIÓN (DEFAULT: 20): ").strip()
TAMANIO_POBLACION = int(TAMANIO_POBLACION) if TAMANIO_POBLACION else 20

LONGITUD_CROMOSOMA  = input("LONGITUD DEL CROMOSOMA (DEFAULT: 5): ").strip()
LONGITUD_CROMOSOMA  = int(LONGITUD_CROMOSOMA ) if LONGITUD_CROMOSOMA  else 5

TASA_LIMITE  = input("TASA LÍMITE PARA LA MUTACIÓN (DEFAULT: 0.09): ").strip()
TASA_LIMITE  = float(TASA_LIMITE) if TASA_LIMITE else 0.09

##################################################################
# Inicializar la población
##################################################################
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma):
    """
    Genera un vector aleatorio de la longitud especificada, con valores entre 0 y 1.
    con valores binarios del tamaño especificado

    Parámetros:
    tamanio_poblacion (int): La longitud del vector.
    longitud_cromosoma (int): La longitud del individuo

    Retorna:
    list: Un vector de individuos (cromosomas) aleatorios)
    """
    poblacion = []
    for _ in range(tamanio_poblacion):
        cromosoma = ""
        for _ in range(longitud_cromosoma):
            cromosoma = cromosoma+str(random.randint(0, 1))
        poblacion.append(cromosoma)
    return poblacion

##################################################################
# Generar vector B de números aleatorios entre 0 y 1
###################################################################

def generar_vector_aleatorio(longitud):
    """
    Genera un vector aleatorio de la longitud especificada, con valores entre 0 y 1.
    
    Parámetros:
    longitud (int): La longitud del vector.
    
    Retorna:
    list: Un vector de valores aleatorios entre 0 y 1.
    """
    vector = [random.random() for _ in range(longitud)]
    return vector


##################################################################
# Función para mutar un bit aleatorio en un cromosoma
###################################################################

def mutar_cromosoma(cromosoma):
    """
    Muta un bit aleatorio de un cromosoma binario.
    
    Parámetros:
    cromosoma (str): Un cromosoma binario.
    
    Retorna:
    str: El cromosoma mutado.
    """
    indice_mutacion = random.randint(0, len(cromosoma) - 1)
    if cromosoma[indice_mutacion] == '0':
        cromosoma_mutado = cromosoma[:indice_mutacion] + '1' + cromosoma[indice_mutacion + 1:]
    else:
        cromosoma_mutado = cromosoma[:indice_mutacion] + '0' + cromosoma[indice_mutacion + 1:]
    return (cromosoma_mutado, indice_mutacion)

##################################################################
# Desarrollo del algoritmo
###################################################################

individuos = inicializar_poblacion(TAMANIO_POBLACION, LONGITUD_CROMOSOMA)

vector_mutacion = generar_vector_aleatorio(TAMANIO_POBLACION)

vector_mutado = []

resultados = []

for i in range(TAMANIO_POBLACION):
    if vector_mutacion[i] < TASA_LIMITE:
        (cromosoma_mutado, gen_mutado) = mutar_cromosoma(individuos[i])
        gen_mutado = "Mutación del gen " + str(gen_mutado+1)
        vector_mutado.append(cromosoma_mutado)
    else:
        (cromosoma_mutado, gen_mutado) = (individuos[i], "Sin mutación")
        vector_mutado.append(individuos[i])

    resultados.append([individuos[i], vector_mutacion[i], vector_mutado[i], gen_mutado])


headers = ["Población inicial", "Vector de mutación", "Vector mutado", "Comentarios (Pm="+ str(TASA_LIMITE)+")"]
print(tabulate(resultados, headers=headers, tablefmt="grid"))