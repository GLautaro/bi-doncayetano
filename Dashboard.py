#Importacion modulos de terceros
import streamlit as st
import pandas as pd
## import psycopg2
from sqlalchemy import create_engine

#Importacion Paginas
import Pages.introduccion as introduccion
import Pages.requerimientos as requerimientos
import Pages.proveedores as proveedores
import Pages.productos as productos

# Conexion BD
alchemyEngine=create_engine(f"postgresql+psycopg2://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}/{st.secrets['dbname']}", pool_recycle=3600)
dbConnection=alchemyEngine.connect()


df=pd.read_sql("select hc.id_compra, prod.id_tipo_producto, prod.nombre_tipo_producto, precio_unitario, prod.id_producto, prod.nombre as nombre_producto, prov.nombre as nombre_proveedor,prov.nombre_condicion_pago as condicion_pago, fs.fecha_solicitud as fecha_solicitud, fs.nombre_mes as nombre_mes_solicitud,fs.mes as mes_solicitud, fs.anio as anio_solicitud,fr.fecha_recepcion as fecha_recepcion, fr.nombre_mes as nombre_mes_recepcion, fr.mes as mes_recepcion, fr.anio as anio_recepcion, cantidad_solicitada, cantidad_recibida from hechos_compras hc join fechas_solicitudes fs on fs.id_fecha_solicitud = hc.id_fecha_solicitud join fechas_recepciones fr on fr.id_fecha_recepcion = hc.id_fecha_recepcion join productos prod on prod.id_producto = hc.id_producto join proveedores prov on prov.id_proveedor = hc.id_proveedor", dbConnection)
pd.set_option('display.expand_frame_repr', False);

##dataFrame = dataFrame.groupby(by="nombre_mes").sum()
dbConnection.close()

def CreateLayout():
    st.sidebar.title("Menú")
    app_mode = st.sidebar.selectbox("Seleccione una página:",
                                    ["Introducción", "Proveedores", "Productos"])
    
    if app_mode == 'Introducción':
        introduccion.LoadPage()
    elif app_mode == 'Proveedores':
        proveedores.LoadPage(df)
    elif app_mode == 'Productos':
        productos.LoadPage(df)
    else:
        pass


if __name__ == "__main__":
    CreateLayout()