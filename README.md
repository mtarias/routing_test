# Routing Test
Esta implementación se basa en un algoritmo que busca asignar despachos a vehículos, donde cada vehículo tiene una capacidad, cada despacho un peso y existe un costo de asignar X despacho a Y vehículo.

## Datos de entrada:
* Carga de cada despacho
* Capacidad de cada vehículo
* Casos de despachos incompatibles
* Matrix de costos de cada despacho por cada vehiculo

## Datos de salida:
* Coste total de la solución lograda
* Asignación de cada paquete en cada vehículo

## Estrategia utilizada:
Para resolver este problema se utiliza una estrategia codiciosa, donde se busca que cada decisión cumpla como un subconjunto óptimo de la solución general, y que cada decisión (asignación de despacho) no sea cambiada a medida que se avanza en el algoritmo, manteniendo siempre un óptimo local. 
Esta estrategia tiene la ventaja de ser rápida y no muy dificil de implementar, lo que ayuda para una implementación real.
Su desventaja es que no asegura llegar a la solución global del problema, además de existir la posibilidad de dejar despachos fuera.
La idea general utilizada es la siguiente: "Primero se asignan los despachos más grandes que tienen el menor costo asignado, para ir avanzando con los despachos más pequeños. En caso de empate, se van llenando aquellos autos que tienen mas espacio disponible"

## Implementacion:
El algoritmo recibe como entrada un arreglo de despachos, la lista de vehiculos y la matriz de costos. Realiza lo siguiente:
1. Ordena los paquetes por peso, de forma descendente (los más pesados primero)
2. Por cada paquete del orden anterior:
2.a. Se buscan sus costos y se ordenan de menor a mayor, en caso de empate, se busca que el vehiculo mencionado tenga una mayor capacidad disponible
2.b. Por cada costo anterior:
2.b.i. Se toma el primer costo (el menor)
2.b.ii. Se busca el auto correspondiente y se compara el peso del despacho con la capacidad del auto
2.b.ii.i. Si tiene capacidad, se asigna el despacho al vehículo correspondiente y se resta la capacidad actual del mismo
2.b.ii.ii. Si no hay capacidad (o hay un choque de despachos incompatibles) se prueba con el siguiente peso disponible.
3. Se itera hasta llenar todos los automóviles o hasta no quedar despachos por asignar.

## Ejecución del código:
Para ejecutar cada instancia se debe ingresar el siguiente código:

`python3 main.py expX`

donde expX corresponde a la carpeta donde se encuentran los archivos de entrada [exp1, exp2, etc]

Para generar una nueva instancia de prueba se deben generar 4 archivos
* costs.txt: Archivo con los costos de cada paquete. En orden: nombre del paquete, vehículo y costo
* incompatible.txt: Archivo con los paquetes incompatibles, separados por coma
* packages.txt: Archivo con cada nombre de paquete y su carga, separados por coma
* vehicles.txt: Archivo con cada nombre de vehículo y su capacidad máxima, separados por coma