import streamlit as st
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(page_title="Proyecto 1 - Python Fundamentals", layout="wide")

# Inicialización de variables en Session State (Persistencia de Datos)
if "flujo_caja" not in st.session_state:
    st.session_state.flujo_caja = []

if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])

if "historial_funciones" not in st.session_state:
    st.session_state.historial_funciones = pd.DataFrame(columns=["Parámetro", "Resultado"])

# Menú Lateral de Navegación
opcion = st.sidebar.selectbox(
    "Navegación",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# ==========================================
# 1. HOME
# ==========================================
if opcion == "Home":
    st.title("Proyecto Aplicado - Python Fundamentals")
    st.subheader("Especialización en Python for Analytics")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # st.image("logo.png", width=150) # Opcional
        pass
    with col2:
        st.markdown("**Estudiante:** Tu Nombre Completo")
        st.markdown("**Módulo:** Módulo 1 - Python Fundamentals")
        st.markdown("**Año:** 2026")
    
    st.divider()
    st.markdown("### Descripción del Proyecto")
    st.write("Esta aplicación integra los fundamentos de programación revisados en el Módulo 1, cubriendo el uso de listas, arreglos con NumPy, DataFrames en Pandas, funciones externas y la implementación de programación orientada a objetos (POO) con operaciones CRUD.")

# ==========================================
# 2. EJERCICIO 1: Flujo de Caja
# ==========================================
elif opcion == "Ejercicio 1":
    st.header("Ejercicio 1: Flujo de Caja con Listas")
    st.markdown("Registro de movimientos financieros personales o institucionales.")
    
    col1, col2, col3 = st.columns(3)
    concepto = col1.text_input("Concepto")
    tipo = col2.selectbox("Tipo de Movimiento", ["Ingreso", "Gasto"])
    valor = col3.number_input("Valor", min_value=0.0, step=10.0)
    
    if st.button("Agregar Movimiento"):
        if concepto:
            st.session_state.flujo_caja.append({"Concepto": concepto, "Tipo": tipo, "Valor": valor})
            st.success("Movimiento registrado con éxito.")
        else:
            st.warning("Por favor ingrese un concepto.")

    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)
        
        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = ingresos - gastos
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"S/ {ingresos:,.2f}")
        m2.metric("Total Gastos", f"S/ {gastos:,.2f}")
        m3.metric("Saldo Final", f"S/ {saldo:,.2f}")
        
        if saldo >= 0:
            st.success("El flujo de caja está **A FAVOR**.")
        else:
            st.error("El flujo de caja está **EN CONTRA**.")

# ==========================================
# 3. EJERCICIO 2: NumPy & DataFrames
# ==========================================
elif opcion == "Ejercicio 2":
    st.header("Ejercicio 2: Registro con NumPy y DataFrames")
    
    with st.form("form_registro"):
        prod = st.text_input("Nombre del Producto")
        cat = st.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios"])
        precio = st.number_input("Precio Unitario", min_value=0.0)
        cant = st.number_input("Cantidad", min_value=1, step=1)
        submitted = st.form_submit_button("Agregar Registro")
        
        if submitted and prod:
            # Procesamiento con NumPy
            arr_datos = np.array([prod, cat, precio, cant, precio * cant])
            nuevo_df = pd.DataFrame([arr_datos], columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo_df], ignore_index=True)
            st.success("Registro añadido.")
            
    st.dataframe(st.session_state.inventario, use_container_width=True)

# ==========================================
# 4. EJERCICIO 3: Funciones
# ==========================================
elif opcion == "Ejercicio 3":
    st.header("Ejercicio 3: Funciones Externas")
    # import libreria_funciones_proyecto1 as lfunc
    st.info("Conecta aquí tus funciones del archivo 'libreria_funciones_proyecto1.py'.")

# ==========================================
# 5. EJERCICIO 4: Clases & CRUD
# ==========================================
elif opcion == "Ejercicio 4":
    st.header("Ejercicio 4: Clases Externas y Operaciones CRUD")
    # import libreria_clases_proyecto1 as lclase
    st.info("Implementa aquí el CRUD de las clases de 'libreria_clases_proyecto1.py'.")
