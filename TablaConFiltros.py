import pandas as pd
import streamlit as st
def main(ArchivoVentas):
    # Cargar el DataFrame con la información de las ventas
    df_ventas = pd.read_csv(ArchivoVentas)

    # Convertir la columna Fecha a datetime
    df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'])

    comprador = st.multiselect("Compradores", df_ventas['Comprador'].unique())
    cantidad_vendida = st.slider("Cantidad vendida", min_value=0, max_value=int(df_ventas['Ventas'].max()))

    fecha_desde = st.date_input("Fecha desde")
    fecha_hasta = st.date_input("Fecha hasta")

    # Convertir la fecha desde y hasta a datetime.date
    fecha_desde = pd.to_datetime(fecha_desde).date() if fecha_desde else df_ventas['Fecha'].min().date()
    fecha_hasta = pd.to_datetime(fecha_hasta).date() if fecha_hasta else df_ventas['Fecha'].max().date()

    ignorar_compradores = st.checkbox("Ignorar compradores")

    ignorar_cantidad = st.checkbox("Ignorar cantidad vendida")
    ignorar_fechas = st.checkbox("Ignorar fechas")

    # Agregar widgets de orden
    orden_columna = st.selectbox("Ordenar por", ['Comprador', 'Ventas', 'Fecha'])
    orden_tipo = st.selectbox("Tipo de orden", ['Ascendente', 'Descendente'])

    # Aplicar los filtros al DataFrame
    if ignorar_compradores and ignorar_cantidad and ignorar_fechas:
        df_filtrado = df_ventas
    elif ignorar_compradores and ignorar_cantidad:
        df_filtrado = df_ventas.loc[
            (df_ventas['Fecha'].dt.date >= fecha_desde) &
            (df_ventas['Fecha'].dt.date <= fecha_hasta)
        ]
    elif ignorar_compradores and ignorar_fechas:
        df_filtrado = df_ventas.loc[
            (df_ventas['Ventas'] >= cantidad_vendida)
        ]
    elif ignorar_cantidad and ignorar_fechas:
        df_filtrado = df_ventas.loc[
            (df_ventas['Comprador'].isin(comprador))
        ]
    elif ignorar_compradores:
        df_filtrado = df_ventas.loc[
            (df_ventas['Ventas'] >= cantidad_vendida) &
            (df_ventas['Fecha'].dt.date >= fecha_desde) &
            (df_ventas['Fecha'].dt.date <= fecha_hasta)
        ]
    elif ignorar_cantidad:
        df_filtrado = df_ventas.loc[
            (df_ventas['Comprador'].isin(comprador)) &
            (df_ventas['Fecha'].dt.date >= fecha_desde) &
            (df_ventas['Fecha'].dt.date <= fecha_hasta)
        ]
    elif ignorar_fechas:
        df_filtrado = df_ventas.loc[
            (df_ventas['Comprador'].isin(comprador)) &
            (df_ventas['Ventas'] >= cantidad_vendida)
        ]
    else:
        df_filtrado = df_ventas.loc[
            (df_ventas['Comprador'].isin(comprador)) &
            (df_ventas['Ventas'] >= cantidad_vendida) &
            (df_ventas['Fecha'].dt.date >= fecha_desde) &
            (df_ventas['Fecha'].dt.date <= fecha_hasta)
        ]

    if df_filtrado.empty:
        st.warning("Selecciona atributos para la consulta")
    else:
        if orden_tipo == 'Ascendente':
            df_filtrado = df_filtrado.sort_values(by=orden_columna, ascending=True)
        else:
            df_filtrado = df_filtrado.sort_values(by=orden_columna, ascending=False)
        st.dataframe(df_filtrado, width=500)