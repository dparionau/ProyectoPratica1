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
    page_title="Analytics System - Python Fundamentals",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# DISEÑO CSS: ESTILO ELEGANTE, PROFESIONAL Y TECNOLÓGICO
# =========================================================
st.markdown("""
    <style>
    /* Fondo limpio de alta resolución */
    .stApp {
        background-color: #f8fafc;
    }

    /* Estilo de botones principales: Azulino Ejecutivo con Hover */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 6px -1px rgba(2, 132, 199, 0.2) !important;
        transition: all 0.25s ease-in-out !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%) !important;
        box-shadow: 0 6px 12px -2px rgba(2, 132, 199, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Tarjetas Tecnológicas con Bordes Finos en Celeste */
    [data-testid="stForm"], div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        border-radius: 12px !important;
        border: 1px solid #e0f2fe !important;
        box-shadow: 0 4px 15px -3px rgba(14, 165, 233, 0.05) !important;
    }

    /* Cajas destacadas de tarjetas azules */
    .card-tech {
        background: #ffffff;
        border-left: 4px solid #0284c7;
        border-top: 1px solid #e0f2fe;
        border-right: 1px solid #e0f2fe;
        border-bottom: 1px solid #e0f2fe;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .card-metric {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }

    /* Títulos principales */
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Estilo del menú lateral */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
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
    st.session_state.historial_funciones = pd.DataFrame(columns=["Fecha/Hora", "Función", "Parámetros Ingresados", "Resultado"])

if "empleados_crud" not in st.session_state:
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1


# =========================================================
# MENÚ LATERAL: DESPLEGABLE MINIMALISTA
# =========================================================
with st.sidebar:
    st.markdown("### 🗂️ Navegación")
    
    # Cuadro desplegable sin íconos cargados
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
    
    # Panel lateral tipo resumen
    st.markdown("""
        <div class="card-tech">
            <span style="color:#0284c7; font-weight:bold; font-size: 0.85rem; text-transform: uppercase;">Estado del Sistema</span>
            <p style="margin-top:8px; margin-bottom:4px; color:#334155; font-size: 0.9rem;"><b>Módulo:</b> Python Fundamentals</p>
            <p style="margin-bottom:0; color:#334155; font-size: 0.9rem;"><b>Versión:</b> 2026.1</p>
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
        st.markdown("### 👤 Información del Proyecto")
        st.write("**Autor:** Dino Fredy Pariona Ucharima")
        st.write("**Programa:** Python for Analytics")
        st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")
        st.write("**Periodo Académico:** 2026")

    with col_resumen:
        with st.container(border=True):
            st.markdown("<h4 style='color:#0284c7; font-size:1.1rem; margin-bottom:10px;'>📊 Métricas en Memoria</h4>", unsafe_allow_html=True)
            st.write(f"• Registros en caja: **{len(st.session_state.flujo_caja)}**")
            st.write(f"• Ítems en inventario: **{len(st.session_state.inventario)}**")
            st.write(f"• Personal en sistema: **{len(st.session_state.empleados_crud)}**")

    st.divider()

    st.markdown("### 📋 Alcance de la Aplicación")
    st.info(
        "Esta plataforma integra de manera modular los fundamentos de desarrollo en Python: "
        "gestión de flujo de datos en listas, arreglos multidimensionales con NumPy, tablas analíticas en Pandas, "
        "módulos de cálculo financiero/comercial y persistencia mediante Programación Orientada a Objetos (POO)."
    )


# =========================================================
# 2. EJERCICIO 1: FLUJO DE CAJA
# =========================================================
elif opcion == "Ejercicio 1 - Flujo de Caja":
    st.header("Ejercicio 1 - Flujo de Caja")
    st.caption("Control y seguimiento de ingresos y egresos financieros.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#0284c7; font-size:1.1rem;'>➕ Captura de Movimiento</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])

        concepto = c1.text_input("Concepto / Descripción", placeholder="Ej. Licencia de software")
        tipo = c2.selectbox("Tipo de Operación", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto ($)", min_value=0.01, step=10.0, format="%.2f")

        if st.button("Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({
                    "Concepto": concepto.strip(),
                    "Tipo": tipo,
                    "Valor": valor
                })
                st.toast("Movimiento registrado exitosamente.", icon="✅")
            else:
                st.warning("Ingrese un concepto descriptivo.")

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
            st.info(f"Balance Positivo: Tienes un superávit de **${saldo:,.2f}**")
        else:
            st.warning(f"Balance En Déficit: Presentas un saldo en contra de **${abs(saldo):,.2f}**")
    else:
        st.info("No se han registrado movimientos todavía.")


# =========================================================
# 3. EJERCICIO 2: INVENTARIO CON NUMPY
# =========================================================
elif opcion == "Ejercicio 2 - Inventario NumPy":
    st.header("Ejercicio 2 - Control de Inventario")
    st.caption("Estructuración de matrices de productos mediante NumPy y DataFrames.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#0284c7; font-size:1.1rem;'>📦 Registrar Producto</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto", placeholder="Ej. Monitor 27 pulgadas")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio Unitario ($)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad en Stock", min_value=1, step=1)

        if st.button("Agregar Producto", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                
                # Construcción con NumPy
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])

                df_nuevo = pd.DataFrame(
                    arr_registro,
                    columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
                )

                df_nuevo["Precio"] = df_nuevo["Precio"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total"] = df_nuevo["Total"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                st.toast(f"Producto '{prod_nombre}' añadido correctamente.", icon="✅")
            else:
                st.warning("Ingrese un nombre de producto.")

    st.write("")
    st.markdown("### 📊 Consolidated Stock Table")

    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inv = st.session_state.inventario["Total"].sum()
        
        st.markdown(f"""
            <div class="card-tech">
                <span style="color:#0284c7; font-weight:bold; font-size: 0.85rem; text-transform: uppercase;">Valorización de Inventario</span>
                <h3 style="color:#0369a1; margin-top:5px; margin-bottom:0;">${total_inv:,.2f} USD</h3>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("El inventario no contiene registros.")


# =========================================================
# 4. EJERCICIO 3: TASA DE CRECIMIENTO DE VENTAS
# =========================================================
elif opcion == "Ejercicio 3 - Crecimiento de Ventas":
    st.header("Ejercicio 3 - Tasa de Crecimiento de Ventas")
    st.caption("Cálculo comercial automatizado mediante `libreria_funciones_proyecto1.py`.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#0284c7; font-size:1.1rem;'>📈 Parámetros de Comparación</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        v_ant = col1.number_input("Ventas del Período Anterior ($)", min_value=1.0, value=15000.0, step=500.0)
        v_act = col2.number_input("Ventas del Período Actual ($)", min_value=0.0, value=18500.0, step=500.0)

        if st.button("Ejecutar Cálculo de Crecimiento", use_container_width=True, type="primary"):
            try:
                # Llamada directa a la función externa
                res = lfunc.calcular_tasa_crecimiento_ventas(
                    ventas_periodo_anterior=v_ant, 
                    ventas_periodo_actual=v_act
                )
                
                tasa_val = res['tasa_crecimiento_pct']
                
                # Presentación ejecutiva del resultado
                st.write("")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.markdown(f"""
                        <div class="card-metric">
                            <span style="color:#0369a1; font-weight:bold; font-size:0.9rem;">TASA DE CRECIMIENTO</span>
                            <h2 style="color:#0284c7; margin:5px 0;">{tasa_val}%</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_res2:
                    diferencia = v_act - v_ant
                    st.markdown(f"""
                        <div class="card-metric">
                            <span style="color:#0369a1; font-weight:bold; font-size:0.9rem;">VARIACIÓN ABSOLUTA</span>
                            <h2 style="color:#0284c7; margin:5px 0;">${diferencia:,.2f}</h2>
                        </div>
                    """, unsafe_allow_html=True)

                # Guardado en el historial de ejecuciones
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_tasa_crecimiento_ventas",
                    "Parámetros Ingresados": f"Anterior=${v_ant:,.2f} | Actual=${v_act:,.2f}",
                    "Resultado": f"Tasa: {tasa_val}% | Dif: ${diferencia:,.2f}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                
            except Exception as e:
                st.error(f"Error durante el cálculo: {e}")

    st.write("")
    st.markdown("### 📜 Bitácora de Cálculos")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("Aún no se han ejecutado cálculos en este módulo.")


# =========================================================
# 5. EJERCICIO 4: GESTIÓN DE EMPLEADOS
# =========================================================
elif opcion == "Ejercicio 4 - Gestión de Empleados":
    st.header("Ejercicio 4 - Gestión de Personal (CRUD)")
    st.caption("Administración de colaboradores utilizando la clase `Empleado`.")

    # Pestañas ejecutivas estilo tab
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs([
        "Registrar", 
        "Directorio", 
        "Editar", 
        "Eliminar"
    ])

    # 1. REGISTRAR
    with tab_crear:
        with st.container(border=True):
            st.markdown("<h4 style='color:#0284c7; font-size:1.1rem;'>➕ Alta de Colaborador</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            emp_nombre = c1.text_input("Nombre Completo", placeholder="Ej. Lucía Alarcón")
            emp_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=1800.0, step=100.0)

            c3, c4 = c1, c2
            emp_bono = c3.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0)
            emp_desc = c4.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0)

            if st.button("Guardar Empleado", use_container_width=True, type="primary"):
                if emp_nombre.strip():
                    try:
                        # Instanciación de la clase
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
                        st.toast(f"Empleado ID {resumen['id']} registrado correctamente.", icon="✅")
                    except Exception as e:
                        st.error(f"Ocurrió un error al registrar: {e}")
                else:
                    st.warning("Ingrese un nombre válido.")

    # 2. VER LISTA
    with tab_leer:
        st.markdown("### Directorio General de Empleados")
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            cols = ["id", "nombre", "salario_base", "pct_bono", "bono", "pct_descuento", "descuento", "salario_neto"]
            df_emp = df_emp[[c for c in cols if c in df_emp.columns]]
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No existen registros en la base de datos.")

    # 3. EDITAR
    with tab_actualizar:
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Seleccione el ID a modificar:", lista_ids)

            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                with st.container(border=True):
                    st.markdown(f"<h4 style='color:#0284c7; font-size:1.1rem;'>Modificar Datos (ID: {id_sel})</h4>", unsafe_allow_html=True)
                    
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
                            
                            st.toast("Registro actualizado con éxito.", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al actualizar: {e}")
        else:
            st.info("No hay registros para modificar.")

    # 4. ELIMINAR
    with tab_eliminar:
        if st.session_state.empleados_crud:
            lista_ids_del = [e["id"] for e in st.session_state.empleados_crud]
            id_del = st.selectbox("Seleccione el ID del empleado a eliminar:", lista_ids_del, key="del_select")

            emp_del = next((item for item in st.session_state.empleados_crud if item["id"] == id_del), None)

            if emp_del:
                with st.container(border=True):
                    st.info(f"¿Desea dar de baja permanentemente a **{emp_del['nombre']}** (ID: {id_del})?")
                    
                    if st.button("Confirmar Eliminación", type="primary", use_container_width=True):
                        st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                        st.toast("Empleado eliminado.", icon="✅")
                        st.rerun()
        else:
            st.info("No existen registros disponibles para dar de baja.")
