# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:39:31 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import random
import time

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Cargar los archivos .xlsx
@st.cache_resource
def cargar_datos():
    df_pensionissste = pd.read_excel('cuenta_habientes_pensionissste.xlsx')
    df_otras_afores = pd.read_excel('cuenta_habientes_otras_afores.xlsx')
    return df_pensionissste, df_otras_afores

# Función para simular las bajas de PENSIONISSSTE
def simular_bajas(df_pensionissste_actualizado, num_bajas):
    indices_bajas = random.sample(range(len(df_pensionissste_actualizado)), num_bajas)
    df_bajas = df_pensionissste_actualizado.iloc[indices_bajas]
    df_pensionissste_actualizado = df_pensionissste_actualizado.drop(indices_bajas)
    monto_bajas = df_bajas['Monto'].sum()
    return df_pensionissste_actualizado, df_bajas, monto_bajas

# Función para simular las altas de otras AFORES
def simular_altas(df_pensionissste_actualizado, df_otras_afores, num_altas):
    indices_altas = random.sample(range(len(df_otras_afores)), num_altas)
    df_altas = df_otras_afores.iloc[indices_altas]
    df_pensionissste_actualizado = pd.concat([df_pensionissste_actualizado, df_altas], ignore_index=True)
    monto_altas = df_altas['Monto'].sum()
    return df_pensionissste_actualizado, df_altas, monto_altas

# Función para mostrar estadísticas
def mostrar_estadisticas(df_pensionissste_actualizado):
    total_cuenta_habientes = len(df_pensionissste_actualizado)
    monto_total = df_pensionissste_actualizado['Monto'].sum()
    return total_cuenta_habientes, monto_total

# Configuración de la aplicación
st.title("Tablero: Simulación Automática de Bajas y Altas de Cuenta Habientes de AFORE PENSIONISSSTE en tiempo REAL")

# Cargar datos de los archivos
df_pensionissste, df_otras_afores = cargar_datos()

# Mostrar el DataFrame original de PENSIONISSSTE
st.subheader("Cuenta Habientes Originales de AFORE PENSIONISSSTE")
st.write(df_pensionissste)

# DataFrame para las actualizaciones en tiempo real
df_pensionissste_actualizado = df_pensionissste.copy()

# Mostrar el DataFrame actualizado
df_placeholder = st.empty()

# Inicializar y mostrar la primera vez las estadísticas y DataFrame
total_cuenta_habientes, monto_total = mostrar_estadisticas(df_pensionissste_actualizado)

# Placeholder para estadísticas generales
stats_placeholder = st.empty()
stats_placeholder.write(f"Total de cuenta habientes en AFORE PENSIONISSSTE: {total_cuenta_habientes}")
stats_placeholder.write(f"Monto total en AFORE PENSIONISSSTE: ${monto_total:,.2f}")

# Variables para llevar el conteo de bajas y altas
total_bajas = 0
total_altas = 0
monto_bajas_total = 0.0
monto_altas_total = 0.0

# Placeholder para el tercer DataFrame (resumen de bajas y altas)
resumen_placeholder = st.empty()

# Sección de ayuda en la barra lateral
st.sidebar.title("Ayuda")
st.sidebar.write("""
**Simulación Automática de Bajas y Altas**

Esta aplicación simula las bajas y altas automáticas de cuenta habientes de AFORE PENSIONISSSTE. Los datos se actualizan en tiempo real, y puedes ver el resumen en las tablas presentadas.

**¿Cómo funciona?**
1. En cada iteración, se genera un número aleatorio de bajas y altas.
2. **Bajas**: Los cuenta habientes de PENSIONISSSTE se reducen en cada iteración, y el monto total de las bajas se calcula y se muestra en la sección de resumen.
3. **Altas**: Se agregan cuenta habientes de otras AFORES y se calcula el monto total de las altas en cada iteración.
4. Los resultados se actualizan en las estadísticas generales y en el resumen de bajas y altas.

**Montos por Altas y Bajas**
- El monto total de **bajas** es la suma de los montos de los cuenta habientes eliminados en cada iteración.
- El monto total de **altas** es la suma de los montos de los nuevos cuenta habientes agregados de otras AFORES.

**Nota**: La simulación continuará mientras la aplicación esté en ejecución.
""")
st.sidebar.write("Desarrollado por Javier Horacio Pérez Ricárdez")
st.sidebar.write("© 2024")

# Simulación automática
max_cuentas = 600  # Límite máximo de cuentas

while True:
    # Generar números aleatorios para bajas y altas de forma independiente
    num_bajas = random.randint(0, 3)  # Número aleatorio de bajas entre 0 y 3
    num_altas = random.randint(0, 3)  # Número aleatorio de altas entre 0 y 3

    # Simular bajas
    if num_bajas > 0 and len(df_pensionissste_actualizado) >= num_bajas:
        df_pensionissste_actualizado, df_bajas, monto_bajas = simular_bajas(df_pensionissste_actualizado, num_bajas)
        total_bajas += len(df_bajas)
        monto_bajas_total += monto_bajas
    else:
        monto_bajas = 0  # Si no hay bajas, el monto es 0

    # Simular altas si no se ha alcanzado el límite de cuentas
    if num_altas > 0 and total_cuenta_habientes < max_cuentas:
        df_pensionissste_actualizado, df_altas, monto_altas = simular_altas(df_pensionissste_actualizado, df_otras_afores, num_altas)
        total_altas += len(df_altas)
        monto_altas_total += monto_altas
    else:
        monto_altas = 0  # Si no hay altas, el monto es 0

    # Actualizar el DataFrame y estadísticas en tiempo real
    total_cuenta_habientes, monto_total = mostrar_estadisticas(df_pensionissste_actualizado)

    # Mostrar el DataFrame actualizado
    df_placeholder.empty()  # Limpiar el DataFrame previo
    df_placeholder.write(df_pensionissste_actualizado)  # Mostrar DataFrame actualizado

    # Actualizar las estadísticas generales
    stats_placeholder.empty()  # Limpiar las estadísticas previas
    stats_placeholder.write(f"Total de cuenta habientes en AFORE PENSIONISSSTE: {total_cuenta_habientes}")
    stats_placeholder.write(f"Monto total en AFORE PENSIONISSSTE: ${monto_total:,.2f}")

    # Crear el DataFrame resumen para bajas y altas
    resumen_df = pd.DataFrame({
        'Descripción': ['Bajas', 'Altas', 'Total Cuenta Habientes'],
        'Monto Total': [monto_bajas_total, monto_altas_total, monto_total],
        'Cuentas Totales': [total_bajas, total_altas, total_cuenta_habientes]
    })

    # Mostrar el DataFrame resumen de bajas y altas
    resumen_placeholder.empty()
    resumen_placeholder.write("Resumen de Bajas y Altas")
    resumen_placeholder.write(resumen_df)

    # Pausar para que se vea el cambio
    time.sleep(2)  # Esperar 2 segundos antes de mostrar la siguiente actualización
    time.sleep(3)  # Esperar 3 segundos antes de realizar una nueva simulación
