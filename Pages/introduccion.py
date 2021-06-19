# Importacion de modulos de terceros
import streamlit as st

def LoadPage():
    st.title('Inteligencia de Negocios - Don Cayetano')
    for i in range(3):
        st.write('')
    st.subheader('Business Intelligence - Trabajo Práctico Integrador')
   
    st.header('💬Sobre la Aplicación')
    st.write('En el menú lateral usted podrá navegar por los distintos requerimientos.')

    st.subheader('Integrantes del grupo:')
    st.write('- Azábal, Dahyana')
    st.write('- Chiavassa, Agustín')
    st.write('- González, Lautaro Iván')
