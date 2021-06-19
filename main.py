#Importacion modulos de terceros
import streamlit as st
import pandas as pd
## import psycopg2
from sqlalchemy import create_engine

#Importacion Paginas
import Pages.introduccion as introduccion
import Pages.requerimientos as requerimientos


# Conexion BD
alchemyEngine=create_engine(f"postgresql+psycopg2://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}/{st.secrets['dbname']}", pool_recycle=3600)
dbConnection=alchemyEngine.connect()

dataFrame=pd.read_sql("select * from hechos_compras hc join fechas_solicitudes fs on fs.id_fecha_solicitud = hc.id_fecha_solicitud ", dbConnection)
pd.set_option('display.expand_frame_repr', False);

##dataFrame = dataFrame.groupby(by="nombre_mes").sum()
dbConnection.close()

def CreateLayout():
    st.sidebar.title("Menú")
    app_mode = st.sidebar.selectbox("Seleccione una página:",
                                    ["Introducción", "Requerimientos"])
    
    if app_mode == 'Introducción':
        introduccion.LoadPage()
    elif app_mode == 'Requerimientos':
        requerimientos.LoadPage(dataFrame)
    else:
        pass


if __name__ == "__main__":
    CreateLayout()