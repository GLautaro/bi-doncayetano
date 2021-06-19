import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

alchemyEngine=create_engine(f"postgresql+psycopg2://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}/{st.secrets['db']}", pool_recycle=3600)
dbConnection=alchemyEngine.connect()


dataFrame=pd.read_sql("select * from hechos_compras hc join fechas_solicitudes fs on fs.id_fecha_solicitud = hc.id_fecha_solicitud ", dbConnection)

pd.set_option('display.expand_frame_repr', False);


dataFrame = dataFrame.groupby(by="nombre_mes").sum()


dbConnection.close()

st.title('BI - Don Cayetanos')


st.text('Desarrollo de los requerimientos solicitados')
st.dataframe(dataFrame)
