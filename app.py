import streamlit as st

def main():
    archivo_ventas = 'ventas.csv'
    # Agregar una imagen en la parte superior de la barra lateral
    imagen_path = 'src/logo_empresa.jpg'
    st.sidebar.image(imagen_path, use_column_width=True)

    # Crear una lista desplegable con opciones
    opciones = ["Menú principal", "Gráficos", "Predicciones IA", "Ventas", "Agregar nueva venta"]
    seleccion = st.sidebar.selectbox("Ir a", opciones, index=0)

    # Redirigir a la página correspondiente según la opción seleccionada
    if seleccion == "Gráficos":
        from VisualizarGraficos import main as graficos_main
        graficos_main(archivo_ventas)
    elif seleccion == "Predicciones IA":
        from IAPredictora import main as ia_main
        ia_main(archivo_ventas)
    elif seleccion == "Ventas":
        from TablaConFiltros import main as tabla_main
        tabla_main(archivo_ventas)
    elif seleccion == "Agregar nueva venta":
        from AgregarVenta import main as agregar_main
        agregar_main(archivo_ventas)

if __name__ == '__main__':
    main()
