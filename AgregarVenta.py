import pandas as pd
import streamlit as st

def main(ArchivoVentas):
    # Leer los nombres de los compradores del archivo csv
    df = pd.read_csv(ArchivoVentas)
    nombres_compradores = df['Comprador'].unique().tolist()

    es_nuevo_cliente = st.checkbox('Cliente nuevo')
    
    if es_nuevo_cliente:
        nombre_comprador = st.text_input("Nombre del nuevo cliente")
    else:
        nombre_comprador = st.selectbox("Nombre del comprador", nombres_compradores)

    cantidad_venta = st.number_input("Piezas vendidas", value=0, step=1)
    fecha = st.date_input("Fecha de la venta")

    if cantidad_venta == 0:
        st.warning("No se puede hacer una venta en 0")
    elif cantidad_venta < 0:
        st.warning("La cantidad de venta no puede ser negativa")
    elif st.button('Agregar venta'):
        # Crear un dataframe con la información de la venta
        venta = pd.DataFrame({
            'Comprador': [nombre_comprador],
            'Ventas': [cantidad_venta],
            'Fecha': [fecha]
        })

        # Leer el archivo ventas.csv
        try:
            ventas = pd.read_csv(ArchivoVentas)
        except FileNotFoundError:
            ventas = pd.DataFrame(columns=['Comprador', 'Ventas','Fecha'])

        # Concatenar el nuevo registro con los registros existentes
        ventas = pd.concat([ventas, venta], ignore_index=True)

        # Guardar los datos en el archivo ventas.csv
        ventas.to_csv(ArchivoVentas, index=False)

        # Agregar el nuevo nombre de comprador a la lista si es un cliente nuevo
        if es_nuevo_cliente and nombre_comprador not in nombres_compradores:
            nombres_compradores.append(nombre_comprador)

        st.success("La venta ha sido agregada correctamente")