####################################################################
# CEIA - 16Co2024 - Algoritmos Evolutivos - TP1 - Ejercicio 4
# Gustavo J. Rivas (a1620) | Myrna L. Degano (a1618)
####################################################################
# Algoritmo genético que utilice el operador de selección por ruleta
# con probabilidades de cruza y mutación a elección.
####################################################################

import random
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from mpl_toolkits.mplot3d import Axes3D

# Parámetros del algoritmo genético

print("\nINGRESE LOS PARÁMETROS PARA LA EJECUCIÓN DEL ALGORITMO (O <ENTER> PARA TOMAR LOS VALORES POR DEFAULT)\n")

TAMANIO_POBLACION = input("TAMAÑO DE LA POBLACIÓN (DEFAULT: 50): ").strip()
TAMANIO_POBLACION = int(TAMANIO_POBLACION) if TAMANIO_POBLACION else 50

GENERACIONES = input("CANTIDAD DE GENERACIONES (DEFAULT: 100): ").strip()
GENERACIONES = int(GENERACIONES) if GENERACIONES else 100

PROBABILIDAD_CRUCE = input("PROBABILIDAD DE CRUCE (DEFAULT: 0.85): ").strip()
PROBABILIDAD_CRUCE = float(PROBABILIDAD_CRUCE) if PROBABILIDAD_CRUCE else 0.85

PROBABILIDAD_MUTACION = input("PROBABILIDAD DE MUTACIÓN (DEFAULT: 0.07): ").strip()
PROBABILIDAD_MUTACION = float(PROBABILIDAD_MUTACION) if PROBABILIDAD_MUTACION else 0.07

# Para representar valores de x entre [-10, 10] con precisión de 3 decimales
# 10 - (-10) => Rango de x = 20.000 => 20000
# Para representar valores de y entre [0, 20] con precisión de 3 decimales
# Rango de y = 20.000 => 20000
# 2**14 = 16384, 2**15 = 32768 => 15 bits
LONGITUD_CROMOSOMA_X = 15
LONGITUD_CROMOSOMA_Y = 15


# Función de concentración c(x, y)
def funcion_c(x, y):
    return 7.7 + 0.15 * x + 0.22 * y - 0.05 * x**2 - 0.016 * y**2 - 0.007 * x * y

# Inicializar la población con individuos binarios
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma_x, longitud_cromosoma_y):
    return [''.join(random.choice('01') for _ in range(longitud_cromosoma_x + longitud_cromosoma_y)) for _ in range(tamanio_poblacion)]

# Decodificar un cromosoma binario a un valor de x en [-10, 10] y y en [0, 20]
def decodificar_cromosoma(cromosoma):
    cromosoma_x = cromosoma[:LONGITUD_CROMOSOMA_X]
    cromosoma_y = cromosoma[LONGITUD_CROMOSOMA_X:]
    valor_decimal_x = int(cromosoma_x, 2)
    valor_decimal_y = int(cromosoma_y, 2)
    x = round(-10 + valor_decimal_x * 20 / (2**LONGITUD_CROMOSOMA_X - 1), 3)
    y = round(valor_decimal_y * 20 / (2**LONGITUD_CROMOSOMA_Y - 1), 3)
    return x, y

# Evaluar la aptitud de un individuo
def evaluar_aptitud(individuo):
    x, y = decodificar_cromosoma(individuo)
    return funcion_c(x, y)

# Selección por ruleta
def seleccion_ruleta(poblacion):
    aptitudes = [evaluar_aptitud(individuo) for individuo in poblacion]
    suma_aptitudes = sum(aptitudes)
    seleccionados = []
    for _ in range(len(poblacion)):
        punto = random.uniform(0, suma_aptitudes)
        acumulado = 0
        for individuo, aptitud in zip(poblacion, aptitudes):
            acumulado += aptitud
            if acumulado >= punto:
                seleccionados.append(individuo)
                break
    return seleccionados

# Cruce de un par de padres
def cruce(padre1, padre2):
    if random.random() < PROBABILIDAD_CRUCE:
        punto_cruce = random.randint(1, LONGITUD_CROMOSOMA_X + LONGITUD_CROMOSOMA_Y - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2
    return padre1, padre2

# Mutación de un individuo
def mutacion(individuo):
    individuo_mutado = ''.join(
        bit if random.random() > PROBABILIDAD_MUTACION else '1' if bit == '0' else '0' 
        for bit in individuo
    )
    return individuo_mutado

# Actualizar la población
def actualizar_poblacion(poblacion):
    nueva_poblacion = []
    seleccionados = seleccion_ruleta(poblacion)

    for i in range(0, len(seleccionados), 2):
        padre1 = seleccionados[i]
        padre2 = seleccionados[i+1 if i+1 < len(seleccionados) else 0]
        hijo1, hijo2 = cruce(padre1, padre2)
        nueva_poblacion.append(mutacion(hijo1))
        nueva_poblacion.append(mutacion(hijo2))
    return nueva_poblacion

# Algoritmo genético principal
def algoritmo_genetico():
    poblacion = inicializar_poblacion(TAMANIO_POBLACION, LONGITUD_CROMOSOMA_X, LONGITUD_CROMOSOMA_Y)

    resultados = []
    mejores_aptitudes = []

    for generacion in range(GENERACIONES):

        aptitudes = [evaluar_aptitud(individuo) for individuo in poblacion]
        mejor_aptitud = max(aptitudes)
        mejores_aptitudes.append(mejor_aptitud)
        mejor_individuo = poblacion[aptitudes.index(mejor_aptitud)]

        mejor_x, mejor_y = decodificar_cromosoma(mejor_individuo)
        resultados.append([generacion+1, round(mejor_aptitud, 3), mejor_individuo, "x="+ str(mejor_x) +" y =" + str(mejor_y)])

        poblacion = actualizar_poblacion(poblacion)

    mejor_individuo = max(poblacion, key=evaluar_aptitud)
    mejor_x, mejor_y = decodificar_cromosoma(mejor_individuo)
    mejor_valor_c = evaluar_aptitud(mejor_individuo)

    headers = ["Generación #", "Mejor Aptitud", "Mejor individuo", "Fenotipo"]
    print(tabulate(resultados, headers=headers, tablefmt="grid"))

    return mejor_x, mejor_y, mejor_valor_c, mejores_aptitudes

# Ejecutar el algoritmo genético
mejor_x, mejor_y, mejor_valor_c, mejores_aptitudes = algoritmo_genetico()
mejor_valor_c = round(mejor_valor_c, 3)
print(f"La concentración máxima aproximada de la función c es: {mejor_valor_c}")
print(f"Valor de x: {mejor_x}")
print(f"Valor de y: {mejor_y}")

#Gráficos
#fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Graficar c en función de x e y
# Crear una malla de puntos en el plano xy
x = np.linspace(-10, 10, 400)
y = np.linspace(0, 20, 400)
X, Y = np.meshgrid(x, y)

# Evaluar la función en la malla de puntos
Z = funcion_c(X, Y)

# Crear una figura y un eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie 3D
ax.plot_surface(X, Y, Z, cmap='viridis')


# Marcar el máximo punto de concentración con un punto rojo en la gráfica 3D

ax.scatter(mejor_x, mejor_y, mejor_valor_c, color='red', marker='o', s=100)

# Agregar etiquetas y título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Distribución de la concentración c(x, y) y máximo encontrado')

# Mostrar la gráfica
plt.show()

# Graficar mejores aptitudes en función de cada generación en el segundo subgráfico (2D)

plt.figure(figsize=(10, 5))
plt.plot(range(GENERACIONES), mejores_aptitudes, label='Mejor aptitud por generación')
plt.title('Mejor aptitud encontrada por generación')
plt.xlabel('Generación')
plt.ylabel('Mejor aptitud')
plt.legend()
plt.grid(True)
plt.show()