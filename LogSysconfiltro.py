import datetime
import streamlit as st
import pandas as pd
from PIL import Image

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("MAHLELogo.png")
with col3:
    st.write(' ')

st.title("Registro de barcos")
dfxl = pd.read_excel('test.xlsx')

formaopc = st.sidebar.form("formaopc")

col4, col5, col6 = formaopc.columns(3)
with col4:
    st.write(' ')
with col5:
    st.image("LogsysLogo.png")
with col6:
    st.write(' ')

st.sidebar.header("Opciones")
namesh = formaopc.text_input("Nombre del Barco:")
nameprv = formaopc.text_input("Nombre Proveedor:")
numprv = formaopc.number_input("Número de Proveedor:")
numbcz = formaopc.text_input("Número de parte BCZ")
estadosh = formaopc.selectbox(
     'Estado del barco',
     ['Óptimo', 'Decente', 'Parcialmente func.', 'Dañado'])
pronosticoclima = formaopc.selectbox(
     'Pronóstico del clima',
     ['Soleado', 'Frío', 'Tormenta', 'Lluvia'])
numbpltt = formaopc.number_input("Número de palett")
eta = formaopc.date_input("Fecha de ETA (Estimación de llegada)", datetime.datetime (2022, 9, 8))
add_data = formaopc.form_submit_button()
if add_data:
    new_data = {"BarcoNombre": namesh,"ProveedorNombre":nameprv,"NumProveedor": int(numprv),"NumBCZ":numbcz,"EstadoBarco":estadosh,"PronClima":pronosticoclima,"NumPaletts": int(numbpltt), "ETA": eta}
    dfxl = dfxl.append(new_data, ignore_index=True)
    dfxl.to_excel('test.xlsx', index = False)

st.markdown("##")
st.sidebar.header("Filtrar por:")
barco = st.sidebar.multiselect(
    "Nombre del barco:",
    options=dfxl["BarcoNombre"].unique(),
)

proveedor = st.sidebar.multiselect(
    "Nombre del Proveedor:",
    options=dfxl["ProveedorNombre"].unique(),
)

numprov = st.sidebar.multiselect(
    "Número de proveedor:",
    options=dfxl["NumProveedor"].unique(),
)

dfxl_selection = dfxl.query(
    "BarcoNombre == @barco & ProveedorNombre == @proveedor & NumProveedor == @numprov"
)

st.dataframe(dfxl_selection)


#--- Estilo de la página ---#
# from PIL import Image (Librería a añadir)
hide_st_style = """
     <style>
     #MainMenu {visibility: hidden;}
     footer {visibility: hidden;}
     header {visibility: hidden;}
     </style>
     """
st.markdown(hide_st_style, unsafe_allow_html=True)
