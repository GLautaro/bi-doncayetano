import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.consts import meses 

def requerimiento_3(dataset):
    st.header("Proveedores con mayor cantidad de productos entregados por mes/año.")
    st.write('Por mes/año')
    anio = st.selectbox(
     'Año',
    (2019,2020,2021, 'Todos los años'))
    if anio != 'Todos los años':
        df_r3_mes = dataset.loc[dataset['anio_recepcion'] == anio]
        meses_dataset = sorted(df_r3_mes.mes_recepcion.unique())
        op_meses = list(map(lambda x : meses[x - 1], meses_dataset))
        op_meses.append('Todos los meses')
        mes_r3= st.selectbox(key="mes_r3",
        label='Mes', options=op_meses)
        if(mes_r3 == 'Todos los meses'):
            df_r3_mes = df_r3_mes.groupby(['nombre_mes_recepcion','mes_recepcion', 'nombre_proveedor']).agg({'cantidad_recibida': 'sum'})
            df_r3_mes = df_r3_mes.sort_values(by=['mes_recepcion', 'cantidad_recibida'], ascending=[True, False])
            df_r3_mes_to_graph = df_r3_mes.reset_index()
            fig = px.bar(df_r3_mes_to_graph, x='nombre_mes_recepcion', y='cantidad_recibida', color="nombre_proveedor", labels={
                     "nombre_mes_recepcion": "Mes recepción",
                     "cantidad_recibida": "Cantidad recibida",
                     "nombre_proveedor": "Proveedor"
                 })
        else:
            df_r3_mes = df_r3_mes.loc[df_r3_mes['nombre_mes_recepcion'] == mes_r3]
            df_r3_mes = df_r3_mes.groupby(['nombre_mes_recepcion','mes_recepcion', 'nombre_proveedor']).agg({'cantidad_recibida': 'sum'})
            df_r3_mes = df_r3_mes.sort_values(by=['mes_recepcion', 'cantidad_recibida'], ascending=[True, False])
            df_r3_mes_to_graph = df_r3_mes.reset_index()
            fig = px.pie(df_r3_mes_to_graph, values='cantidad_recibida', names="nombre_proveedor", labels={
                     "cantidad_recibida": "Cantidad recibida",
                     "nombre_proveedor": "Proveedor"
                 })
    else:
        df_r3_mes = dataset.groupby(['anio_recepcion', 'nombre_proveedor']).agg({'cantidad_recibida': 'sum'})
        df_r3_mes = df_r3_mes.sort_values(by=['anio_recepcion', 'cantidad_recibida'], ascending=[True, False])
        df_r3_mes_to_graph = df_r3_mes.reset_index()
        df_r3_mes_to_graph =df_r3_mes_to_graph.astype({"anio_recepcion": str})
        fig = px.bar(df_r3_mes_to_graph, x='anio_recepcion', y='cantidad_recibida', color="nombre_proveedor", labels={
                     "anio_recepcion": "Año recepción",
                     "cantidad_recibida": "Cantidad recibida",
                     "nombre_proveedor": "Proveedor"
                 })

    st.write(fig)
    #Mayor proveedor por mes
    df_r3_mes = df_r3_mes.rename(columns={'cantidad_recibida': 'Cantidad recibida' })
    st.write("Mayor proveedor por mes:")
    st.dataframe(df_r3_mes)

def requerimiento_4(dataset):
    st.header("Pérdidas por mes")
    anio = st.selectbox(
     'Año',
    (2019,2020,2021))
    
    df_r4_mes = dataset.loc[dataset['anio_solicitud'] == anio]
    meses_dataset = sorted(df_r4_mes.mes_solicitud.unique())
    op_meses = list(map(lambda x : meses[x - 1], meses_dataset))
    op_meses.append('Todos los meses')
    mes_r4= st.selectbox(key="mes_r4",
        label='Mes', options=op_meses)
    if(mes_r4 == 'Todos los meses'):
        df_r4_mes = df_r4_mes.groupby(['nombre_mes_solicitud', 'mes_solicitud', 'nombre_proveedor']).agg({'cantidad_solicitada': 'sum','cantidad_recibida': 'sum'})
        df_r4_mes['cantidad_perdida'] =  df_r4_mes['cantidad_solicitada'] - df_r4_mes['cantidad_recibida']
        df_r4_mes['porcentaje_perdida'] = df_r4_mes.apply(lambda x:100 * x.cantidad_perdida / x.cantidad_solicitada,axis=1)
        df_r4_mes = df_r4_mes.sort_values(by=['mes_solicitud'], ascending=[True])
        df_r4_mes = df_r4_mes.reset_index()
        fig = px.bar(df_r4_mes, x='nombre_mes_solicitud', y='porcentaje_perdida', color="nombre_proveedor", labels={
                     "nombre_mes_solicitud": "Mes solicitud",
                     "porcentaje_perdida": "Porcentaje de pérdida",
                     "nombre_proveedor": "Proveedor"
                 })
    else:
        df_r4_mes = df_r4_mes.loc[df_r4_mes['nombre_mes_solicitud'] == mes_r4]       
        df_r4_mes = df_r4_mes.sort_values(by=['mes_solicitud'], ascending=[True])
        df_r4_mes = df_r4_mes.groupby(['nombre_proveedor']).agg({'cantidad_solicitada': 'sum','cantidad_recibida': 'sum'}) 
        df_r4_mes['cantidad_perdida'] =  df_r4_mes['cantidad_solicitada'] - df_r4_mes['cantidad_recibida']
        df_r4_mes['porcentaje_perdida'] = df_r4_mes.apply(lambda x:100 * x.cantidad_perdida / x.cantidad_solicitada,axis=1)
        df_r4_mes = df_r4_mes.reset_index()
        fig = px.pie(df_r4_mes, values='porcentaje_perdida', names="nombre_proveedor", labels={
           "porcentaje_perdida": "Porcentaje de pérdida",
            "nombre_proveedor": "Proveedor"
        })
    st.write(fig)

    
def requerimiento_7(dataset):
    st.header("Comparador por condicion de pago")
    proveedores = st.multiselect("Seleccione proveedores", list(dataset["nombre_proveedor"].unique()), ["Dahyana Azabal", "Agustin Chiavassa"])

    df_r6 = dataset[["nombre_proveedor", "condicion_pago"]].drop_duplicates()
    df_r6_to_show = df_r6[df_r6["nombre_proveedor"].isin(proveedores)]
    df_r6_to_show = df_r6_to_show.rename(columns={'nombre_proveedor': 'Proveedor', 'condicion_pago': 'Condición de pago'})
    st.write(df_r6_to_show)

    st.header("Comparador por Tiempo de Entrega por producto")
    proveedores_2 = st.multiselect("Seleccione proveedores", list(dataset["nombre_proveedor"].unique()), ["Dahyana Azabal", "Lautaro Gonzalez"])
    productos = st.multiselect("Seleccione productos", list(dataset["nombre_producto"].unique()), ["Levadura", "Harina 0000"])

    df_r7 = dataset[["nombre_proveedor", "nombre_producto", "fecha_solicitud", "fecha_recepcion"]]

    df_r7['tiempo_entrega'] =  df_r7['fecha_recepcion'] - df_r7['fecha_solicitud']
    df_r7['tiempo_entrega'] =  df_r7['tiempo_entrega'] / np.timedelta64(1,"D")
    df_r7 = df_r7.groupby(['nombre_proveedor', 'nombre_producto']).mean().reset_index()
    df_r7 = df_r7[df_r7["nombre_proveedor"].isin(proveedores_2) & df_r7["nombre_producto"].isin(productos)]
    df_r7 = df_r7.rename(columns={'nombre_proveedor': 'Proveeor', 'nombre_producto': 'Producto','tiempo_entrega': 'Tiempo entrega' })
    st.write(df_r7)



def LoadPage(dataset):
    
    st.title("Requerimientos relacionados a proveedores")
    requerimiento_3(dataset)
    requerimiento_4(dataset)
    requerimiento_7(dataset)


