#######################################################################################
# Algoritmo para mutar un alelo aleatorio a aquellos genes pertenecientes a los 
# cromosomas de A que tengan en su i-ésima fila un correspondiente de B inferior a 0.09 
#  Guarda los resultados en un vector C y los muestra por pantalla
#######################################################################################

import random

# Parámetros
TAMANIO_POBLACION = 20
LONGITUD_CROMOSOMA = 5

##################################################################
# Inicializar la población
###################################################################
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma):
    poblacion = []
    for z in range(tamanio_poblacion):
        cromosoma = ""
        for t in range(longitud_cromosoma):
            cromosoma = cromosoma+str(random.randint(0, 1))
        poblacion.append(cromosoma)
    return poblacion

##################################################################
# Generar vector B de números aleatorios entre 0 y 1
###################################################################

def generar_vector_aleatorio(longitud=20):
    """
    Genera un vector aleatorio de la longitud especificada, con valores entre 0 y 1.
    
    Parámetros:
    longitud (int): La longitud del vector. Por defecto es 20.
    
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
    return cromosoma_mutado

##################################################################
# Generar población vector A de 20 individuos binarios aleatorios
###################################################################

individuos = inicializar_poblacion(TAMANIO_POBLACION, LONGITUD_CROMOSOMA)
print("Población inicial:", individuos)

vector_mutacion = generar_vector_aleatorio(TAMANIO_POBLACION)
print("Vector de mutación:", vector_mutacion)

##################################################################
# Generar el vector mutado según el criterio dado
###################################################################

vector_mutado = []

for i in range(TAMANIO_POBLACION):
    if vector_mutacion[i] < 0.09:
        vector_mutado.append(mutar_cromosoma(individuos[i]))
    else:
        vector_mutado.append(individuos[i])

print("Vector mutado:", vector_mutado)

