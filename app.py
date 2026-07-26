import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# Importamos las librerías con las funciones y clases del proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# ARCHIVO DE PERSISTENCIA
ARCHIVO_PERSISTENCIA = "datos_guardados.json"

# =========================================================
# FUNCIONES DE PERSISTENCIA DE DATOS
# =========================================================
def cargar_datos_disco():
    if os.path.exists(ARCHIVO_PERSISTENCIA):
        try:
            with open(ARCHIVO_PERSISTENCIA, "r", encoding="utf-8") as f:
                datos = json.load(f)
                st.session_state.flujo_caja = datos.get("flujo_caja", [])
                st.session_state.empleados_crud = datos.get("empleados_crud", [])
                st.session_state.contador_id = datos.get("contador_id", 1)
                
                historial_dict = datos.get("historial_funciones", [])
                st.session_state.historial_funciones = pd.DataFrame(historial_dict) if historial_dict else pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])
                
                inventario_dict = datos.get("inventario", [])
                st.session_state.inventario = pd.DataFrame(inventario_dict) if inventario_dict else pd.DataFrame(columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"])
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")

def guardar_datos_disco():
    try:
        datos = {
            "flujo_caja": st.session_state.flujo_caja,
            "empleados_crud": st.session_state.empleados_crud,
            "contador_id": st.session_state.contador_id,
            "inventario": st.session_state.inventario.to_dict(orient="records"),
            "historial_funciones": st.session_state.historial_funciones.to_dict(orient="records")
        }
        with open(ARCHIVO_PERSISTENCIA, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error al guardar datos: {e}")

# =========================================================
# CONFIGURACIÓN Y ESTILOS
# =========================================================
st.set_page_config(page_title="Analytics System", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b !important; }
    h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; font-weight: 700 !important; }
    div[data-testid="stExpander"] { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# INICIALIZACIÓN
if "inicializado" not in st.session_state:
    st.session_state.flujo_caja = []
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"])
    st.session_state.historial_funciones = pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1
    cargar_datos_disco()
    st.session_state.inicializado = True

# NAVEGACIÓN
with st.sidebar:
    st.markdown("### 🗂️ Navegación")
    opcion = st.selectbox("Seleccione un módulo:", [
        "Inicio",
        "Ejercicio 1 - Flujo de Caja",
        "Ejercicio 2 - Inventario NumPy",
        "Ejercicio 3 - Crecimiento de Ventas",
        "Ejercicio 4 - Gestión de Empleados"
    ])

# =========================================================
# MÓDULOS ORGANIZADOS CON st.expander
# =========================================================

if opcion == "Inicio":
    st.title("Plataforma Analytics - Python Fundamentals")
    st.caption("Especialización en Python for Analytics")
    st.divider()
    
    with st.expander("📌 Ver Resumen General del Sistema", expanded=True):
        st.write(f"• Registros en caja: **{len(st.session_state.flujo_caja)}**")
        st.write(f"• Ítems en inventario: **{len(st.session_state.inventario)}**")
        st.write(f"• Personal registrado: **{len(st.session_state.empleados_crud)}**")

elif opcion == "Ejercicio 1 - Flujo de Caja":
    st.header("Ejercicio 1 - Flujo de Caja")
    
    # EXPANDER PARA FORMULARIO DE REGISTRO
    with st.expander("➕ Formulario: Registrar Nuevo Movimiento", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        concepto = c1.text_input("Concepto / Descripción")
        tipo = c2.selectbox("Tipo de Operación", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto (S/)", min_value=0.01, step=10.0, format="%.2f")

        if st.button("Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({"Concepto": concepto.strip(), "Tipo": tipo, "Valor (S/)": valor})
                guardar_datos_disco()
                st.toast("Movimiento guardado permanentemente.", icon="✅")
            else:
                st.warning("Ingrese un concepto válido.")

    # EXPANDER PARA CONSULTA DE DATOS
    with st.expander("📋 Ver Histórico de Transacciones", expanded=True):
        if st.session_state.flujo_caja:
            df_flujo = pd.DataFrame(st.session_state.flujo_caja)
            st.dataframe(df_flujo, use_container_width=True)
            ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor (S/)"].sum()
            gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor (S/)"].sum()
            st.metric("Saldo Neto", f"S/ {(ingresos - gastos):,.2f}")
        else:
            st.info("No hay transacciones registradas.")

elif opcion == "Ejercicio 2 - Inventario NumPy":
    st.header("Ejercicio 2 - Control de Inventario")

    with st.expander("📦 Formulario: Registrar Producto", expanded=True):
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio Unitario (S/)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad", min_value=1, step=1)

        if st.button("Agregar Producto", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])
                df_nuevo = pd.DataFrame(arr_registro, columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"])
                df_nuevo["Precio (S/)"] = df_nuevo["Precio (S/)"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total (S/)"] = df_nuevo["Total (S/)"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                guardar_datos_disco()
                st.toast(f"Producto '{prod_nombre}' guardado.", icon="✅")
            else:
                st.warning("Ingrese un nombre de producto.")

    with st.expander("📊 Ver Reporte de Inventario Consolidado", expanded=True):
        if not st.session_state.inventario.empty:
            st.dataframe(st.session_state.inventario, use_container_width=True)
            total_inv = st.session_state.inventario["Total (S/)"].sum()
            st.write(f"**Valorización Total del Stock:** S/ {total_inv:,.2f}")
        else:
            st.info("El inventario está vacío.")

elif opcion == "Ejercicio 3 - Crecimiento de Ventas":
    st.header("Ejercicio 3 - Tasa de Crecimiento de Ventas")

    with st.expander("📈 Calculadora de Crecimiento", expanded=True):
        col1, col2 = st.columns(2)
        v_ant = col1.number_input("Ventas Período Anterior (S/)", min_value=1.0, value=15000.0)
        v_act = col2.number_input("Ventas Período Actual (S/)", min_value=0.0, value=18500.0)

        if st.button("Ejecutar Cálculo", use_container_width=True, type="primary"):
            try:
                res = lfunc.calcular_tasa_crecimiento_ventas(v_ant, v_act)
                tasa_val = res['tasa_crecimiento_pct']
                diferencia = v_act - v_ant

                st.success(f"Tasa de Crecimiento: **{tasa_val}%** | Variación: **S/ {diferencia:,.2f}**")

                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_tasa_crecimiento_ventas",
                    "Parámetros Ingresados": f"Anterior=S/ {v_ant:,.2f} | Actual=S/ {v_act:,.2f}",
                    "Resultado": f"Tasa: {tasa_val}% | Dif: S/ {diferencia:,.2f}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                guardar_datos_disco()
            except Exception as e:
                st.error(f"Error: {e}")

    with st.expander("📜 Bitácora de Consultas", expanded=False):
        if not st.session_state.historial_funciones.empty:
            st.dataframe(st.session_state.historial_funciones, use_container_width=True)
        else:
            st.info("Sin registros.")

elif opcion == "Ejercicio 4 - Gestión de Empleados":
    st.header("Ejercicio 4 - Gestión de Personal (CRUD)")

    # EXPANDER DE ALTA DE EMPLEADOS
    with st.expander("➕ Registrar Empleado", expanded=True):
        c1, c2 = st.columns(2)
        emp_nombre = c1.text_input("Nombre Completo", key="crear_nombre")
        emp_salario = c2.number_input("Salario Base (S/)", min_value=1.0, value=2500.0, key="crear_salario")

        emp_bono = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0, key="crear_bono")
        emp_desc = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0, key="crear_desc")

        if st.button("Guardar Empleado", use_container_width=True, type="primary", key="btn_crear"):
            if emp_nombre.strip():
                try:
                    nuevo_emp = lclase.Empleado(emp_nombre.strip(), emp_salario, emp_bono, emp_desc)
                    resumen = nuevo_emp.resumen()
                    resumen["id"] = st.session_state.contador_id
                    resumen["pct_bono"] = emp_bono
                    resumen["pct_descuento"] = emp_desc

                    st.session_state.empleados_crud.append(resumen)
                    st.session_state.contador_id += 1
                    guardar_datos_disco()
                    st.toast("Empleado registrado permanentemente.", icon="✅")
                except Exception as e:
                    st.error(f"Error: {e}")

    # EXPANDER DE DIRECTORIO
    with st.expander("👥 Directorio de Personal Guardado", expanded=True):
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            cols = ["id", "nombre", "salario_base", "bono", "descuento", "salario_neto"]
            df_emp = df_emp[[c for c in cols if c in df_emp.columns]]
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No hay registros disponibles.")

    # EXPANDER DE EDICIÓN Y ELIMINACIÓN
    with st.expander("✏️ Editar o Eliminar Empleados", expanded=False):
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Seleccione ID:", lista_ids, key="select_id_gestion")
            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                col_ed1, col_ed2 = st.columns(2)
                up_nombre = col_ed1.text_input("Editar Nombre", value=emp_actual["nombre"], key=f"edit_nombre_{id_sel}")
                up_salario = col_ed2.number_input("Editar Salario (S/)", min_value=1.0, value=float(emp_actual["salario_base"]), key=f"edit_salario_{id_sel}")

                if st.button("Actualizar Cambios", key=f"btn_up_{id_sel}"):
                    idx = next(i for i, item in enumerate(st.session_state.empleados_crud) if item["id"] == id_sel)
                    st.session_state.empleados_crud[idx]["nombre"] = up_nombre
                    st.session_state.empleados_crud[idx]["salario_base"] = up_salario
                    guardar_datos_disco()
                    st.toast("Registro actualizado.", icon="✅")
                    st.rerun()

                if st.button("Eliminar Registro", type="primary", key=f"btn_del_{id_sel}"):
                    st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_sel]
                    guardar_datos_disco()
                    st.toast("Empleado eliminado.", icon="✅")
                    st.rerun()
