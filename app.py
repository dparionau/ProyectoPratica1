import streamlit as st
import pandas as pd
import numpy as np

# Cargamos las librerías con las funciones y clases del proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Proyecto Python Fundamentals",
    page_icon="🚀",
    layout="wide"
)

# Estilos visuales sencillos para mejorar los botones y textos
st.markdown("""
    <style>
    /* Hace que todos los botones tengan bordes redondeados y texto centrado */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# MEMORIA DE LA APLICACIÓN (Session State)
# =========================================================
# Guarda la lista de compras/movimientos
if "flujo_caja" not in st.session_state:
    st.session_state.flujo_caja = []

# Guarda la lista de productos del inventario
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])

# Guarda el historial de cálculos realizados
if "historial_funciones" not in st.session_state:
    st.session_state.historial_funciones = pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])

# Guarda la lista de empleados creados
if "empleados_crud" not in st.session_state:
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1


# =========================================================
# MENÚ LATERAL (Navegación)
# =========================================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5968/5968350.png", width=60)
st.sidebar.title("Menú Principal")
st.sidebar.caption("Selecciona una opción para navegar:")

opcion = st.sidebar.radio(
    "",
    ["🏠 Inicio", "💵 Ejercicio 1 (Listas)", "📦 Ejercicio 2 (NumPy)", "🧮 Ejercicio 3 (Funciones)", "👥 Ejercicio 4 (POO/CRUD)"]
)


# =========================================================
# 1. INICIO / HOME
# =========================================================
if opcion == "🏠 Inicio":
    st.title("💻 Proyecto Aplicado - Python Fundamentals")
    st.caption("Especialización en Python for Analytics")
    st.divider()

    col_info, col_resumen = st.columns([2, 1])

    with col_info:
        st.markdown("### 👤 Datos del Estudiante")
        st.write("**Estudiante:** Dino Fredy Pariona Ucharima")
        st.write("**Módulo:** Módulo 1 - Fundamentos de Python")
        st.write("**Año:** 2026")
        st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")

    with col_resumen:
        with st.container(border=True):
            st.markdown("### 📌 Estado del Sistema")
            st.write(f"• **Movimientos registrados:** {len(st.session_state.flujo_caja)}")
            st.write(f"• **Productos en inventario:** {len(st.session_state.inventario)}")
            st.write(f"• **Empleados activos:** {len(st.session_state.empleados_crud)}")

    st.divider()

    st.markdown("### 📋 ¿Qué hace esta aplicación?")
    st.info(
        "Esta plataforma permite interactuar de forma práctica con conceptos clave de Python: "
        "manejo de listas, tablas de datos (NumPy y Pandas), llamadas a funciones matemáticas/financieras "
        "y gestión de registros (CRUD) con Programación Orientada a Objetos."
    )


# =========================================================
# 2. EJERCICIO 1: FLUJO DE CAJA (LISTAS)
# =========================================================
elif opcion == "💵 Ejercicio 1 (Listas)":
    st.header("💵 Ejercicio 1 - Registrar Movimientos de Dinero")
    st.caption("Uso de listas simples para guardar ingresos y gastos.")

    # Caja con borde para el formulario de registro
    with st.container(border=True):
        st.subheader("➕ Agregar un nuevo movimiento")
        c1, c2, c3 = st.columns([2, 1, 1])

        concepto = c1.text_input("Concepto o Descripción", placeholder="Ej. Pago de servicio de internet")
        tipo = c2.selectbox("Tipo", ["Ingreso", "Gasto"])
        valor = c3.number_input("Monto ($)", min_value=0.01, step=10.0, format="%.2f")

        # Botón con ícono y ancho completo
        if st.button("📥 Guardar Movimiento", use_container_width=True, type="primary"):
            if concepto.strip():
                st.session_state.flujo_caja.append({
                    "Concepto": concepto.strip(),
                    "Tipo": tipo,
                    "Valor": valor
                })
                st.toast("¡Movimiento guardado con éxito!", icon="✅")
            else:
                st.warning("⚠️ Escribe un concepto antes de guardar.")

    st.write("")

    # Muestra de la lista guardada
    st.subheader("📋 Lista de movimientos registrados")
    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)

        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = ingresos - gastos

        # Cajas con tarjetas de métricas visuales
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"${ingresos:,.2f}")
        m2.metric("Total Gastos", f"${gastos:,.2f}")
        m3.metric("Saldo Disponible", f"${saldo:,.2f}")

        if saldo >= 0:
            st.success(f"✅ Saldo a favor: **${saldo:,.2f}**")
        else:
            st.error(f"🚨 Saldo en contra: **${abs(saldo):,.2f}**")
    else:
        st.info("Aún no has registrado ningún movimiento.")


# =========================================================
# 3. EJERCICIO 2: INVENTARIO (NUMPY Y DATAFRAMES)
# =========================================================
elif opcion == "📦 Ejercicio 2 (NumPy)":
    st.header("📦 Ejercicio 2 - Inventario de Productos")
    st.caption("Uso de NumPy para estructurar datos y Pandas para tablas.")

    with st.container(border=True):
        st.subheader("🛒 Registrar nuevo producto")
        
        col1, col2 = st.columns(2)
        prod_nombre = col1.text_input("Nombre del Producto", placeholder="Ej. Lápiz técnico")
        prod_cat = col2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])

        col3, col4 = st.columns(2)
        prod_precio = col3.number_input("Precio por Unidad ($)", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col4.number_input("Cantidad en Stock", min_value=1, step=1)

        if st.button("➕ Añadir Producto al Inventario", use_container_width=True, type="primary"):
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                # Creamos una fila usando un arreglo de NumPy
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])

                df_nuevo = pd.DataFrame(
                    arr_registro,
                    columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
                )

                # Ajustamos los tipos de datos numéricos
                df_nuevo["Precio"] = df_nuevo["Precio"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total"] = df_nuevo["Total"].astype(float)

                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                st.toast(f"¡Producto '{prod_nombre}' añadido!", icon="📦")
            else:
                st.warning("⚠️ Escribe el nombre del producto.")

    st.write("")

    st.subheader("📊 Tabla general de productos")
    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inv = st.session_state.inventario["Total"].sum()
        st.success(f"💰 **Valor Total del Inventario:** ${total_inv:,.2f}")
    else:
        st.info("El inventario se encuentra vacío.")


# =========================================================
# 4. EJERCICIO 3: USO DE FUNCIONES EXTERNAS
# =========================================================
elif opcion == "🧮 Ejercicio 3 (Funciones)":
    st.header("🧮 Ejercicio 3 - Calculadoras con Funciones")
    st.caption("Ejecuta fórmulas automáticas importadas desde `libreria_funciones_proyecto1.py`.")

    funcion_seleccionada = st.selectbox(
        "Elige qué cálculo quieres realizar:",
        [
            "Calcular Punto de Equilibrio (Administración)",
            "Calcular Cuota de Préstamo (Finanzas)",
            "Calcular Crecimiento de Ventas (Negocios)",
            "Calcular Indicadores de Mantenimiento (MTBF/MTTR)"
        ]
    )

    st.write("")

    with st.container(border=True):
        # --- OPCIÓN 1 ---
        if funcion_seleccionada == "Calcular Punto de Equilibrio (Administración)":
            st.subheader("⚖️ Punto de Equilibrio")
            st.caption("Calcula cuántas unidades debes vender para no ganar ni perder.")
            
            c1, c2, c3 = st.columns(3)
            cf = c1.number_input("Costos Fijos Totales ($)", min_value=1.0, value=5000.0)
            pu = c2.number_input("Precio de Venta ($)", min_value=1.0, value=50.0)
            cvu = c3.number_input("Costo Variable por Unidad ($)", min_value=0.0, value=20.0)

            if st.button("⚡ Calcular Punto de Equilibrio", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_punto_equilibrio(costos_fijos=cf, precio_unitario=pu, costo_variable_unitario=cvu)
                    st.success(f"🎯 Debes vender **{res['punto_equilibrio_unidades']} unidades** (Equivalente a **${res['punto_equilibrio_ventas']:,.2f}** en ventas).")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Punto de Equilibrio",
                        "Parámetros Ingresados": f"Costos=${cf}, Precio=${pu}, CostoVar=${cvu}",
                        "Resultado": f"Unidades: {res['punto_equilibrio_unidades']} | Ventas: ${res['punto_equilibrio_ventas']}"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Ocurrió un error al calcular: {e}")

        # --- OPCIÓN 2 ---
        elif funcion_seleccionada == "Calcular Cuota de Préstamo (Finanzas)":
            st.subheader("💳 Cuota Mensual de Préstamo (Sistema Francés)")
            
            c1, c2, c3 = st.columns(3)
            monto = c1.number_input("Monto del Préstamo ($)", min_value=100.0, value=10000.0)
            tasa = c2.number_input("Tasa Anual (%)", min_value=0.1, max_value=100.0, value=12.0)
            plazo = c3.number_input("Plazo (Meses)", min_value=1, value=24)

            if st.button("⚡ Calcular Cuota", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_cuota_prestamo_frances(monto=monto, tasa_anual_pct=tasa, plazo_meses=plazo)
                    st.success(f"💵 Cuota mensual: **${res['cuota_mensual']:,.2f}** | Interés total a pagar: **${res['interes_total']:,.2f}**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Cuota Préstamo",
                        "Parámetros Ingresados": f"Monto=${monto}, Tasa={tasa}%, Plazo={plazo}m",
                        "Resultado": f"Cuota Mensual: ${res['cuota_mensual']} | Total Interés: ${res['interes_total']}"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Ocurrió un error al calcular: {e}")

        # --- OPCIÓN 3 ---
        elif funcion_seleccionada == "Calcular Crecimiento de Ventas (Negocios)":
            st.subheader("📈 Tasa de Crecimiento de Ventas")
            
            c1, c2 = st.columns(2)
            v_ant = c1.number_input("Ventas del Período Anterior ($)", min_value=1.0, value=15000.0)
            v_act = c2.number_input("Ventas del Período Actual ($)", min_value=0.0, value=18500.0)

            if st.button("⚡ Calcular Crecimiento", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_tasa_crecimiento_ventas(ventas_periodo_anterior=v_ant, ventas_periodo_actual=v_act)
                    st.success(f"📈 Porcentaje de Crecimiento: **{res['tasa_crecimiento_pct']}%**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Crecimiento Ventas",
                        "Parámetros Ingresados": f"Anterior=${v_ant}, Actual=${v_act}",
                        "Resultado": f"Tasa de Crecimiento: {res['tasa_crecimiento_pct']}%"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Ocurrió un error al calcular: {e}")

        # --- OPCIÓN 4 ---
        elif funcion_seleccionada == "Calcular Indicadores de Mantenimiento (MTBF/MTTR)":
            st.subheader("🛠️ Indicadores de Mantenimiento de Equipos")
            
            c1, c2, c3 = st.columns(3)
            t_op = c1.number_input("Horas de Operación", min_value=1.0, value=720.0)
            n_fallas = c2.number_input("Número de Fallas", min_value=1, value=3)
            t_rep = c3.number_input("Horas de Reparación Total", min_value=0.0, value=15.0)

            if st.button("⚡ Calcular Indicadores", use_container_width=True, type="primary"):
                try:
                    res = lfunc.calcular_indicadores_mantenimiento(
                        tiempo_operacion_h=t_op,
                        numero_fallas=n_fallas,
                        tiempo_reparacion_total_h=t_rep
                    )
                    st.success(f"⚙️ MTBF: **{res['mtbf_h']} hrs** | MTTR: **{res['mttr_h']} hrs** | Disponibilidad: **{res['disponibilidad_pct']}%**")
                    
                    nuevo_hist = pd.DataFrame([{
                        "Función": "Indicadores Mantenimiento",
                        "Parámetros Ingresados": f"Op={t_op}h, Fallas={n_fallas}, Rep={t_rep}h",
                        "Resultado": f"MTBF: {res['mtbf_h']}h | MTTR: {res['mttr_h']}h | Disponibilidad: {res['disponibilidad_pct']}%"
                    }])
                    st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
                except Exception as e:
                    st.error(f"Ocurrió un error al calcular: {e}")

    st.write("")

    st.subheader("📜 Historial de cálculos realizados")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("Aún no se ha realizado ningún cálculo.")


# =========================================================
# 5. EJERCICIO 4: GESTIÓN DE EMPLEADOS (POO Y CRUD)
# =========================================================
elif opcion == "👥 Ejercicio 4 (POO/CRUD)":
    st.header("👥 Ejercicio 4 - Gestión de Empleados")
    st.caption("Crear, ver, actualizar y eliminar registros utilizando la clase `Empleado`.")

    # Pestañas limpias para las 4 acciones principales
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs([
        "➕ Registrar (Crear)", 
        "📋 Listado (Leer)", 
        "✏️ Editar (Actualizar)", 
        "🗑️ Eliminar"
    ])

    # 1. CREAR
    with tab_crear:
        with st.container(border=True):
            st.subheader("Registrar un nuevo empleado")
            
            c1, c2 = st.columns(2)
            emp_nombre = c1.text_input("Nombre Completo", placeholder="Ej. Ana Martínez")
            emp_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=1500.0, step=100.0)

            c3, c4 = c1, c2
            emp_bono = c3.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0)
            emp_desc = c4.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=5.0)

            if st.button("💾 Guardar Empleado", use_container_width=True, type="primary"):
                if emp_nombre.strip():
                    try:
                        # Creamos la instancia/objeto a partir de la clase Empleado
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
                        st.toast(f"Empleado '{emp_nombre}' registrado con éxito.", icon="👤")
                    except Exception as e:
                        st.error(f"Error al guardar empleado: {e}")
                else:
                    st.warning("⚠️ Escribe un nombre válido.")

    # 2. LEER
    with tab_leer:
        st.subheader("Lista general de empleados")
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            
            # Ordenamos las columnas para verlas con claridad
            columnas_orden = ["id", "nombre", "salario_base", "pct_bono", "bono", "pct_descuento", "descuento", "salario_neto"]
            df_emp = df_emp[[col for col in columnas_orden if col in df_emp.columns]]
            
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No hay empleados registrados en la base de datos.")

    # 3. ACTUALIZAR
    with tab_actualizar:
        if st.session_state.empleados_crud:
            lista_ids = [e["id"] for e in st.session_state.empleados_crud]
            id_sel = st.selectbox("Selecciona el ID del empleado que deseas editar:", lista_ids)

            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)

            if emp_actual:
                with st.container(border=True):
                    st.subheader(f"Modificando a: {emp_actual['nombre']} (ID: {id_sel})")
                    
                    c1, c2 = st.columns(2)
                    up_nombre = c1.text_input("Nombre Completo", value=emp_actual["nombre"])
                    up_salario = c2.number_input("Salario Base ($)", min_value=1.0, value=float(emp_actual["salario_base"]))

                    up_bono = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_bono", 0)))
                    up_desc = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_descuento", 0)))

                    if st.button("🔄 Actualizar Datos", use_container_width=True, type="primary"):
                        try:
                            # Re-creamos el objeto con los datos modificados
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

                            # Reemplazamos los datos en la lista
                            posicion = next(i for i, item in enumerate(st.session_state.empleados_crud) if item["id"] == id_sel)
                            st.session_state.empleados_crud[posicion] = resumen
                            
                            st.toast("¡Datos actualizados con éxito!", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al actualizar: {e}")
        else:
            st.info("No hay datos disponibles para editar.")

    # 4. ELIMINAR
    with tab_eliminar:
        if st.session_state.empleados_crud:
            lista_ids_del = [e["id"] for e in st.session_state.empleados_crud]
            id_del = st.selectbox("Selecciona el ID del empleado a eliminar:", lista_ids_del, key="del_select")

            emp_del = next((item for item in st.session_state.empleados_crud if item["id"] == id_del), None)

            if emp_del:
                with st.container(border=True):
                    st.warning(f"⚠️ ¿Estás seguro de que deseas borrar a **{emp_del['nombre']}** (ID: {id_del})?")
                    
                    # Botón destacado en color rojo/principal para alerta de borrado
                    if st.button("🗑️ Sí, Eliminar Definitivamente", type="primary", use_container_width=True):
                        st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                        st.toast(f"Empleado con ID {id_del} eliminado.", icon="🗑️")
                        st.rerun()
        else:
            st.info("No hay datos disponibles para eliminar.")
