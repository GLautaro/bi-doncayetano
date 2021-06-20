import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def requerimiento_3(dataset):
    st.header("3 - Proveedores con mayor cantidad de productos entregados por mes/año.")
    st.write('Por mes/año')
    anio = st.selectbox(
     'Año',
    (2019,2020,2021, 'Todos los años'))
    if anio != 'Todos los años':
        df_r3_mes = dataset.loc[dataset['anio_recepcion'] == anio]
        df_r3_mes = df_r3_mes.groupby(['nombre_mes_recepcion','mes_recepcion', 'nombre_proveedor']).agg({'cantidad_recibida': 'sum'})
        df_r3_mes = df_r3_mes.sort_values(by=['mes_recepcion', 'cantidad_recibida'], ascending=[True, False])
        df_r3_mes_to_graph = df_r3_mes.reset_index()
        fig = px.bar(df_r3_mes_to_graph, x='nombre_mes_recepcion', y='cantidad_recibida', color="nombre_proveedor")

    else:
        df_r3_mes = dataset.groupby(['anio_recepcion', 'nombre_proveedor']).agg({'cantidad_recibida': 'sum'})
        df_r3_mes = df_r3_mes.sort_values(by=['anio_recepcion', 'cantidad_recibida'], ascending=[True, False])
        df_r3_mes_to_graph = df_r3_mes.reset_index()
        df_r3_mes_to_graph =df_r3_mes_to_graph.astype({"anio_recepcion": str})
        fig = px.bar(df_r3_mes_to_graph, x='anio_recepcion', y='cantidad_recibida', color="nombre_proveedor")

    st.write(fig)
    #Mayor proveedor por mes
    st.write("Mayor proveedor por mes:")
    st.dataframe(df_r3_mes)

def requerimiento_4(dataset):
    st.header("4 - Perdidas por mes")
    anio = st.selectbox(
     'Año',
    (2019,2020,2021))
    df_r4_mes = dataset.loc[dataset['anio_solicitud'] == anio]
    df_r4_mes = df_r4_mes.groupby(['nombre_mes_solicitud', 'mes_solicitud', 'nombre_proveedor']).agg({'cantidad_solicitada': 'sum','cantidad_recibida': 'sum'})
    df_r4_mes['cantidad_perdida'] =  df_r4_mes['cantidad_solicitada'] - df_r4_mes['cantidad_recibida']
    df_r4_mes['porcentaje_perdida'] = df_r4_mes.apply(lambda x:100 * x.cantidad_perdida / x.cantidad_solicitada,axis=1)
    df_r4_mes = df_r4_mes.sort_values(by=['mes_solicitud'], ascending=[True])
    df_r4_mes = df_r4_mes.reset_index()
    fig = px.bar(df_r4_mes, x='nombre_mes_solicitud', y='porcentaje_perdida', color="nombre_proveedor")

    st.write(fig)

    
def requerimiento_7(dataset):
    st.header("Comparador por condicion de pago")
    proveedores = st.multiselect("Seleccione proveedores", list(df["nombre_proveedor"].unique()), ["Dahyana Azabal", "Agustin Chiavassa"])

    df_r6 = df[["nombre_proveedor", "condicion_pago"]].drop_duplicates()
    
    st.write(df_r6[df_r6["nombre_proveedor"].isin(proveedores)])

    st.header("Comparador por Tiempo de Entrega por producto")
    proveedores_2 = st.multiselect("Seleccione proveedores", list(df["nombre_proveedor"].unique()), ["Dahyana Azabal", "Lautaro Gonzalez"])
    productos = st.multiselect("Seleccione productos", list(df["nombre_producto"].unique()), ["Levadura", "Harina 0000"])

    df_r7 = df[["nombre_proveedor", "nombre_producto", "fecha_solicitud", "fecha_recepcion"]]

    df_r7['tiempo_entrega'] =  df_r7['fecha_recepcion'] - df_r7['fecha_solicitud']
    df_r7['tiempo_entrega'] =  df_r7['tiempo_entrega'] / np.timedelta64(1,"D")
    df_r7 = df_r7.groupby(['nombre_proveedor', 'nombre_producto']).mean().reset_index()

    st.write(df_r7[df_r7["nombre_proveedor"].isin(proveedores_2) & df_r7["nombre_producto"].isin(productos)])



def LoadPage(dataset):
    st.title("Requerimientos relacionados a proveedores")
    st.write("Set de datos:")
    st.write(dataset)
    requerimiento_3(dataset)
    requerimiento_4(dataset)
    requerimiento_7(dataset)


