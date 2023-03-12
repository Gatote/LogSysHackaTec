import random
import csv
from datetime import datetime, timedelta

    
# Lista de nombres de compradores
nombres_compradores = ['Comprador 1', 'Comprador 2', 'Comprador 3', 'Comprador 4', 'Comprador 5']

# Fecha de inicio (522 semanas antes de la fecha actual)
fecha_actual = datetime.now()
fecha_inicio = fecha_actual - timedelta(weeks=522)
fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')

# Crear archivo CSV y escribir encabezados
with open('GeneradorDeCSVUnProducto/ventas.csv', mode='w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Comprador', 'Numero de ventas', 'Fecha'])

    # Escribir una venta aleatoria para cada comprador en cada semana
    fecha_actual = fecha_inicio
    while fecha_actual <= datetime.now():
        for comprador in nombres_compradores:
            numero_ventas = random.randint(1, 10)

            # Escribir registro en archivo CSV
            fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
            writer.writerow([comprador, numero_ventas, fecha_actual_str])

        fecha_actual = fecha_actual + timedelta(weeks=1)

print(f'Se ha creado el archivo "ventaqueso.csv" con ventas aleatorias de las últimas 522 semanas desde el {fecha_inicio_str}.')
