import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parámetros del algoritmo genético
TAMANIO_POBLACION = 50
LONGITUD_CROMOSOMA_X = 14  # Para representar valores en [-10, 10] con precisión de 3 decimales
LONGITUD_CROMOSOMA_Y = 14  # Para representar valores en [0, 20] con precisión de 3 decimales
GENERACIONES = 100
PROBABILIDAD_CRUCE = 0.85
PROBABILIDAD_MUTACION = 0.07

# Función de concentración c(x, y)
def funcion_c(x, y):
    return 7.7 + 0.15 * x + 0.22 * y - 0.05 * x**2 - 0.016 * y**2 - 0.007 * x * y

# Inicializar la población con individuos binarios
def inicializar_poblacion(tamanio_poblacion, longitud_cromosoma_x, longitud_cromosoma_y):
    return [''.join(random.choice('01') for _ in range(longitud_cromosoma_x + longitud_cromosoma_y)) for _ in range(tamanio_poblacion)]

# Decodificar un cromosoma binario a un valor de x en [-10, 10] y y en [0, 20]
def decodificar_cromosoma(cromosoma):
    cromosoma_x = cromosoma[:LONGITUD_CROMOSOMA_X]
    cromosoma_y = cromosoma[LONGITUD_CROMOSOMA_Y:]
    valor_binario_x = int(cromosoma_x, 2)
    valor_binario_y = int(cromosoma_y, 2)
    x = -10 + valor_binario_x * 20 / (2**LONGITUD_CROMOSOMA_X - 1)
    y = valor_binario_y * 20 / (2**LONGITUD_CROMOSOMA_Y - 1)
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
    mejores_aptitudes = []

    for generacion in range(GENERACIONES):
        aptitudes = [evaluar_aptitud(individuo) for individuo in poblacion]
        mejor_aptitud = max(aptitudes)
        mejores_aptitudes.append(mejor_aptitud)
        mejor_individuo = poblacion[aptitudes.index(mejor_aptitud)]
        
        print(f"Generación {generacion}: Mejor aptitud = {mejor_aptitud}, Mejor individuo = {mejor_individuo}")

        poblacion = actualizar_poblacion(poblacion)

    mejor_individuo = max(poblacion, key=evaluar_aptitud)
    mejor_x, mejor_y = decodificar_cromosoma(mejor_individuo)
    mejor_valor_c = evaluar_aptitud(mejor_individuo)
    
    return mejor_x, mejor_y, mejor_valor_c, mejores_aptitudes

# Ejecutar el algoritmo genético
mejor_x, mejor_y, mejor_valor_c, mejores_aptitudes = algoritmo_genetico()

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

# Agregar etiquetas y título
plt.figure(figsize=(10, 5))
contour = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(contour)
plt.scatter([mejor_x], [mejor_y], color='red', zorder=5)


# Marcar el máximo punto de concentración con un punto rojo en la gráfica 3D

ax.scatter(mejor_x, mejor_y, mejor_valor_c, color='red', marker='o', s=100)

# Agregar etiquetas y título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Distribución de la concentración c(x, y) y máximo encontrado')



# Mostrar la gráfica
plt.show()


# Graficar mejores aptitudes en función de cada generación
plt.figure(figsize=(10, 5))
plt.plot(range(GENERACIONES), mejores_aptitudes, label='Mejor aptitud por generación')
plt.title('Mejor aptitud encontrada por generación')
plt.xlabel('Generación')
plt.ylabel('Mejor aptitud')
plt.legend()
plt.grid(True)
plt.show()
