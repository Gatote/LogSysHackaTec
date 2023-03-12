import pandas as pd
import streamlit as st

def main(ArchivoVentas):
    # Cargar el archivo CSV
    ventas = pd.read_csv(ArchivoVentas)

    # Convertir la columna de fecha a tipo datetime
    ventas['Fecha'] = pd.to_datetime(ventas['Fecha'])

    # Obtener el rango de fechas de las ventas
    fecha_minima = ventas['Fecha'].min()
    fecha_maxima = ventas['Fecha'].max()

    # Obtener la lista de vendedores únicos
    vendedores = ventas['Comprador'].unique()

    # Crear el widget multiselect para seleccionar los vendedores a mostrar
    vendedores_seleccionados = st.multiselect('Seleccione los compradores:', vendedores)

    # Filtrar los datos de ventas solo para los vendedores seleccionados
    ventas_seleccionadas = ventas[ventas['Comprador'].isin(vendedores_seleccionados)]

    # Crear los widgets para seleccionar el rango de fechas
    st.write('Seleccione un rango de fechas para filtrar las ventas:')
    start_date = st.date_input('Fecha de inicio', fecha_minima)
    end_date = st.date_input('Fecha de fin', fecha_maxima)

    # Obtener las ventas del intervalo de fechas seleccionado
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    ventas_seleccionadas = ventas_seleccionadas[(ventas_seleccionadas['Fecha'] >= start_date) & (ventas_seleccionadas['Fecha'] <= end_date)]

    if len(vendedores_seleccionados)==0:
        st.warning('Seleccione un comprador')
    else:
        ver_por_mes = st.checkbox("Ver ventas por mes")

        if ver_por_mes:
            # Agrupar las ventas por mes y comprador, y sumar las ventas de cada mes para cada comprador
            ventas_por_mes_y_comprador = ventas_seleccionadas.groupby([pd.Grouper(key='Fecha', freq='M'), 'Comprador'])['Ventas'].sum()

            # Crear un único gráfico con las series de tiempo de los vendedores seleccionados
            if vendedores_seleccionados:
                st.write('Ventas por mes para cada comprador seleccionado:')
                chart_data = pd.DataFrame()
                for comprador in vendedores_seleccionados:
                    ventas_por_mes_comprador = ventas_por_mes_y_comprador.loc[:, comprador]
                    chart_data[comprador] = ventas_por_mes_comprador
                st.line_chart(chart_data)
        else:
            # Agrupar las ventas por semana y comprador, y sumar las ventas de cada semana para cada comprador
            ventas_por_semana_y_comprador = ventas_seleccionadas.groupby([pd.Grouper(key='Fecha', freq='W'), 'Comprador'])['Ventas'].sum()

            # Crear un único gráfico con las series de tiempo de los vendedores seleccionados
            if vendedores_seleccionados:
                st.write('Ventas por semana para cada comprador seleccionado:')
                chart_data = pd.DataFrame()
                for comprador in vendedores_seleccionados:
                    ventas_por_semana_comprador = ventas_por_semana_y_comprador.loc[:, comprador]
                    chart_data[comprador] = ventas_por_semana_comprador
                st.line_chart(chart_data)
