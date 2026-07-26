import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# Importamos las librerías con las funciones y clases del proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# ARCHIVO LOCAL DONDE SE GUARDARÁN LOS DATOS PERMANENTEMENTE
ARCHIVO_PERSISTENCIA = "datos_guardados.json"

# =========================================================
# FUNCIONES DE PERSISTENCIA (CARGAR Y GUARDAR EN DISCO)
# =========================================================
def cargar_datos_disco():
    """Carga los datos guardados en el archivo JSON al iniciar la app."""
    if os.path.exists(ARCHIVO_PERSISTENCIA):
        try:
            with open(ARCHIVO_PERSISTENCIA, "r", encoding="utf-8") as f:
                datos = json.load(f)
                
                # Carga de listas y contadores
                st.session_state.flujo_caja = datos.get("flujo_caja", [])
                st.session_state.empleados_crud = datos.get("empleados_crud", [])
                st.session_state.contador_id = datos.get("contador_id", 1)
                
                # Reconstrucción de DataFrames de Pandas
                historial_dict = datos.get("historial_funciones", [])
                st.session_state.historial_funciones = pd.DataFrame(historial_dict) if historial_dict else pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])
                
                inventario_dict = datos.get("inventario", [])
                st.session_state.inventario = pd.DataFrame(inventario_dict) if inventario_dict else pd.DataFrame(columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"])
        except Exception as e:
            st.error(f"Error al cargar la base de datos persistente: {e}")

def guardar_datos_disco():
    """Guarda el estado actual de session_state en el archivo JSON."""
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
        st.error(f"Error al guardar datos en disco: {e}")


# =========================================================
# CONFIGURACIÓN GENERAL Y ESTILOS DARK TECH / AZUL ÍNDIGO
# =========================================================
st.set_page_config(
    page_title="Analytics System - Dark Tech Edition",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b !important; }
    h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; font-weight: 700 !important; }
    [data-testid="stForm"], div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background-color: #1e293b !important; border-radius: 12px !important; border: 1px solid #334155 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }
    .card-dark-tech {
        background: #1e293b; border: 1px solid #0284c7; border-radius: 12px; padding: 20px; margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.15);
    }
    .card-metric-dark {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); border: 1px solid #38bdf8;
        border-radius: 12px; padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important; color: #ffffff !important;
        border: none !important; border-radius: 8px !important; padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important; box-shadow: 0 0 12px rgba(2, 132, 199, 0.4) !important; transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important; box-shadow: 0 0 20px rgba(2, 132, 199, 0.7) !important;
    }
    input, select, textarea { color: #f8fafc !important; }
    .stSelectbox > div > div { background-color: #0f172a !important; border: 1px solid #334155 !important; color: #f8fafc !important; border-radius: 8px !important; }
    button[data-baseweb="tab"] { color: #94a3b8 !important; }
    button[aria-selected="true"] { color: #38bdf8 !important; border-bottom-color: #38bdf8 !important; }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# INICIALIZACIÓN DE LA MEMORIA PERMANENTE
# =========================================================
if "inicializado" not in st.session_state:
    st.session_state.flujo_caja = []
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"])
    st.session_state.historial_funciones = pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1
    
    cargar_datos_disco()
    st.session_state.inicializado = True


# =========================================================
# MENÚ LATERAL DE NAVEGACIÓN
# =========================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3 style="margin-top: 8px; margin-bottom: 0; color: #f8fafc; font-size: 1.2rem; letter-spacing: 1px;">
                ANALYTICS<span style="color:#38bdf8;">PRO</span>
            </h3>
            <span style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px;">Core System 2026</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🗂️ Navegación")
    
    opcion = st.selectbox(
        "Seleccione un módulo:",
        [
            "Inicio",
            "Ejercicio 1 - Flujo de Caja",
            "Ejercicio 2 - Inventario NumPy",
            "Ejercicio 3 - Crecimiento de Ventas",
            "Ejercicio 4 - Gestión de Empleados"
        ]
    )
    
    st.divider()
    
    st.markdown("""
        <div class="card-dark-tech" style="padding: 14px; margin-top: 10px;">
            <span style="color:#38bdf8; font-weight:bold; font-size: 0.8rem; text-transform: uppercase;">Estado del Entorno</span>
            <p style="margin-top:6px; margin-bottom:2px; color:#cbd5e1; font-size: 0.85rem;"><b>Persistencia:</b> Activa (JSON)</p>
            <p style="margin-bottom:0; color:#cbd5e1; font-size: 0.85rem;"><b>Moneda:</b> Soles (S/)</p>
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# 1. INICIO / HOME
# =========================================================
if opcion == "Inicio":
    st.title("Plataforma Analytics - Python Fundamentals")
    st.caption("Especialización en Python for Analytics")
    st.divider()

    col_info, col_resumen = st.columns([2, 1])

    with col_info:
        st.markdown("### 👤 Datos del Proyecto")
        st.write("**Estudiante:** Juan Pérez")
        st.write("**Programa:** Python for Analytics")
        st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")
        st.write("**Año:** 2026")

    with col_resumen:
        with st.container(border=True):
            st.markdown("<h4 style='color:#38bdf8; font-size:1.05rem; margin-bottom:10px;'>📊 Métricas Persistidas</h4>", unsafe_allow_html=True)
            st.write(f"• Registros en caja: **{len(st.session_state.flujo_caja)}**")
            st.write(f"• Ítems en inventario: **{len(st.session_state.inventario)}**")
            st.write(f"• Personal registrado: **{len(st.session_state.empleados_crud)}**")

    st.divider()
    st.info("Los datos registrados en cualquiera de los módulos son guardados en tiempo real en la memoria local del servidor/PC.")


# =========================================================
# 2. EJERCICIO 1: FLUJO DE CAJA
# =========================================================
elif opcion == "Ejercicio 1 - Flujo de Caja":
    st.header("Ejercicio 1 - Flujo de Caja")
    st.caption("Gestión iterativa de transacciones financieras mediante listas de Python.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>➕ Registrar Movimiento</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])

        concepto = c1.text_input("Concepto / Descripción", placeholder="Ej. Pago de licencias informáticas")
        tipo = c2.selectbox("Tipo de Operación", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto (S/)", min_value=0.01, step=10.0, format="%.2f")

        if st.button("Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({
                    "Concepto": concepto.strip(),
                    "Tipo": tipo,
                    "Valor (S/)": valor
                })
                guardar_datos_disco()
                st.toast("Movimiento guardado permanentemente.", icon="✅")
            else:
                st.warning("Ingrese un concepto válido.")

    st.write("")
    st.markdown("### 📋 Registro de Movimientos")

    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)

        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor (S/)"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor (S/)"].sum()
        saldo = ingresos - gastos

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"S/ {ingresos:,.2f}")
        m2.metric("Total Gastos", f"S/ {gastos:,.2f}")
        m3.metric("Saldo Neto", f"S/ {saldo:,.2f}")
    else:
        st.info("No hay transacciones registradas.")


# =========================================================
# 3. EJERCICIO 2: INVENTARIO CON NUMPY
# =========================================================
elif opcion == "Ejercicio 2 - Inventario NumPy":
    st.header("Ejercicio 2 - Control de Inventario")
    st.caption("Estructuración de datos en matrices NumPy y Pandas DataFrames.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>📦 Captura de Producto</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto", placeholder="Ej. Laptops Corporativas")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio Unitario (S/)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad", min_value=1, step=1)

        if st.button("Agregar Producto", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])

                df_nuevo = pd.DataFrame(
                    arr_registro,
                    columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"]
                )

                df_nuevo["Precio (S/)"] = df_nuevo["Precio (S/)"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total (S/)"] = df_nuevo["Total (S/)"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                guardar_datos_disco()
                st.toast(f"Producto '{prod_nombre}' guardado en disco.", icon="✅")
            else:
                st.warning("Ingrese un nombre de producto.")

    st.write("")
    st.markdown("### 📊 Inventario Consolidado")

    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inv = st.session_state.inventario["Total (S/)"].sum()
        
        st.markdown(f"""
            <div class="card-dark-tech">
                <span style="color:#38bdf8; font-weight:bold; font-size: 0.85rem; text-transform: uppercase;">Valorización de Stock</span>
                <h2 style="color:#f8fafc; margin-top:5px; margin-bottom:0;">S/ {total_inv:,.2f} PEN</h2>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("El inventario se encuentra vacío.")


# =========================================================
# 4. EJERCICIO 3: TASA DE CRECIMIENTO DE VENTAS
# =========================================================
elif opcion == "Ejercicio 3 - Crecimiento de Ventas":
    st.header("Ejercicio 3 - Tasa de Crecimiento de Ventas")
    st.caption("Cálculo comercial automatizado con la librería `libreria_funciones_proyecto1.py`.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>📈 Análisis Comparativo de Ventas</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        v_ant = col1.number_input("Ventas Período Anterior (S/)", min_value=1.0, value=15000.0, step=500.0)
        v_act = col2.number_input("Ventas Período Actual (S/)", min_value=0.0, value=18500.0, step=500.0)

        if st.button("Ejecutar Cálculo", use_container_width=True, type="primary"):
            try:
                res = lfunc.calcular_tasa_crecimiento_ventas(
                    ventas_periodo_anterior=v_ant, 
                    ventas_periodo_actual=v_act
                )
                
                tasa_val = res['tasa_crecimiento_pct']
                diferencia = v_act - v_ant

                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.markdown(f"""
                        <div class="card-metric-dark">
                            <span style="color:#38bdf8; font-weight:bold; font-size:0.85rem; text-transform:uppercase;">Tasa de Crecimiento</span>
                            <h1 style="color:#f8fafc; margin:5px 0; font-size:2.2rem;">{tasa_val}%</h1>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_res2:
                    st.markdown(f"""
                        <div class="card-metric-dark">
                            <span style="color:#38bdf8; font-weight:bold; font-size:0.85rem; text-transform:uppercase;">Variación Absoluta</span>
                            <h1 style="color:#f8fafc; margin:5px 0; font-size:2.2rem;">S/ {diferencia:,.2f}</h1>
                        </div>
                    """, unsafe_allow_html=True)

                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_tasa_crecimiento_ventas",
                    "Parámetros Ingresados": f"Anterior=S/ {v_ant:,.2f} | Actual=S/ {v_act:,.2f}",
                    "Resultado": f"Tasa: {tasa_val}% | Dif: S/ {diferencia:,.2f}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                guardar_datos_disco()
                
            except Exception as e:
                st.error(f"Error en la ejecución: {e}")

    st.write("")
    st.markdown("### 📜 Bitácora de Cálculos")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("No hay cálculos guardados.")


# =========================================================
# 5. EJERCICIO 4: GESTIÓN DE EMPLEADOS (POO Y CRUD)
# =========================================================
elif opcion == "Ejercicio 4 - Gestión de Empleados":
    st.header("Ejercicio 4 - Gestión de Personal (CRUD)")
    st.caption("Administración de colaboradores utilizando la clase `Empleado`.")

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(["Registrar", "Directorio", "Editar", "Eliminar"])

    # CREAR
    with tab_crear:
        with st.container(border=True):
            st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>➕ Alta de Empleado</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            emp_nombre = c1.text_input("Nombre Completo", placeholder="Ej. Lucía Alarcón", key="crear_nombre")
            emp_salario = c2.number_input("Salario Base (S/)", min_value=1.0, value=2500.0, step=100.0, key="crear_salario")

            c3, c4 = c1, c2
            emp_bono = c3.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0, key="crear_bono")
            emp_desc = c4.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0, key="crear_desc")

            if st.button("Guardar Empleado", use_container_width=True, type="primary", key="btn_crear"):
                if emp_nombre.strip():
                    try:
                        nuevo_emp = lclase.Empleado(
                            nombre=emp_nombre.strip(),
                            salario_base=emp_salario,
                            porcentaje_bono=emp_bono,
                            porcentaje_descuento=emp_desc
                        )

                        resumen = nuevo_emp.resumen()
                        resumen["id"] = st.session_state.contador_id
                        resumen["pct_bono"] = emp_bono
                        resumen["pct_descuento"] = emp_desc

                        st.session_state.empleados_crud.append(resumen)
                        st.session_state.contador_id += 1
                        
                        guardar_datos_disco()
                        st.toast(f"Empleado ID {resumen['id']} registrado permanentemente.", icon="✅")
                    except Exception as e:
                        st.error(f"Error al registrar: {e}")
                else:
                    st.warning("Ingrese un nombre válido.")

    # LEER
    with tab_leer:
        st.markdown("### Directorio de Personal")
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            cols = ["id", "nombre", "salario_base", "pct_bono", "bono", "pct_descuento", "descuento", "salario_neto"]
            df_emp = df_emp[[c for c in cols if c in df_emp.columns]]
            df_emp = df_emp.rename(columns={
                "salario_base": "Salario Base (S/)",
                "bono": "Bono (S/)",
                "descuento": "Descuento (S/)",
                "salario_neto": "Salario Neto (S/)"
            })
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No hay registros disponibles.")

    # ACTUALIZAR (CLAVE: SE AGREGARON KEYS ÚNICAS PARA EVITAR EL DUPLICATE ELEMENT ID)
    with tab_actualizar:
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Seleccione el ID a editar:", lista_ids, key="select_id_editar")
            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                with st.container(border=True):
                    st.markdown(f"<h4 style='color:#38bdf8; font-size:1.1rem;'>Editar Registro (ID: {id_sel})</h4>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    up_nombre = c1.text_input("Nombre Completo", value=emp_actual["nombre"], key=f"edit_nombre_{id_sel}")
                    up_salario = c2.number_input("Salario Base (S/)", min_value=1.0, value=float(emp_actual["salario_base"]), key=f"edit_salario_{id_sel}")

                    up_bono = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_bono", 0)), key=f"edit_bono_{id_sel}")
                    up_desc = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_descuento", 0)), key=f"edit_desc_{id_sel}")

                    if st.button("Actualizar Registro", use_container_width=True, type="primary", key=f"btn_edit_{id_sel}"):
                        try:
                            obj_modificado = lclase.Empleado(
                                nombre=up_nombre.strip(),
                                salario_base=up_salario,
                                porcentaje_bono=up_bono,
                                porcentaje_descuento=up_desc
                            )

                            resumen = obj_modificado.resumen()
                            resumen["id"] = id_sel
                            resumen["pct_bono"] = up_bono
                            resumen["pct_descuento"] = up_desc

                            idx = next(i for i, item in enumerate(st.session_state.empleados_crud) if item["id"] == id_sel)
                            st.session_state.empleados_crud[idx] = resumen
                            
                            guardar_datos_disco()
                            st.toast("Registro actualizado en disco.", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al actualizar: {e}")
        else:
            st.info("No existen registros para actualizar.")

    # ELIMINAR
    with tab_eliminar:
        if st.session_state.empleados_crud:
            lista_ids_del = [e["id"] for e in st.session_state.empleados_crud]
            id_del = st.selectbox("Seleccione el ID a eliminar:", lista_ids_del, key="del_select")
            emp_del = next((item for item in st.session_state.empleados_crud if item["id"] == id_del), None)

            if emp_del:
                with st.container(border=True):
                    st.info(f"¿Confirma la eliminación de **{emp_del['nombre']}** (ID: {id_del})?")
                    if st.button("Confirmar Eliminación", type="primary", use_container_width=True, key=f"btn_del_{id_del}"):
                        st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                        
                        guardar_datos_disco()
                        st.toast("Empleado eliminado.", icon="✅")
                        st.rerun()
        else:
            st.info("No hay registros para eliminar.")
