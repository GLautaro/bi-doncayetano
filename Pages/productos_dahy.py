import streamlit as st
import plotly.express as px

def requerimiento_8(df):
    st.header("8 - Histórico de precio de compra por producto")
    producto = st.selectbox(key="id_producto",
     label='Producto',
    options= list(df["nombre_producto"].unique()))
    df=df.loc[df['nombre_producto'] == producto]
    df = df.groupby(['nombre_producto', 'mes_recepcion', 'nombre_mes_recepcion', 'anio_recepcion']).agg({'precio_unitario': 'mean'}).sort_values(by=['anio_recepcion', 'mes_recepcion'])
    st.write(df)
    df = df.reset_index()
    fig = px.bar(df, x='nombre_mes_recepcion', y='precio_unitario')
    st.write(fig)

def requerimiento_10(df, meses):
    st.header("10 - Tipos de ingredientes más solicitados por mes")
    meses_dataset = sorted(df.mes_solicitud.unique())
    mes = st.selectbox(key="mes_r2",
     label='Mes', options=list(map(lambda x : meses[x - 1], meses_dataset)))
    df = df.loc[df['nombre_mes_solicitud'] == mes]
    df = df.groupby(['nombre_tipo_producto']).agg({'cantidad_solicitada': 'sum'}).sort_values(by=['cantidad_solicitada'])
    st.write(df)


def LoadPage(df):
    meses = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo','Junio','Julio','Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ]
    requerimiento_8(df)
    requerimiento_10(df, meses)
