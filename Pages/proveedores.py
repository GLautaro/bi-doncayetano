import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def LoadPage(df):
    st.title("Requerimientos relacionados a proveedores")
    st.write("Set de datos:")
    st.write(df)

    st.header("Proveedores con mayor cantidad de productos entregados por mes.")
   
    st.header("Comparador por condicion de pago")
    proveedores = st.multiselect("Seleccione proveedores", list(df["nombre_proveedor"].unique()), ["Dahyana Azabal", "Agustin Chiavassa"])

    df_r4 = df[["nombre_proveedor", "condicion_pago"]].drop_duplicates()
    
    st.write(df_r4[df_r4["nombre_proveedor"].isin(proveedores)])

    st.header("Comparador por Tiempo de Entrega por producto")
    proveedores_2 = st.multiselect("Seleccione proveedores", list(df["nombre_proveedor"].unique()), ["Dahyana Azabal", "Lautaro Gonzalez"])
    productos = st.multiselect("Seleccione proveedores", list(df["nombre_producto"].unique()), ["Levadura", "Harina 0000"])

    df_r5 = df[["nombre_proveedor", "nombre_producto", "fecha_solicitud", "fecha_recepcion"]]

    df_r5['tiempo_entrega'] =  df_r5['fecha_recepcion'] - df_r5['fecha_solicitud']
    df_r5['tiempo_entrega'] =  df_r5['tiempo_entrega'] / np.timedelta64(1,"D")
    df_r5 = df_r5.groupby(['nombre_proveedor', 'nombre_producto']).mean().reset_index()

    st.write(df_r5[df_r5["nombre_proveedor"].isin(proveedores_2) & df_r5["nombre_producto"].isin(productos)])


