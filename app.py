import streamlit as st
import pandas as pd
import numpy as np

# Importación de las librerías proporcionadas para el proyecto
import libreria_funciones_proyecto1 as lfunc
import libreria_clases_proyecto1 as lclase

# ==========================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Proyecto 1 - Python Fundamentals",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN (SESSION STATE)
# ==========================================
# Ejercicio 1: Lista para el flujo de caja
if "flujo_caja" not in st.session_state:
    st.session_state.flujo_caja = []

# Ejercicio 2: DataFrame para productos registrado con NumPy
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])

# Ejercicio 3: Histórico de resultados de funciones ejecutadas
if "historial_funciones" not in st.session_state:
    st.session_state.historial_funciones = pd.DataFrame(columns=["Función", "Parámetros Ingresados", "Resultado"])

# Ejercicio 4: Almacenamiento de objetos/registros para operaciones CRUD
if "empleados_crud" not in st.session_state:
    # Formato: list of dicts -> [{"id": 0, "nombre": "...", "salario_base": 0.0, ...}]
    st.session_state.empleados_crud = []
    st.session_state.contador_id = 1

# ==========================================
# NAVEGACIÓN - MENÚ LATERAL
# ==========================================
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox(
    "Seleccione una sección:",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# ==========================================
# 1. HOME
# ==========================================
if opcion == "Home":
    st.title("💻 Proyecto Aplicado - Python Fundamentals")
    st.subheader("Especialización en Python for Analytics")
    
    st.divider()
    
    col_info, col_logo = st.columns([2, 1])
    with col_info:
        st.markdown("### 👤 Información del Estudiante")
        st.markdown("**Autor:** Dino Fredy Pariona Ucharima")
        st.markdown("**Módulo:** Módulo 1 - Python Fundamentals")
        st.markdown("**Año:** 2026")
        st.markdown("**Docente:** MSc. Carlos Carrillo Villavicencio")
        
    with col_logo:
        # Muestra una imagen descriptiva o logo
        st.info("📌 **DILIC Institute**\nPython for Analytics 2026")

    st.divider()
    
    st.markdown("### 📋 Descripción del Proyecto")
    st.write(
        "Esta aplicación interactiva desarrollada en Streamlit consolida los conocimientos adquiridos en el Módulo 1 "
        "del programa. A lo largo de la plataforma se evidencian estructuras de datos nativas (listas y diccionarios), "
        "manejo de arreglos multidimensionales y dataframes (NumPy y Pandas), llamadas a funciones modularizadas con "
        "gestión de excepciones, y un sistema completo de persistencia tipo CRUD utilizando Programación Orientada a Objetos (POO)."
    )
    
    st.markdown("### 🛠️ Tecnologías Utilizadas")
    st.markdown("- **Python 3.10+**")
    st.markdown("- **Streamlit** (Interfaz de usuario e interactividad)")
    st.markdown("- **Pandas & NumPy** (Procesamiento y análisis de datos)")

# ==========================================
# 2. EJERCICIO 1: Flujo de caja con listas
# ==========================================
elif opcion == "Ejercicio 1":
    st.header("💵 Ejercicio 1 - Flujo de Caja con Listas")
    st.markdown(
        "Esta sección permite registrar movimientos financieros de manera iterativa utilizando una **lista** "
        "en el estado de la sesión (`st.session_state`)."
    )
    
    st.subheader("Ingresar Movimiento")
    col1, col2, col3 = st.columns([2, 1, 1])
    concepto = col1.text_input("Concepto / Descripción")
    tipo = col2.selectbox("Tipo de Movimiento", ["Ingreso", "Gasto"])
    valor = col3.number_input("Valor ($ / S/)", min_value=0.01, step=10.0, format="%.2f")
    
    if st.button("➕ Agregar Movimiento", use_container_width=True):
        if concepto.strip():
            st.session_state.flujo_caja.append({
                "Concepto": concepto.strip(),
                "Tipo": tipo,
                "Valor": valor
            })
            st.success(f"Movimiento '{concepto}' registrado exitosamente.")
        else:
            st.warning("Debe ingresar un concepto válido.")

    st.divider()
    st.subheader("📋 Lista de Movimientos Registrados")
    
    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo, use_container_width=True)
        
        # Cálculos acumulados
        ingresos = df_flujo[df_flujo["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df_flujo[df_flujo["Tipo"] == "Gasto"]["Valor"].sum()
        saldo_final = ingresos - gastos
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ingresos", f"${ingresos:,.2f}")
        m2.metric("Total Gastos", f"${gastos:,.2f}")
        m3.metric("Saldo Final", f"${saldo_final:,.2f}")
        
        if saldo_final >= 0:
            st.success(f"El flujo de caja está **A FAVOR** con un saldo de ${saldo_final:,.2f}")
        else:
            st.error(f"El flujo de caja está **EN CONTRA** con un déficit de ${abs(saldo_final):,.2f}")
    else:
        st.info("No se han registrado movimientos todavía.")

# ==========================================
# 3. EJERCICIO 2: Registro con NumPy y DataFrames
# ==========================================
elif opcion == "Ejercicio 2":
    st.header("📦 Ejercicio 2 - Registro con NumPy y DataFrame")
    st.markdown(
        "En esta sección los datos capturados se estructuran usando **arreglos de NumPy** "
        "para luego consolidarse en un DataFrame interactivo."
    )
    
    with st.form("form_inventario", clear_on_submit=True):
        st.subheader("Formulario de Registro de Producto")
        col_p1, col_p2 = st.columns(2)
        prod_nombre = col_p1.text_input("Nombre del Producto")
        prod_cat = col_p2.selectbox("Categoría", ["Tecnología", "Oficina", "Servicios", "Línea Blanca"])
        
        col_p3, col_p4 = st.columns(2)
        prod_precio = col_p3.number_input("Precio Unitario", min_value=0.01, step=1.0, format="%.2f")
        prod_cant = col_p4.number_input("Cantidad", min_value=1, step=1)
        
        btn_agregar = st.form_submit_button("➕ Registrar Producto", use_container_width=True)
        
        if btn_agregar:
            if prod_nombre.strip():
                prod_total = prod_precio * prod_cant
                # Construcción del registro utilizando un array de NumPy
                arr_registro = np.array([[prod_nombre.strip(), prod_cat, prod_precio, prod_cant, prod_total]])
                
                df_nuevo = pd.DataFrame(
                    arr_registro, 
                    columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
                )
                
                # Conversión de tipos numéricos
                df_nuevo["Precio"] = df_nuevo["Precio"].astype(float)
                df_nuevo["Cantidad"] = df_nuevo["Cantidad"].astype(int)
                df_nuevo["Total"] = df_nuevo["Total"].astype(float)
                
                st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
                st.success(f"Producto '{prod_nombre}' agregado correctamente.")
            else:
                st.error("Ingrese el nombre del producto.")

    st.divider()
    st.subheader("📊 Inventario Consolidado")
    if not st.session_state.inventario.empty:
        st.dataframe(st.session_state.inventario, use_container_width=True)
        total_inventario = st.session_state.inventario["Total"].sum()
        st.metric("Valor Total del Inventario", f"${total_inventario:,.2f}")
    else:
        st.info("El inventario está vacío.")

# ==========================================
# 4. EJERCICIO 3: Uso de Funciones Externas
# ==========================================
elif opcion == "Ejercicio 3":
    st.header("🧮 Ejercicio 3 - Conexión con Funciones Externas")
    st.markdown(
        "Integración con la librería externa `libreria_funciones_proyecto1.py`. "
        "Seleccione una función, configure sus parámetros y guarde el histórico de ejecuciones."
    )
    
    # Menú de funciones importadas desde libreria_funciones_proyecto1.py
    funcion_seleccionada = st.selectbox(
        "Seleccione la función a ejecutar:",
        [
            "Calcular Punto de Equilibrio (Administración)",
            "Calcular Cuota Préstamo Francés (Finanzas)",
            "Calcular Tasa de Crecimiento de Ventas (Negocios)",
            "Calcular Indicadores de Mantenimiento (MTBF/MTTR)"
        ]
    )
    
    st.divider()
    st.subheader("⚙️ Configuración de Parámetros")
    
    # ---------------------------------------------------------
    # Opción 1: Punto de Equilibrio
    # ---------------------------------------------------------
    if funcion_seleccionada == "Calcular Punto de Equilibrio (Administración)":
        cf = st.number_input("Costos Fijos Totales ($)", min_value=1.0, value=5000.0)
        pu = st.number_input("Precio Unitario ($)", min_value=1.0, value=50.0)
        cvu = st.number_input("Costo Variable Unitario ($)", min_value=0.0, value=20.0)
        
        if st.button("🚀 Ejecutar Función"):
            try:
                res = lfunc.calcular_punto_equilibrio(costos_fijos=cf, precio_unitario=pu, costo_variable_unitario=cvu)
                st.success("Cálculo ejecutado exitosamente:")
                st.json(res)
                
                # Guardar en histórico
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_punto_equilibrio",
                    "Parámetros Ingresados": f"Costos Fijos={cf}, Precio={pu}, Costo Var={cvu}",
                    "Resultado": f"Unidades: {res['punto_equilibrio_unidades']} | Ventas: ${res['punto_equilibrio_ventas']}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
            except Exception as e:
                st.error(f"Error al ejecutar: {e}")

    # ---------------------------------------------------------
    # Opción 2: Cuota Préstamo Francés
    # ---------------------------------------------------------
    elif funcion_seleccionada == "Calcular Cuota Préstamo Francés (Finanzas)":
        monto = st.number_input("Monto del Préstamo ($)", min_value=100.0, value=10000.0)
        tasa = st.number_input("Tasa Anual (%)", min_value=0.1, max_value=100.0, value=12.0)
        plazo = st.number_input("Plazo (Meses)", min_value=1, value=24)
        
        if st.button("🚀 Ejecutar Función"):
            try:
                res = lfunc.calcular_cuota_prestamo_frances(monto=monto, tasa_anual_pct=tasa, plazo_meses=plazo)
                st.success("Cálculo ejecutado exitosamente:")
                st.json(res)
                
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_cuota_prestamo_frances",
                    "Parámetros Ingresados": f"Monto={monto}, Tasa={tasa}%, Plazo={plazo}m",
                    "Resultado": f"Cuota Mensual: ${res['cuota_mensual']} | Total Interés: ${res['interes_total']}"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
            except Exception as e:
                st.error(f"Error al ejecutar: {e}")

    # ---------------------------------------------------------
    # Opción 3: Tasa de Crecimiento de Ventas
    # ---------------------------------------------------------
    elif funcion_seleccionada == "Calcular Tasa de Crecimiento de Ventas (Negocios)":
        v_ant = st.number_input("Ventas Período Anterior ($)", min_value=1.0, value=15000.0)
        v_act = st.number_input("Ventas Período Actual ($)", min_value=0.0, value=18500.0)
        
        if st.button("🚀 Ejecutar Función"):
            try:
                res = lfunc.calcular_tasa_crecimiento_ventas(ventas_periodo_anterior=v_ant, ventas_periodo_actual=v_act)
                st.success("Cálculo ejecutado exitosamente:")
                st.json(res)
                
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_tasa_crecimiento_ventas",
                    "Parámetros Ingresados": f"Anterior={v_ant}, Actual={v_act}",
                    "Resultado": f"Tasa de Crecimiento: {res['tasa_crecimiento_pct']}%"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
            except Exception as e:
                st.error(f"Error al ejecutar: {e}")

    # ---------------------------------------------------------
    # Opción 4: Indicadores de Mantenimiento
    # ---------------------------------------------------------
    elif funcion_seleccionada == "Calcular Indicadores de Mantenimiento (MTBF/MTTR)":
        t_op = st.number_input("Tiempo de Operación (Horas)", min_value=1.0, value=720.0)
        n_fallas = st.number_input("Número de Fallas", min_value=1, value=3)
        t_rep = st.number_input("Tiempo Total Reparación (Horas)", min_value=0.0, value=15.0)
        
        if st.button("🚀 Ejecutar Función"):
            try:
                res = lfunc.calcular_indicadores_mantenimiento(
                    tiempo_operacion_h=t_op, 
                    numero_fallas=n_fallas, 
                    tiempo_reparacion_total_h=t_rep
                )
                st.success("Cálculo ejecutado exitosamente:")
                st.json(res)
                
                nuevo_hist = pd.DataFrame([{
                    "Función": "calcular_indicadores_mantenimiento",
                    "Parámetros Ingresados": f"Op={t_op}h, Fallas={n_fallas}, Rep={t_rep}h",
                    "Resultado": f"MTBF: {res['mtbf_h']}h | MTTR: {res['mttr_h']}h | Disponibilidad: {res['disponibilidad_pct']}%"
                }])
                st.session_state.historial_funciones = pd.concat([st.session_state.historial_funciones, nuevo_hist], ignore_index=True)
            except Exception as e:
                st.error(f"Error al ejecutar: {e}")

    st.divider()
    st.subheader("📜 Histórico de Ejecuciones")
    if not st.session_state.historial_funciones.empty:
        st.dataframe(st.session_state.historial_funciones, use_container_width=True)
    else:
        st.info("Aún no se han ejecutado funciones.")

# ==========================================
# 5. EJERCICIO 4: POO y Operaciones CRUD
# ==========================================
elif opcion == "Ejercicio 4":
    st.header("👥 Ejercicio 4 - POO con Clase Empleado y Módulo CRUD")
    st.markdown(
        "Utiliza la clase `Empleado` importada de `libreria_clases_proyecto1.py`. "
        "Permite realizar las operaciones **C**reate, **R**ead, **U**pdate y **D**elete sobre el registro de personal."
    )
    
    # Sub-navegación usando pestañas (st.tabs)
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs([
        "➕ Crear (Create)", 
        "📋 Leer / Listar (Read)", 
        "✏️ Actualizar (Update)", 
        "🗑️ Eliminar (Delete)"
    ])
    
    # ---------------------------------------------------------
    # TAB 1: CREATE
    # ---------------------------------------------------------
    with tab_crear:
        st.subheader("Registrar Nuevo Empleado")
        with st.form("form_crear_emp", clear_on_submit=True):
            emp_nombre = st.text_input("Nombre Completo")
            emp_salario = st.number_input("Salario Base ($)", min_value=1.0, value=1500.0, step=100.0)
            emp_bono = st.number_input("Porcentaje Bono (%)", min_value=0.0, max_value=100.0, value=10.0)
            emp_desc = st.number_input("Porcentaje Descuento (%)", min_value=0.0, max_value=100.0, value=5.0)
            
            btn_crear = st.form_submit_button("Crear Empleado", use_container_width=True)
            
            if btn_crear:
                if emp_nombre.strip():
                    try:
                        # Instanciación de la clase Empleado
                        nuevo_obj = lclase.Empleado(
                            nombre=emp_nombre.strip(),
                            salario_base=emp_salario,
                            porcentaje_bono=emp_bono,
                            porcentaje_descuento=emp_desc
                        )
                        
                        # Obtener resumen calculado del objeto
                        resumen = nuevo_obj.resumen()
                        resumen["id"] = st.session_state.contador_id
                        resumen["pct_bono"] = emp_bono
                        resumen["pct_descuento"] = emp_desc
                        
                        st.session_state.empleados_crud.append(resumen)
                        st.session_state.contador_id += 1
                        st.success(f"Empleado '{emp_nombre}' creado correctamente con ID {resumen['id']}.")
                    except Exception as e:
                        st.error(f"Error al instanciar el empleado: {e}")
                else:
                    st.error("Ingrese un nombre válido.")

    # ---------------------------------------------------------
    # TAB 2: READ
    # ---------------------------------------------------------
    with tab_leer:
        st.subheader("Listado General de Empleados")
        if st.session_state.empleados_crud:
            df_emp = pd.DataFrame(st.session_state.empleados_crud)
            # Reorganizar columnas
            cols = ["id", "nombre", "salario_base", "pct_bono", "bono", "pct_descuento", "descuento", "salario_neto"]
            df_emp = df_emp[[c for c in cols if c in df_emp.columns]]
            
            st.dataframe(df_emp, use_container_width=True)
        else:
            st.info("No existen empleados en la base de datos.")

    # ---------------------------------------------------------
    # TAB 3: UPDATE
    # ---------------------------------------------------------
    with tab_actualizar:
        st.subheader("Actualizar Registro de Empleado")
        if st.session_state.empleados_crud:
            lista_ids = [emp["id"] for emp in st.session_state.empleados_crud]
            id_sel = st.selectbox("Seleccione el ID del empleado a modificar:", lista_ids)
            
            # Buscar datos actuales del ID seleccionado
            emp_actual = next((item for item in st.session_state.empleados_crud if item["id"] == id_sel), None)
            
            if emp_actual:
                with st.form("form_update_emp"):
                    up_nombre = st.text_input("Nombre Completo", value=emp_actual["nombre"])
                    up_salario = st.number_input("Salario Base ($)", min_value=1.0, value=float(emp_actual["salario_base"]))
                    up_bono = st.number_input("Porcentaje Bono (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_bono", 0)))
                    up_desc = st.number_input("Porcentaje Descuento (%)", min_value=0.0, max_value=100.0, value=float(emp_actual.get("pct_descuento", 0)))
                    
                    btn_actualizar = st.form_submit_button("Guardar Cambios", use_container_width=True)
                    
                    if btn_actualizar:
                        try:
                            # Re-instanciación para recalcular los métodos
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
                            
                            # Reemplazar registro en la lista
                            idx = next(i for i, item in enumerate(st.session_state.empleados_crud) if item["id"] == id_sel)
                            st.session_state.empleados_crud[idx] = resumen
                            st.success(f"Empleado con ID {id_sel} actualizado exitosamente.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al actualizar: {e}")
        else:
            st.info("No hay registros para actualizar.")

    # ---------------------------------------------------------
    # TAB 4: DELETE
    # ---------------------------------------------------------
    with tab_eliminar:
        st.subheader("Eliminar Registro de Empleado")
        if st.session_state.empleados_crud:
            lista_ids_del = [emp["id"] for emp in st.session_state.empleados_crud]
            id_del = st.selectbox("Seleccione el ID a eliminar:", lista_ids_del, key="del_sel")
            
            emp_del = next((item for item in st.session_state.empleados_crud if item["id"] == id_del), None)
            
            if emp_del:
                st.warning(f"¿Está seguro de eliminar al empleado **{emp_del['nombre']}** (ID: {id_del})?")
                if st.button("🗑️ Confirmar Eliminación", type="primary", use_container_width=True):
                    st.session_state.empleados_crud = [item for item in st.session_state.empleados_crud if item["id"] != id_del]
                    st.success(f"Registro con ID {id_del} eliminado correctamente.")
                    st.rerun()
        else:
            st.info("No existen datos disponibles para eliminar.")
