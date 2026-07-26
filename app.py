import streamlit as st
import pandas as pd
import numpy as np

# Cargamos las librerías con las funciones y clases del proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# =========================================================
# CONFIGURACIÓN GENERAL Y ESTILOS AZULES / CELESTES
# =========================================================
st.set_page_config(
    page_title="Proyecto Python Fundamentals",
    page_icon="💻",
    layout="wide"
)

# Inyección de CSS para la personalización en tonos azulinos, celeste y azul profundo
st.markdown("""
    <style>
    /* Fondo general de la app */
    .main {
        background-color: #f8fafc;
    }
    
    /* Estilo para los botones principales (Azul Intenso / Azulino) */
    div.stButton > button[kind="primary"] {
        background-color: #0284c7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #0369a1 !important;
        box-shadow: 0 4px 12px rgba(3, 105, 161, 0.25) !important;
    }

    /* Estilo para los botones secundarios */
    div.stButton > button[kind="secondary"] {
        border: 1px solid #bae6fd !important;
        color: #0369a1 !important;
        background-color: #f0f9ff !important;
        border-radius: 8px !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background-color: #e0f2fe !important;
    }

    /* Personalización de los contenedores/cuadros con borde */
    [data-testid="stForm"], [data-testid="stHeader"] {
        border-color: #bae6fd !important;
    }
    
    /* Estilo para destacar tarjetas informativas */
    .card-azul {
        background-color: #f0f9ff;
        border: 1px solid #7dd3fc;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }

    /* Títulos en tono azul oscuro */
    h1, h2, h3 {
        color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# MEMORIA DE LA APLICACIÓN (Session State)
# =========================================================
# Almacenamiento interactivo para cada sección
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
# MENÚ LATERAL: CUADRO DESPLEGABLE LIMPIC
# =========================================================
with st.sidebar:
    st.markdown("### 🗂️ Panel de Control")
    
    # Cuadro desplegable para seleccionar la sección (sin íconos cargados)
    opcion = st.selectbox(
        "Ir a la sección:",
        [
            "Inicio",
            "Ejercicio 1 - Flujo de Caja",
            "Ejercicio 2 - Inventario NumPy",
            "Ejercicio 3 - Calculadoras",
            "Ejercicio 4 - Gestión de Empleados"
        ]
    )
    
    st.divider()
    
    # Tarjeta azulina de estado rápido en el menú
    st.markdown("""
        <div class="card-azul">
            <h4 style="color:#0369a1; margin-top:0;">Estado General</h4>
            <p style="margin-bottom:5px; color:#334155;"><b>Módulo:</b> Python Fundamentals</p>
            <p style="margin-bottom:0; color:#334155;"><b>Año:</b> 2026</p>
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# 1. INICIO / HOME
# =========================================================
if opcion == "Inicio":
    st.title("Proyecto Aplicado - Python Fundamentals")
    st.caption("Especialización en Python for Analytics")
    st.divider()

    col_info, col_resumen = st.columns([2, 1])

    with col_info:
        st.markdown("### Datos del Estudiante")
        st.write("**Estudiante:** Dino Fredy Pariona Ucharima")
        st.write("**Programa:** Python for Analytics")
        st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")
        st.write("**Año Académico:** 2026")

    with col_resumen:
        with st.container(border=True):
            st.markdown("<h4 style='color:#0284c7;'>Resumen del Sistema</h4>", unsafe_allow_html=True)
            st.write(f"• Movimientos en caja: **{len(st.session_state.flujo_caja)}**")
            st.write(f"• Productos en stock: **{len(st.session_state.inventario)}**")
            st.write(f"• Empleados registrados: **{len(st.session_state.empleados_crud)}**")

    st.divider()

    st.markdown("### Descripción de la Plataforma")
    st.info(
        "Esta aplicación consolida el uso práctico de estructuras de datos en Python, arreglos multidimensionales con NumPy, "
        "gestión de tablas con Pandas, llamada a librerías externas de funciones y operaciones CRUD avanzadas con "
        "Programación Orientada a Objetos (POO)."
    )


# =========================================================
# 2. EJERCICIO 1: FLUJO DE CAJA
# =========================================================
elif opcion == "Ejercicio 1 - Flujo de Caja":
    st.header("Ejercicio 1 - Flujo de Caja")
    st.caption("Registro iterativo de ingresos y egresos de dinero usando listas de Python.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#0369a1;'>Registrar Nuevo Movimiento</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])

        concepto = c1.text_input("Concepto / Descripción", placeholder="Ej. Pago de servicio de hosting")
        tipo = c2.selectbox("Tipo de Movimiento", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto ($)", min_value=0.01, step=10.0, format="%.2f")

        if st.button("Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({
                    "Concepto": concepto.strip(),
                    "Tipo": tipo,
                    "Valor": valor
                })
                st.toast("Movimiento registrado correctamente.", icon="✅")
            else:
                st.warning("Por favor, ingresa un concepto válido.")

    st.write("")
    st.markdown("### Historial de Movimientos")

    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)

        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = ingresos - gastos

        # Métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"${ingresos:,.2f}")
        m2.metric("Total Gastos", f"${gastos:,.2f}")
        m3.metric("Saldo Neto", f"${saldo:,.2f}")

        if saldo >= 0:
            st.info(f"Balance Positivo: Se cuenta con un saldo a favor de **${saldo:,.2f}**")
        else:
            st.warning(f"Balance En Deficit: Se registra un déficit de **${abs(saldo):,.2f}**")
    else:
        st.info("No hay movimientos registrados hasta el momento.")


# =========================================================
# 3. EJERCICIO 2: INVENTARIO CON NUMPY
# =========================================================
elif opcion == "Ejercicio 2 - Inventario NumPy":
    st.header("Ejercicio 2 - Registro de Inventario")
    st.caption("Uso de arreglos NumPy para estructurar datos y consolidarlos en un DataFrame.")

    with st.container(border=True):
        st.markdown("<h4 style='color:#0369a1;'>Ingreso de Producto</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto", placeholder="Ej. Teclado Mecánico")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio Unitario ($)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad", min_value=1, step=1)

        if st.button("Agregar al Inventario", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                
                # Arreglo de NumPy para la fila
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])

                df_nuevo = pd.DataFrame(
                    arr_registro,
                    columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
                )

                # Ajuste de tipos numéricos
                df_nuevo["Precio"] = df_nuevo["Precio"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total"] = df_nuevo["Total"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                st.toast(f"Producto '{prod_nombre}' agregado.", icon="✅")
            else:
                st.warning("Escribe el nombre del producto.")

    st.write("")
    st.markdown("### Productos Registrados")

    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inv = st.session_state.inventario["Total"].sum()
        
        st.markdown(f"""
            <div class="card-azul">
                <h4 style="color:#0284c7; margin:0;">Valor Total del Inventario: ${total_inv:,.2f}</h4>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("El inventario está vacío.")


# =========================================================
# 4. EJERCICIO 3: CALCULADORAS CON FUNCIONES
# =========================================================
elif opcion == "Ejercicio 3 - Calculadoras":
    st.header("Ejercicio 3 - Módulo de Calculadoras")
    st.caption("Conexión directa con las funciones importadas de `libreria_funciones_proyecto1.py`.")

    funcion_seleccionada = st.selectbox(
        "Selecciona el tipo de cálculo a realizar:",
        [
            "Punto de Equilibrio (Administración)",
            "Cuota de Préstamo (Finanzas)",
            "Tasa de Crecimiento de Ventas (Negocios)",
            "Indicadores MTBF/MTTR (Mantenimiento)"
        ]
    )

    st.write("")

    with st.container(border=True):
        # Punto de Equilibrio
        if funcion_seleccionada == "Punto de Equilibrio (Administración)":
            st.markdown("<h4 style='color:#0369a1;'>Cálculo de Punto de Equilibrio</h4>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            cf = c1.number_input("Costos Fijos Totales ($)", min_value=1.0, value=5000.0)
            pu = c2.number_input("Precio Unitario ($)", min_value=1.0, value=50.0)
            cvu = c3.number_input("Costo Variable Unitario ($)", min_value=0.0, value=20.0)

            if st.button("Calcular Punto de Equilibrio", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_punto_equilibrio(costos_fijos=cf, precio_unitario=pu, costo_variable_unitario=cvu)
                    st.info(f"Punto de equilibrio: **{res['punto_equilibrio_unidades']} unidades** (Ventas requeridas: **${res['punto_equilibrio_ventas']:,.2f}**)")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Punto de Equilibrio",
                        "Parámetros Ingresados": f"CF=${cf}, PU=${pu}, CVU=${cvu}",
                        "Resultado": f"Unidades: {res['punto_equilibrio_unidades']} | Ventas: ${res['punto_equilibrio_ventas']}"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Error en el cálculo: {e}")

        # Cuota Préstamo
        elif funcion_seleccionada == "Cuota de Préstamo (Finanzas)":
            st.markdown("<h4 style='color:#0369a1;'>Cálculo de Cuota Francés</h4>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            monto = c1.number_input("Monto del Préstamo ($)", min_value=100.0, value=10000.0)
            tasa = c2.number_input("Tasa Anual (%)", min_value=0.1, max_value=100.0, value=12.0)
            plazo = c3.number_input("Plazo (Meses)", min_value=1, value=24)

            if st.button("Calcular Cuota Mensual", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_cuota_prestamo_frances(monto=monto, tasa_anual_pct=tasa, plazo_meses=plazo)
                    st.info(f"Cuota Mensual: **${res['cuota_mensual']:,.2f}** | Total Interés: **${res['interes_total']:,.2f}**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Cuota Préstamo",
                        "Parámetros Ingresados": f"Monto=${monto}, Tasa={tasa}%, Plazo={plazo}m",
                        "Resultado": f"Cuota: ${res['cuota_mensual']} | Interés: ${res['interes_total']}"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Error en el cálculo: {e}")

        # Crecimiento de Ventas
        elif funcion_seleccionada == "Tasa de Crecimiento de Ventas (Negocios)":
            st.markdown("<h4 style='color:#0369a1;'>Cálculo de Crecimiento de Ventas</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            v_ant = c1.number_input("Ventas Período Anterior ($)", min_value=1.0, value=15000.0)
            v_act = c2.number_input("Ventas Período Actual ($)", min_value=0.0, value=18500.0)

            if st.button("Calcular Crecimiento", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_tasa_crecimiento_ventas(ventas_periodo_anterior=v_ant, ventas_periodo_actual=v_act)
                    st.info(f"Tasa de Crecimiento Obtenida: **{res['tasa_crecimiento_pct']}%**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Crecimiento Ventas",
                        "Parámetros Ingresados": f"Anterior=${v_ant}, Actual=${v_act}",
                        "Resultado": f"Crecimiento: {res['tasa_crecimiento_pct']}%"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Error en el cálculo: {e}")

        # Indicadores Mantenimiento
        elif funcion_seleccionada == "Indicadores MTBF/MTTR (Mantenimiento)":
            st.markdown("<h4 style='color:#0369a1;'>Indicadores MTBF y MTTR</h4>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            t_op = c1.number_input("Horas de Operación", min_value=1.0, value=720.0)
            n_fallas = c2.number_input("Cantidad de Fallas", min_value=1, value=3)
            t_rep = c3.number_input("Horas de Reparación Total", min_value=0.0, value=15.0)

            if st.button("Calcular Indicadores", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_indicadores_mantenimiento(
                        tiempo_operacion_h=t_op,
                        numero_fallas=n_fallas,
                        tiempo_reparacion_total_h=t_rep
                    )
                    st.info(f"MTBF: **{res['mtbf_h']} hrs** | MTTR: **{res['mttr_h']} hrs** | Disponibilidad: **{res['disponibilidad_pct']}%**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Indicadores MTBF/MTTR",
                        "Parámetros Ingresados": f"Op={t_op}h, Fallas={n_fallas}, Rep={t_rep}h",
                        "Resultado": f"MTBF: {res['mtbf_h']}h | MTTR: {res['mttr_h']}h | Disp: {res['disponibilidad_pct']}%"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Error en el cálculo: {e}")

    st.write("")
    st.markdown("### Histórico de Consultas Realizadas")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("Aún no has ejecutado ninguna función en esta sesión.")


# =========================================================
# 5. EJERCICIO 4: GESTIÓN DE EMPLEADOS (POO Y CRUD)
# =========================================================
elif opcion == "Ejercicio 4 - Gestión de Empleados":
    st.header("Ejercicio 4 - Gestión de Empleados")
    st.caption("Módulo de mantenimiento CRUD utilizando la clase `Empleado`.")

    # Pestañas para dividir cada operación
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs([
        "Registrar", 
        "Ver Lista", 
        "Actualizar", 
        "Eliminar"
    ])

    # CREAR
    with tab_crear:
        with st.container(border=True):
            st.markdown("<h4 style='color:#0369a1;'>Nuevo Empleado</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            emp_nombre = c1.text_input("Nombre Completo", placeholder="Ej. Carlos Mendoza")
            emp_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=1500.0, step=100.0)

            c3, c4 = c1, c2
            emp_bono = c3.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0)
            emp_desc = c4.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0)

            if st.button("Guardar Registro", use_container_width=True, type="primary"):
                if emp_nombre.strip():
                    try:
                        # Instanciación del objeto Empleado
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
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Escribe un nombre válido.")

    # LEER
    with tab_leer:
        st.markdown("### Directorio de Personal")
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            cols = ["id", "nombre", "salario_base", "pct_bono", "bono", "pct_descuento", "descuento", "salario_neto"]
            df_emp = df_emp[[c for c in cols if c in df_emp.columns]]
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No hay registros disponibles en la base de datos.")

    # ACTUALIZAR
    with tab_actualizar:
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Selecciona el ID del empleado a editar:", lista_ids)

            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                with st.container(border=True):
                    st.markdown(f"<h4 style='color:#0369a1;'>Modificar Registro (ID: {id_sel})</h4>", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    up_nombre = c1.text_input("Nombre Completo", value=emp_actual["nombre"])
                    up_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=float(emp_actual["salario_base"]))

                    up_bono = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_bono", 0)))
                    up_desc = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_descuento", 0)))

                    if st.button("Guardar Cambios", use_container_width=True, type="primary"):
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
            st.info("No hay registros para actualizar.")

    # ELIMINAR
    with tab_eliminar:
        if st.session_state.empleados_crud:
            lista_ids_del = [e["id"] for e in st.session_state.empleados_crud]
            id_del = st.selectbox("Selecciona el ID del registro a eliminar:", lista_ids_del, key="del_select")

            emp_del = next((item for item in st.session_state.empleados_crud if item["id"] == id_del), None)

            if emp_del:
                with st.container(border=True):
                    st.info(f"¿Confirmas la eliminación del registro **{emp_del['nombre']}** (ID: {id_del})?")
                    
                    if st.button("Confirmar Eliminación", type="primary", use_container_width=True):
                        st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                        st.toast("Empleado eliminado.", icon="✅")
                        st.rerun()
        else:
            st.info("No existen registros para eliminar.")
