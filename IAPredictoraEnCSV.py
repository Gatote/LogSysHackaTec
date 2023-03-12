import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

def predecir_ventas(archivo_ventas, compradores_interes, carpeta_resultados):
    # Leer archivo CSV
    df = pd.read_csv(archivo_ventas)

    # Filtrar compradores de interés
    df = df[df['Comprador'].isin(compradores_interes)]

    # Agrupar por nombre, comprador y semana
    df = df.groupby(['Comprador', 'Fecha']).agg({'Ventas': np.sum}).reset_index()

    # Agregar columna de semanas adelante
    df['Semanas adelante'] = df['Fecha'].apply(lambda x: (pd.to_datetime(x, utc=True) - pd.to_datetime('now', utc=True)).days // 7)

    # Entrenar modelo de regresión lineal para cada comprador
    compradores = df['Comprador'].unique()
    modelos = {}
    for comprador in compradores:
        df_comprador = df[df['Comprador'] == comprador]
        X = df_comprador['Semanas adelante'].values.reshape(-1, 1)
        y = df_comprador['Ventas'].values.reshape(-1, 1)
        modelo = LinearRegression()
        modelo.fit(X, y)
        modelos[comprador] = modelo

    # Hacer predicciones de ventas para las próximas 2 semanas
    semanas = np.array([1, 2]).reshape(-1, 1)

    predicciones = []
    for comprador in compradores:
        modelo = modelos[comprador]
        prediccion = modelo.predict(semanas)
        predicciones.append({
            'Comprador': comprador,
            'Semana 1': round(prediccion[0][0], 2),
            'Semana 2': round(prediccion[1][0], 2)
        })

    # Crear DataFrame con las predicciones
    df_predicciones = pd.DataFrame(predicciones)

    # Agregar fecha actual como columna
    df_predicciones['Fecha'] = datetime.datetime.now().strftime('%Y-%m-%d')

    # Crear ruta completa del archivo CSV
    ruta_archivo = os.path.join(carpeta_resultados, 'predicciones.csv')

    # Escribir los resultados en el archivo CSV
    df_predicciones.to_csv(ruta_archivo, index=False)
                

predecir_ventas('GeneradorDeCSVUnProducto/ventas.csv', ['Comprador 1', 'Comprador 2', 'Comprador 3', 'Comprador 4', 'Comprador 5'], 'GeneradorDeCSVUnProducto/Resultados')
