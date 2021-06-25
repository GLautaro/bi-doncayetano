import streamlit as st
import pandas as pd
import plotly.express as px
from utils.consts import meses


def requerimiento_1(dataset):
    st.header('Porcentajes de productos solicitados por mes/año')
    st.write('Por mes')
    tipo_producto = st.selectbox(
     'Tipo Producto',
    ('Ingrediente', 'Packaging', 'Insumo descartable'))
    anio = st.selectbox(
     'Año',
    (2019,2020,2021, 'Todos los años'))
    
    df_r1 = dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    if anio != 'Todos los años':
        df_r1 = df_r1.loc[df_r1['anio_solicitud'] == anio]
        meses_dataset = sorted(df_r1.mes_solicitud.unique())
        op_meses = list(map(lambda x : meses[x - 1], meses_dataset))
        op_meses.append('Todos los meses')
        mes_r1= st.selectbox(key="mes_r1",
        label='Mes', options=op_meses)
        if(mes_r1 == 'Todos los meses'):
            df_r1 = df_r1.groupby(['mes_solicitud', 'nombre_mes_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
            df_r1['Porcentaje'] = df_r1.groupby(['mes_solicitud']).apply(lambda x:100 * x / float(x.sum()))
            df_r1 = df_r1.reset_index()
            #df_r1_mes =df_r1_mes.astype({"anio_solicitud": str})
            #df_r1_mes['mes_anio'] = df_r1_mes[['nombre_mes_solicitud', 'anio_solicitud']].agg(' '.join, axis=1)
            df_r1 = df_r1.sort_values(['mes_solicitud'])
            fig = px.bar(df_r1, x='nombre_mes_solicitud', y='Porcentaje', color="nombre_producto", labels={
                     "nombre_mes_solicitud": "Mes Solicitud",
                     "Porcentaje": "Porcentaje",
                     "nombre_producto": "Producto"
                 })
        else:
            df_r1 = df_r1.loc[df_r1['nombre_mes_solicitud'] == mes_r1]       
            df_r1 = df_r1.groupby(['nombre_producto']).agg({'cantidad_solicitada': 'sum'})
            df_r1['Porcentaje'] = df_r1.apply(lambda x:100 * x / float(x.sum()))
            df_r1 = df_r1.reset_index()
            #df_r1_mes =df_r1_mes.astype({"anio_solicitud": str})
            #df_r1_mes['mes_anio'] = df_r1_mes[['nombre_mes_solicitud', 'anio_solicitud']].agg(' '.join, axis=1)
            fig = px.pie(df_r1, values='Porcentaje', names="nombre_producto", labels={
                     "Porcentaje": "Porcentaje",
                     "nombre_producto": "Producto"
                 })
 
    else:
        df_r1 = df_r1.groupby(['anio_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
        df_r1['Porcentaje'] = df_r1.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_r1 = df_r1.reset_index()
        df_r1 =df_r1.astype({"anio_solicitud": str})
        fig = px.bar(df_r1, x='anio_solicitud', y='Porcentaje', color="nombre_producto", labels={
                     "anio_solicitud": "Año Solicitud",
                     "Porcentaje": "Porcentaje",
                     "nombre_producto": "Producto"
                 })
        fig.update_layout(xaxis_title="Año", yaxis_title="Porcentaje")

    st.write(fig)

def requerimiento_2(dataset, meses):
    st.header('Relación de cantidad solicitada y entregada por producto por proveedor')
    tipo_producto_r2_mes= st.selectbox(key="tipo_producto_r2_mes",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    df_r2_mes = dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto_r2_mes]
    anio_r2 = st.selectbox(key="anio_r2",
     label='Año',
    options=(2019,2020,2021))
    df_r2_mes = df_r2_mes.loc[df_r2_mes['anio_solicitud'] == anio_r2]
    meses_dataset = sorted(df_r2_mes.mes_solicitud.unique())
    mes_r2= st.selectbox(key="mes_r2",
     label='Mes', options=list(map(lambda x : meses[x - 1], meses_dataset)))
    df_r2_mes = df_r2_mes.loc[df_r2_mes['nombre_mes_solicitud'] == mes_r2]
    df_r2_mes = df_r2_mes.groupby(['nombre_producto', 'nombre_proveedor']).agg({'cantidad_solicitada': 'sum', 'cantidad_recibida':'sum'})
    df_r2_mes = df_r2_mes.rename(columns={'cantidad_solicitada': 'Cantidad Solicitada', 'cantidad_recibida': 'Cantidad Recibida'})
    st.write(df_r2_mes)
    st.write('Por año')
    tipo_producto_r2_mes= st.selectbox(key="tipo_producto_r2_anio",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    df_r2_anio = dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto_r2_mes]
    anio_r2 = st.selectbox(key="anio_r2_anio",
     label='Año',
    options=(2019,2020,2021))
    df_r2_anio = df_r2_anio.loc[df_r2_anio['anio_solicitud'] == anio_r2]
    df_r2_anio = df_r2_anio.groupby(['nombre_producto', 'nombre_proveedor']).agg({'cantidad_solicitada': 'sum', 'cantidad_recibida':'sum'})
    df_r2_anio = df_r2_anio.rename(columns={'cantidad_solicitada': 'Cantidad Solicitada', 'cantidad_recibida': 'Cantidad Recibida'})
    st.write(df_r2_anio)

def requerimiento_5(dataset):
    st.header('Promedio de compras de productos por mes/año')
    st.write('Frecuencia de compra')
    tipo_producto= st.selectbox(key="tipo_producto_r5",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    anio = st.selectbox(key="anio_r5",
     label='Año',
    options=(2019,2020,2021, 'Todos los años'))
    df=dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    if anio != 'Todos los años':
        df = df.loc[df['anio_solicitud'] == anio]
        df = df.groupby(['mes_solicitud','nombre_mes_solicitud','nombre_producto']).agg({'id_producto': 'count'})
        df = df.sort_values(['mes_solicitud'])
        df = df.reset_index()
        fig = px.bar(df, x='nombre_mes_solicitud', y='id_producto', color="nombre_producto", labels={
                     "nombre_mes_solicitud": "Mes solicitud",
                     "id_producto": "Frecuencia",
                     "nombre_producto": "Producto"
                 })

    else: 
        df = df.groupby(['anio_solicitud','nombre_producto']).agg({'id_producto': 'count'})
        df = df.reset_index()
        df =df.astype({"anio_solicitud": str})
        fig = px.bar(df, x='anio_solicitud', y='id_producto', color="nombre_producto", labels={
                     "anio_solicitud": "Año solicitud",
                     "id_producto": "Frecuencia",
                     "nombre_producto": "Producto"
                 },)

    st.write(fig)
    
    st.write('Promedio de cantidad comprada')
    tipo_producto= st.selectbox(key="tipo_producto_r5_prom",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    anio = st.selectbox(key="anio_r5_prom",
     label='Año',
    options=(2019,2020,2021, 'Todos los años'))
    df=dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    if anio != 'Todos los años':
        df = df.loc[df['anio_solicitud'] == anio]
        df = df.groupby(['mes_solicitud','nombre_mes_solicitud','nombre_producto']).agg({'cantidad_solicitada': 'mean'})
        df = df.sort_values(['mes_solicitud'])
        df = df.reset_index()
        fig = px.bar(df, x='nombre_mes_solicitud', y='cantidad_solicitada', color="nombre_producto",labels={
                     "nombre_mes_solicitud": "Mes solicitud",
                     "cantidad_solicitada": "Promedio cantidad solicitada",
                     "nombre_producto": "Producto"
                 }, )

    else: 
        df = df.groupby(['anio_solicitud','nombre_producto']).agg({'cantidad_solicitada': 'mean'})
        df = df.reset_index()
        df =df.astype({"anio_solicitud": str})
        fig = px.bar(df, x='anio_solicitud', y='cantidad_solicitada', color="nombre_producto", labels={
                     "anio_solicitud": "Año solicitud",
                     "cantidad_solicitada": "Promedio cantidad solicitada",
                     "nombre_producto": "Producto"
                 })
    st.write(fig)

def requerimiento_5_alt(dataset):
    st.header('Frecuencia de compra por producto')
    st.write('Por mes')
    tipo_producto= st.selectbox(key="tipo_producto_r5_alt",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    anio = st.selectbox(key="anio_r5_alt",
     label='Año',
    options=(2019,2020,2021, 'Todos los años'))
    df=dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    if anio != 'Todos los años':
        df = df.loc[df['anio_solicitud'] == anio]
        df = df.groupby(['mes_solicitud','nombre_mes_solicitud','nombre_producto']).agg({'id_producto': 'count'})
        df = df.reset_index()
        df = df.groupby(['nombre_producto']).agg({'id_producto': 'mean'})
        df = df.reset_index()

        fig = px.bar(df, x='nombre_producto', y='id_producto', labels={
                     "id_producto": "Frecuencia de compra por mes",
                     "nombre_producto": "Producto"
                 })

    else: 
        df = df.groupby(['mes_solicitud','nombre_mes_solicitud','nombre_producto']).agg({'id_producto': 'count'})
        df = df.reset_index()
        df = df.groupby(['nombre_producto']).agg({'id_producto': 'mean'})
        df = df.reset_index()
        fig = px.bar(df, x='nombre_producto', y='id_producto',labels={
                     "id_producto": "Frecuencia de compra por mes",
                     "nombre_producto": "Producto"
                 },)
    st.write(fig)

    st.write('Por año')
    df_anual=dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    df_anual = df_anual.groupby(['anio_solicitud', 'nombre_producto']).agg({'id_producto': 'count'})
    df_anual = df_anual.reset_index()
    df_anual =df_anual.astype({"anio_solicitud": str})
    df_anual = df_anual.groupby(['nombre_producto']).agg({'id_producto': 'mean'})
    df_anual = df_anual.reset_index()
    fig_anual = px.bar(df_anual, x='nombre_producto', y='id_producto',labels={
                     "id_producto": "Frecuencia de compra anual",
                     "nombre_producto": "Producto"
                 },)

    st.write(fig_anual)
    
    st.header('Promedio de cantidad solicitada por producto')
    tipo_producto= st.selectbox(key="tipo_producto_r5_prom_alt",
     label='Tipo Producto',
    options=('Ingrediente', 'Packaging', 'Insumo descartable'))
    anio = st.selectbox(key="anio_r5_prom_alt",
     label='Año',
    options=(2019,2020,2021, 'Todos los años'))
    df=dataset.loc[dataset['nombre_tipo_producto'] == tipo_producto]
    if anio != 'Todos los años':
        df = df.loc[df['anio_solicitud'] == anio]
        meses_dataset = sorted(df.mes_solicitud.unique())
        op_meses = list(map(lambda x : meses[x - 1], meses_dataset))
        op_meses.append('Todos los meses')
        mes = st.selectbox(key="mes_r_alt",
     label='Mes', options=op_meses)
        if mes != 'Todos los meses':
            df = df.loc[df['nombre_mes_solicitud'] == mes]
        df = df.groupby(['nombre_producto']).agg({'cantidad_solicitada': 'mean'})
        df = df.reset_index()
        fig = px.bar(df, x='nombre_producto', y='cantidad_solicitada', labels={
                     "cantidad_solicitada": "Promedio cantidad solicitada",
                     "nombre_producto": "Producto"
                 }, )

    else: 
        df = df.groupby(['anio_solicitud','nombre_producto']).agg({'cantidad_solicitada': 'mean'})
        df = df.reset_index()
        df =df.astype({"anio_solicitud": str})
        fig = px.bar(df, x='anio_solicitud', y='cantidad_solicitada', color="nombre_producto", labels={
                     "anio_solicitud": "Año solicitud",
                     "cantidad_solicitada": "Promedio cantidad solicitada",
                     "nombre_producto": "Producto"
                 })
    st.write(fig)

def requerimiento_8(df):
    st.header("Histórico de precio de compra por producto")
    producto = st.selectbox(key="id_producto",
     label='Producto',
    options= list(df["nombre_producto"].unique()))
    df=df.loc[df['nombre_producto'] == producto]
    df = df.groupby(['nombre_producto', 'mes_recepcion', 'nombre_mes_recepcion', 'anio_recepcion']).agg({'precio_unitario': 'mean'}).sort_values(by=['anio_recepcion', 'mes_recepcion'])
    df_to_show = df.rename(columns={'precio_unitario': 'Precio unitario'})
    st.write(df_to_show)
    df = df.reset_index()
    df = df.sort_values(['mes_recepcion'])
    df =df.astype({"anio_recepcion": str})
    fig = px.bar(df, x='nombre_mes_recepcion', y='precio_unitario' , color="anio_recepcion", labels={
                     "nombre_mes_recepcion": "Mes recepción",
                     "precio_unitario": "Promedio precio unitario",
                     "anio_recepcion": "Año recepción"
                 })
    fig.update_layout(xaxis_title="Mes", yaxis_title="Precio unitario", legend_title="Años")
    st.write(fig)

def requerimiento_10(df, meses):
    st.header("Tipos de ingredientes más solicitados por mes")
    meses_dataset = sorted(df.mes_solicitud.unique())
    mes = st.selectbox(key="mes_r2",
     label='Mes', options=list(map(lambda x : meses[x - 1], meses_dataset)))
    df = df.loc[df['nombre_mes_solicitud'] == mes]
    df = df.groupby(['nombre_tipo_producto']).agg({'cantidad_solicitada': 'sum'}).sort_values(by=['cantidad_solicitada'])
    df = df.rename(columns={'cantidad_solicitada': 'Cantidad Solicitada', 'cantidad_recibida': 'Cantidad Recibida'})

    st.write(df)


def LoadPage(dataset):
    meses = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo','Junio','Julio','Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ]
    
    st.title("Requerimientos relacionados a los productos")

    requerimiento_1(dataset)

    requerimiento_2(dataset, meses)

    requerimiento_5_alt(dataset)

    requerimiento_8(dataset)

    requerimiento_10(dataset, meses)
    
