import streamlit as st
import pandas as pd
import numpy as np

# Importamos las librerías con las funciones y clases del proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# =========================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# =========================================================
st.set_page_config(
    page_title="Analytics System - Dark Tech Edition",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# DISEÑO CSS: ESTILO DARK TECH / AZUL ÍNDIGO ELEGANTE
# =========================================================
st.markdown("""
    <style>
    /* Fondo principal modo oscuro - Azul Índigo / Noche */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }

    /* Menú Lateral Oscuro */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Personalización de Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    /* Estilo para Tarjetas y Contenedores */
    [data-testid="stForm"], div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background-color: #1e293b !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }

    /* Tarjeta Dark Tech con borde neón azulino */
    .card-dark-tech {
        background: #1e293b;
        border: 1px solid #0284c7;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.15);
    }

    /* Tarjetas Métricas */
    .card-metric-dark {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Botón Principal (Azulino Neón) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 0 12px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.7) !important;
        transform: translateY(-1px);
    }

    /* Personalización de Inputs y Selectboxes en modo oscuro */
    input, select, textarea {
        color: #f8fafc !important;
    }
    
    .stSelectbox > div > div {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }

    /* Ajuste de Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
    }
    button[aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# MEMORIA DE LA APLICACIÓN (Session State)
# =========================================================
if "flujo_caja" not in st.session_state:
    st.session_state.flujo_caja = []

if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])

if "historial_funciones" not in st.session_state:
    st.session_state.historial_funciones = pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])

if "empleados_crud" not in st.session_state:
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1


# =========================================================
# MENÚ LATERAL: LOGO VECTORIAL ELEGANTE Y DESPLEGABLE
# =========================================================
with st.sidebar:
    # Logo Profesional en Vector SVG (Modo Oscuro / Cyber Tech)
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
    
    # Menú desplegable minimalista
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
    
    # Tarjeta Informativa Sidebar
    st.markdown("""
        <div class="card-dark-tech" style="padding: 14px; margin-top: 10px;">
            <span style="color:#38bdf8; font-weight:bold; font-size: 0.8rem; text-transform: uppercase;">Estado del Entorno</span>
            <p style="margin-top:6px; margin-bottom:2px; color:#cbd5e1; font-size: 0.85rem;"><b>Motor:</b> Python 3.12+</p>
            <p style="margin-bottom:0; color:#cbd5e1; font-size: 0.85rem;"><b>Tema:</b> Dark Indigo Tech</p>
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
        st.write("**Autor:** Dino Fredy Pariona Ucharima")  # Personaliza con tu nombre
        st.write("**Programa:** Python for Analytics")
        st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")
        st.write("**Año:** 2026")

    with col_resumen:
        with st.container(border=True):
            st.markdown("<h4 style='color:#38bdf8; font-size:1.05rem; margin-bottom:10px;'>📊 Métricas en Sistema</h4>", unsafe_allow_html=True)
            st.write(f"• Registros en caja: **{len(st.session_state.flujo_caja)}**")
            st.write(f"• Ítems en inventario: **{len(st.session_state.inventario)}**")
            st.write(f"• Personal registrado: **{len(st.session_state.empleados_crud)}**")

    st.divider()

    st.markdown("### 📋 Descripción")
    st.info(
        "Plataforma analítica con diseño Dark Tech optimizado. Consolida el manejo de flujo de datos, "
        "matrices con NumPy, análisis de ventas y persistencia modular mediante clases en Python."
    )


# =========================================================
# 2. EJERCICIO 1: FLUJO DE CAJA
# =========================================================
elif opcion == "Ejercicio 1 - Flujo de Caja":
    st.header("Ejercicio 1 - Flujo de Caja")
    st.caption("")

    with st.container(border=True):
        st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>➕ Registrar Movimiento</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])

        concepto = c1.text_input("Concepto / Descripción", placeholder="Ej. Suscripción Servidores AWS")
        tipo = c2.selectbox("Tipo de Operación", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto ($)", min_value=0.01, step=10.0, format="%.2f")

        if st.button("Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({
                    "Concepto": concepto.strip(),
                    "Tipo": tipo,
                    "Valor": valor
                })
                st.toast("Movimiento guardado con éxito.", icon="✅")
            else:
                st.warning("Ingrese un concepto válido.")

    st.write("")
    st.markdown("### 📋 Registro de Movimientos")

    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)

        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = ingresos - gastos

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"${ingresos:,.2f}")
        m2.metric("Total Gastos", f"${gastos:,.2f}")
        m3.metric("Saldo Neto", f"${saldo:,.2f}")

        if saldo >= 0:
            st.info(f"Balance Positivo: Superávit de **${saldo:,.2f}**")
        else:
            st.warning(f"Balance En Déficit: Déficit de **${abs(saldo):,.2f}**")
    else:
        st.info("No hay transacciones registradas.")


# =========================================================
# 3. EJERCICIO 2: INVENTARIO CON NUMPY
# =========================================================
elif opcion == "Ejercicio 2 - Inventario NumPy":
    st.header("Ejercicio 2 - Control de Inventario")
    st.caption("")

    with st.container(border=True):
        st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>📦 Captura de Producto</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto", placeholder="Ej. Laptop Core i9")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio Unitario ($)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad", min_value=1, step=1)

        if st.button("Agregar Producto", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                
                # Matriz con NumPy
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])

                df_nuevo = pd.DataFrame(
                    arr_registro,
                    columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
                )

                df_nuevo["Precio"] = df_nuevo["Precio"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total"] = df_nuevo["Total"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                st.toast(f"Producto '{prod_nombre}' agregado.", icon="✅")
            else:
                st.warning("Ingrese un nombre de producto.")

    st.write("")
    st.markdown("### 📊 Inventario Consolidado")

    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inv = st.session_state.inventario["Total"].sum()
        
        st.markdown(f"""
            <div class="card-dark-tech">
                <span style="color:#38bdf8; font-weight:bold; font-size: 0.85rem; text-transform: uppercase;">Valorización de Stock</span>
                <h2 style="color:#f8fafc; margin-top:5px; margin-bottom:0;">${total_inv:,.2f} USD</h2>
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
        v_ant = col1.number_input("Ventas Período Anterior ($)", min_value=1.0, value=15000.0, step=500.0)
        v_act = col2.number_input("Ventas Período Actual ($)", min_value=0.0, value=18500.0, step=500.0)

        if st.button("Ejecutar Cálculo", use_container_width=True, type="primary"):
            try:
                # Llamada directa a la función externa
                res = lfunc.calcular_tasa_crecimiento_ventas(
                    ventas_periodo_anterior=v_ant, 
                    ventas_periodo_actual=v_act
                )
                
                tasa_val = res['tasa_crecimiento_pct']
                diferencia = v_act - v_ant

                # Presentación Neón Dark Tech
                st.write("")
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
                            <h1 style="color:#f8fafc; margin:5px 0; font-size:2.2rem;">${diferencia:,.2f}</h1>
                        </div>
                    """, unsafe_allow_html=True)

                # Historial de consultas
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_tasa_crecimiento_ventas",
                    "Parámetros Ingresados": f"Anterior=${v_ant:,.2f} | Actual=${v_act:,.2f}",
                    "Resultado": f"Tasa: {tasa_val}% | Dif: ${diferencia:,.2f}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                
            except Exception as e:
                st.error(f"Error en la ejecución: {e}")

    st.write("")
    st.markdown("### 📜 Bitácora de Cálculos")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("No hay cálculos guardados en esta sesión.")


# =========================================================
# 5. EJERCICIO 4: GESTIÓN DE EMPLEADOS
# =========================================================
elif opcion == "Ejercicio 4 - Gestión de Empleados":
    st.header("Ejercicio 4 - Gestión de Personal (CRUD)")
    st.caption("Administración de colaboradores utilizando la clase `Empleado`.")

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs([
        "Registrar", 
        "Directorio", 
        "Editar", 
        "Eliminar"
    ])

    # CREAR
    with tab_crear:
        with st.container(border=True):
            st.markdown("<h4 style='color:#38bdf8; font-size:1.1rem;'>➕ Alta de Empleado</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            emp_nombre = c1.text_input("Nombre Completo", placeholder="Ej. Lucía Alarcón")
            emp_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=1800.0, step=100.0)

            c3, c4 = c1, c2
            emp_bono = c3.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0)
            emp_desc = c4.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0)

            if st.button("Guardar Empleado", use_container_width=True, type="primary"):
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
                        st.toast(f"Empleado ID {resumen['id']} registrado.", icon="✅")
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
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No hay registros disponibles.")

    # ACTUALIZAR
    with tab_actualizar:
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Seleccione el ID a editar:", lista_ids)

            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                with st.container(border=True):
                    st.markdown(f"<h4 style='color:#38bdf8; font-size:1.1rem;'>Editar Registro (ID: {id_sel})</h4>", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    up_nombre = c1.text_input("Nombre Completo", value=emp_actual["nombre"])
                    up_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=float(emp_actual["salario_base"]))

                    up_bono = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_bono", 0)))
                    up_desc = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_descuento", 0)))

                    if st.button("Actualizar Registro", use_container_width=True, type="primary"):
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
                            
                            st.toast("Registro actualizado.", icon="✅")
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
                    
                    if st.button("Confirmar Eliminación", type="primary", use_container_width=True):
                        st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                        st.toast("Empleado eliminado.", icon="✅")
                        st.rerun()
        else:
            st.info("No hay registros para eliminar.")
