####################################################################
# CEIA - 16Co2024 - Algoritmos Evolutivos - TP1 - Ejercicio 2
# Gustavo J. Rivas (a1620) | Myrna L. Degano (a1618)
####################################################################

# Algoritmo Genético que encuentra el máximo de la función x^2
# Selección por ruleta
###################################################################
import random
from tabulate import tabulate

##################################################################
# Parámetros
##################################################################

print("\nINGRESE LOS PARÁMETROS PARA LA EJECUCIÓN DEL ALGORITMO (O <ENTER> PARA TOMAR LOS VALORES POR DEFAULT)\n")

TAMANIO_POBLACION = input("TAMAÑO DE LA POBLACIÓN (DEFAULT: 4): ").strip()
TAMANIO_POBLACION = int(TAMANIO_POBLACION) if TAMANIO_POBLACION else 4

LONGITUD_CROMOSOMA = input("LONGITUD DEL CROMOSOMA (DEFAULT: 5): ").strip()
LONGITUD_CROMOSOMA = int(LONGITUD_CROMOSOMA) if LONGITUD_CROMOSOMA else 5

TASA_CRUCE = input("PROBABILIDAD DE CRUCE (DEFAULT: 0.92): ").strip()
TASA_CRUCE = float(TASA_CRUCE) if TASA_CRUCE else 0.92

TASA_MUTACION = input("PROBABILIDAD DE MUTACIÓN (DEFAULT: 0.01): ").strip()
TASA_MUTACION = float(TASA_MUTACION) if TASA_MUTACION else 0.01

GENERACIONES = input("CANTIDAD DE GENERACIONES (DEFAULT: 10): ").strip()
GENERACIONES = int(GENERACIONES) if GENERACIONES else 10


###################################################################
# Aptitud (y = x^2)
###################################################################
def aptitud(cromosoma):
    x = int(cromosoma, 2)
    return x ** 2

###################################################################
# Inicializar la población
###################################################################
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma):
    poblacion = []
    for _ in range(tamanio_poblacion):
        cromosoma = ""
        for _ in range(longitud_cromosoma):
            cromosoma = cromosoma+str(random.randint(0, 1))
        poblacion.append(cromosoma)
    return poblacion

###################################################################
# Selección por ruleta
###################################################################
def seleccion_ruleta(poblacion, aptitud_total):
    seleccion = random.uniform(0, aptitud_total)
    aptitud_actual = 0
    for individuo in poblacion:
        aptitud_actual = aptitud_actual+aptitud(individuo)
        if aptitud_actual > seleccion:
            return individuo

###################################################################
# Cruce monopunto
###################################################################
def cruce_mono_punto(progenitor1, progenitor2, tasa_cruce):
    if random.random() < tasa_cruce:
        punto_cruce = random.randint(1, len(progenitor1) - 1)
        descendiente1 = progenitor1[:punto_cruce] + progenitor2[punto_cruce:]
        descendiente2 = progenitor2[:punto_cruce] + progenitor1[punto_cruce:]
    else:
        descendiente1, descendiente2 = progenitor1, progenitor2
    return descendiente1, descendiente2

###################################################################
# Mutación
###################################################################
def mutacion(cromosoma, tasa_mutacion):
    cromosoma_mutado = ""
    for bit in cromosoma:
        if random.random() < tasa_mutacion:
            cromosoma_mutado = cromosoma_mutado+str(int(not int(bit)))
        else:
            cromosoma_mutado = cromosoma_mutado+bit
    return cromosoma_mutado

###################################################################
# Aplicación de operadores genéticos
###################################################################
def algoritmo_genetico(tamaño_poblacion, longitud_cromosoma, tasa_mutacion, tasa_cruce, generaciones):
    poblacion = inicializar_poblacion(tamaño_poblacion, longitud_cromosoma)

    for generacion in range(generaciones):

        # Calcular aptitud total
        aptitud_total = 0
        for cromosoma in poblacion:
            aptitud_total = aptitud_total+aptitud(cromosoma)

        # Selección
        # de progenitores con el método ruleta
        progenitores = []
        for _ in range(tamaño_poblacion):
            progenitores.append(seleccion_ruleta(poblacion, aptitud_total))

        # Cruce
        descendientes = []
        for i in range(0, tamaño_poblacion, 2):
            descendiente1, descendiente2 = cruce_mono_punto(progenitores[i], progenitores[i + 1], tasa_cruce)
            descendientes.extend([descendiente1, descendiente2])

        # Mutación
        descendientes_mutados = []
        for descendiente in descendientes:
            descendientes_mutados.append(mutacion(descendiente, tasa_mutacion))

        # Elitismo - se reemplazan los peores cromosomas con los mejores progenitores
        poblacion.sort(key=aptitud)
        descendientes_mutados.sort(key=aptitud, reverse=True)
        for i in range(len(descendientes_mutados)):
            if aptitud(descendientes_mutados[i]) > aptitud(poblacion[i]):
                poblacion[i] = descendientes_mutados[i]

        # Mostrar el mejor individuo de la generación
        mejor_individuo = max(poblacion, key=aptitud)

        resultados.append([generacion + 1, aptitud_total, int(mejor_individuo, 2), aptitud(mejor_individuo)])

    return max(poblacion, key=aptitud)

###################################################################
# Algoritmo genético ejecución principal
###################################################################
print("\n")
resultados = []
mejor_solucion = algoritmo_genetico(TAMANIO_POBLACION, LONGITUD_CROMOSOMA, TASA_MUTACION, TASA_CRUCE, GENERACIONES)

headers = ["Generación #", "Aptitud Total", "Mejor Individuo", "Aptitud del Mejor Individuo"]
print(tabulate(resultados, headers=headers, tablefmt="grid"))

print("\n* Mejor solución:", int(mejor_solucion, 2), "\n* Aptitud:", aptitud(mejor_solucion))

