import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from sklearn.linear_model import LinearRegression

def main(archivo_ventas):
    df = pd.read_csv(archivo_ventas)
    compradores = st.multiselect("Compradores", df['Comprador'].unique(), key=archivo_ventas)


    if len(compradores)!=0:
        # Leer archivo CSV

        # Filtrar por compradores de interés
        df = df.loc[df['Comprador'].isin(compradores)]

        # Agregar columna de semanas adelante (incluyendo las próximas dos semanas)
        df['Semanas adelante'] = df['Fecha'].apply(lambda x: ((pd.to_datetime(x, utc=True) - pd.to_datetime('now', utc=True)).days + 7*2) // 7)

        # Inicializar listas para almacenar los resultados
        ventas_estimadas = []
        ventas_estimadas_2 = []  # lista para almacenar las ventas estimadas para la semana 1
        compradores_pred = []

        # Entrenar modelo de regresión lineal y hacer predicciones para cada comprador
        for comprador in compradores:
            # Filtrar por comprador de interés
            df_comprador = df.loc[df['Comprador'] == comprador]

            X = df_comprador['Semanas adelante'].values.reshape(-1, 1)
            y = df_comprador['Ventas'].values.reshape(-1, 1)
            modelo = LinearRegression()
            modelo.fit(X, y)

            # Hacer predicciones de ventas para las próximas 2 semanas
            semanas = np.array([1, 2]).reshape(-1, 1)
            predicciones = modelo.predict(semanas)

            # Almacenar resultados en listas
            compradores_pred.append(comprador)
            ventas_estimadas.append(round(predicciones[-1][0], 2))
            ventas_estimadas_2.append(round(predicciones[0][0], 2))  # agregar ventas estimadas para la semana 1

        # Crear dataframe con los resultados
        resultados = pd.DataFrame({'Comprador': compradores_pred, 'Ventas Estimadas Semana 1': ventas_estimadas_2, 'Ventas Estimadas Semana 2': ventas_estimadas})

        chart1 = alt.Chart(resultados).mark_bar().encode(
            x=alt.X('Comprador', sort=None),
            y='Ventas Estimadas Semana 1',
            tooltip=['Comprador', 'Ventas Estimadas Semana 1']
        ).properties(
            title='Ventas Estimadas para la Semana 1'
        )
        
        chart2 = alt.Chart(resultados).mark_bar().encode(
            x=alt.X('Comprador', sort=None),
            y='Ventas Estimadas Semana 2',
            tooltip=['Comprador', 'Ventas Estimadas Semana 2']
        ).properties(
            title='Ventas Estimadas para la Semana 2'
        )
    else:
        resultados=None
    try:
        if resultados!=None:
            None
    except ValueError:
        st.write(resultados)
        ver_grafico_barras=st.checkbox('Mostrar graficos de barras')
        if  ver_grafico_barras:
            st.altair_chart(chart1, use_container_width=True)
            st.altair_chart(chart2, use_container_width=True)