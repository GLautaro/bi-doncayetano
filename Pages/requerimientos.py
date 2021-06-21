import streamlit as st

def LoadPage(df):
    st.title("Requerimientos")
    st.write("Set de datos:")
    st.write(df)
    st.header('Requerimiento 1 - Porcentajes de ingredientes solicitados por mes/año')
    #Requerimiento 1 - Mes
    st.write('Por mes')
    df_r1_mes = df.loc[df['id_tipo_producto'] == 1]
    df_r1_mes = df_r1_mes.groupby(['nombre_mes_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
    df_r1_mes['Porcentaje'] = df_r1_mes.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
    st.write(df_r1_mes)
    #Requerimiento 1 - Anio
    st.write('Por año')
    df_r1_anio = df.loc[df['id_tipo_producto'] == 1]
    df_r1_anio = df_r1_anio.groupby(['anio_solicitud', 'nombre_producto']).agg({'cantidad_solicitada': 'sum'})
    df_r1_anio['Porcentaje'] = df_r1_anio.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
    st.write(df_r1_anio)
    st.header('Requerimiento 2')
    #Requerimiento 2  - Mes
    st.write('Por mes')
    df_r2_mes = df.loc[df['id_tipo_producto'] == 1]
    df_r2_mes = df_r2_mes.groupby(['nombre_producto', 'nombre_proveedor', 'nombre_mes_solicitud']).agg({'cantidad_solicitada': 'sum', 'cantidad_recibida':'sum'})
    st.write(df_r2_mes)
    #Requerimiento 2  - Anio
    st.write('Por año')
    df_r2_anio = df.loc[df['id_tipo_producto'] == 1]
    df_r2_anio = df_r2_anio.groupby(['nombre_producto', 'nombre_proveedor', 'anio_solicitud']).agg({'cantidad_solicitada': 'sum', 'cantidad_recibida':'sum'})
    st.write(df_r2_anio)
    st.header('Requerimiento 3')
    #Requerimiento 3 - Mes
    st.write('Por mes')
    df_r3_mes = df.groupby(['nombre_mes_solicitud', 'nombre_proveedor']).agg({'cantidad_solicitada': 'sum','cantidad_recibida': 'sum'})
    df_r3_mes['cantidad_perdida'] =  df_r3_mes['cantidad_solicitada'] - df_r3_mes['cantidad_recibida']
    df_r3_mes['porcentaje_perdida'] = df_r3_mes.apply(lambda x:100 * x.cantidad_perdida / x.cantidad_solicitada,axis=1)
    st.write(df_r3_mes)
 