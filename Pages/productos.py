import streamlit as st
import pandas as pd
import plotly.express as px

def requerimiento_1(dataset):
    st.header('1 - Porcentajes de ingredientes solicitados por mes')
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
        df_r1 = df_r1.groupby(['mes_solicitud', 'nombre_mes_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
        df_r1['Porcentaje'] = df_r1.groupby(['mes_solicitud']).apply(lambda x:100 * x / float(x.sum()))
        df_r1 = df_r1.reset_index()
        #df_r1_mes =df_r1_mes.astype({"anio_solicitud": str})
        #df_r1_mes['mes_anio'] = df_r1_mes[['nombre_mes_solicitud', 'anio_solicitud']].agg(' '.join, axis=1)
        df_r1 = df_r1.sort_values(['mes_solicitud'])
        fig = px.bar(df_r1, x='nombre_mes_solicitud', y='Porcentaje', color="nombre_producto")
 
    else:
        df_r1 = df_r1.groupby(['anio_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
        df_r1['Porcentaje'] = df_r1.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_r1 = df_r1.reset_index()
        df_r1 =df_r1.astype({"anio_solicitud": str})
        fig = px.bar(df_r1, x='anio_solicitud', y='Porcentaje', color="nombre_producto")
    st.write(fig)

def requerimiento_2(dataset, meses):
    st.header('2 - Relación de cantidad solicitada y entregada por producto por proveedor')
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
    st.write(df_r2_anio)

def requerimiento_5(dataset):
    st.header('5 y 9 - Promedio de compras de productos por mes')
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
        fig = px.bar(df, x='nombre_mes_solicitud', y='id_producto', color="nombre_producto")
    else: 
        df = df.groupby(['anio_solicitud','nombre_producto']).agg({'id_producto': 'count'})
        df = df.reset_index()
        df =df.astype({"anio_solicitud": str})
        fig = px.bar(df, x='anio_solicitud', y='id_producto', color="nombre_producto")
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
        fig = px.bar(df, x='nombre_mes_solicitud', y='cantidad_solicitada', color="nombre_producto")
    else: 
        df = df.groupby(['anio_solicitud','nombre_producto']).agg({'cantidad_solicitada': 'mean'})
        df = df.reset_index()
        df =df.astype({"anio_solicitud": str})
        fig = px.bar(df, x='anio_solicitud', y='cantidad_solicitada', color="nombre_producto")
    st.write(fig)




def LoadPage(dataset):
    meses = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo','Junio','Julio','Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ]
    
    requerimiento_1(dataset)

    requerimiento_2(dataset, meses)

    requerimiento_5(dataset)
    
