import streamlit as st
import pandas as pd

def LoadPage(dataset):
    st.title("Requerimientos relacionados a proveedores")
    st.write("Set de datos:")
    st.write(dataset)

    st.header("Proveedores con mayor cantidad de productos entregados por mes.")
    data_prov_1 = dataset[dataset["id_proveedor"] == 1]
    st.write(data_prov_1)