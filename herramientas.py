import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from colores import *
from imagenes import cargar_imagen_productos, cargar_icono_categoria

ubicacion_banco_identidades = "usuarios.json"
ubicacion_memoria_sesion = "recordar.json"
ubicacion_catalogo_ofertas = "menu.json"
ubicacion_libro_transacciones = "facturacion.json"
ubicacion_logistica_tarifa = "domicilio.json"
factor_recargo_tributario = 0.15

def _transaccionar_json_lectura(ruta_al_disco, estructura_respaldo):
    """Carga de manera segura un archivo JSON; retorna un fallback si no existe o falla."""
    if not os.path.exists(ruta_al_disco):
        return estructura_respaldo
    try:
        with open(ruta_al_disco, "r", encoding="utf-8") as flujo_archivo:
            return json.load(flujo_archivo)
    except json.JSONDecodeError:
        return estructura_respaldo

def _transaccionar_json_escritura(ruta_al_disco, datos_para_volcar):
    """Guarda datos estructurados en un archivo JSON."""
    with open(ruta_al_disco, "w", encoding="utf-8") as flujo_archivo:
        json.dump(datos_para_volcar, flujo_archivo, indent=4, ensure_ascii=False)

def _crear_pulsador_interactivo(padre, etiqueta_texto, tipografia, tono_fondo, tono_texto, comando_accion, anchura_x=20, altura_y=8):
    """Fabrica botones estandarizados con animaciones automáticas de hover."""
    pulsador = tk.Button(
        padre,
        text=etiqueta_texto,
        font=tipografia,
        bg=tono_fondo,
        fg=tono_texto,
        relief="raised",
        bd=2,
        padx=anchura_x,
        pady=altura_y,
        cursor="hand2",
        command=comando_accion
    )
    pulsador.bind("<Enter>", lambda evento: pulsador.config(bg=rojo_fuerte_claro if tono_fondo == rojo else cafe_claro))
    pulsador.bind("<Leave>", lambda evento: pulsador.config(bg=tono_fondo))
    return pulsador

def _desplegar_marco_flotante(padre, titulo_ventana, dimensiones_matriz):
    """Instancia ventanas secundarias (Toplevel) configuradas con el fondo general."""
    escenario_emergente = tk.Toplevel(padre) if padre else tk.Toplevel()
    escenario_emergente.title(titulo_ventana)
    escenario_emergente.geometry(dimensiones_matriz)
    escenario_emergente.config(bg=crema)
    return escenario_emergente

def cargar_usuarios():
    return _transaccionar_json_lectura(ubicacion_banco_identidades, {})

def login_usuario(usuario, contrasena, usuarios):
    llave_secreta_registrada = usuarios.get(usuario)
    return llave_secreta_registrada is not None and llave_secreta_registrada == contrasena

def guardar_recordar(usuario, contrasena):
    _transaccionar_json_escritura(ubicacion_memoria_sesion, {"usuario": usuario, "contrasena": contrasena})

def cargar_recordar():
    return _transaccionar_json_lectura(ubicacion_memoria_sesion, None)

def borrar_recordar():
    if os.path.exists(ubicacion_memoria_sesion):
        os.remove(ubicacion_memoria_sesion)

def cargar_menu():
    return _transaccionar_json_lectura(ubicacion_catalogo_ofertas, [])

def actualizar_total(pedido_actual, label_total):
    acumulado_monetario = sum(articulo["precio"] for articulo in pedido_actual)
    label_total.config(text=f"Total: ${acumulado_monetario:.2f}")

def agregar_producto(producto, pedido_actual, lista_pedido, label_total):
    dimensiones_subvariantes = producto.get("tamanos") or producto.get("tamaños")
    if dimensiones_subvariantes:
        mostrar_seleccion_tamano(producto, pedido_actual, lista_pedido, label_total)
        return
    
    pedido_actual.append(producto)
    lista_pedido.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f}")
    actualizar_total(pedido_actual, label_total)

def eliminar_producto(pedido_actual, lista_pedido, label_total):
    casilla_marcada = lista_pedido.curselection()
    if not casilla_marcada:
        messagebox.showinfo("Nada seleccionado", "Selecciona un producto de la lista para eliminar")
        return
    
    indice_posicional = casilla_marcada[0]
    elemento_sustraido = pedido_actual.pop(indice_posicional)
    lista_pedido.delete(indice_posicional)
    actualizar_total(pedido_actual, label_total)
    messagebox.showinfo("Producto eliminado", f"Se eliminó: {elemento_sustraido['nombre']}")

def mostrar_categoria(categoria, frame_productos, menu_productos, pedido_actual, lista_pedido, label_total):
    for componente in frame_productos.winfo_children():
        componente.destroy()
    
    emblema_seccion = cargar_icono_categoria(categoria)
    
    encabezado_contenedor = tk.Frame(frame_productos, bg=crema)
    encabezado_contenedor.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
    
    if emblema_seccion:
        etiqueta_grafica = tk.Label(encabezado_contenedor, image=emblema_seccion, bg=crema)
        etiqueta_grafica.pack(side="left")
        encabezado_contenedor.image = emblema_seccion
    
    tk.Label(
        encabezado_contenedor,
        text=f" {categoria}",
        font=titulo,
        bg=crema,
        fg=rojo
    ).pack(side="left")
    
    items_categoria_activa = [item for item in menu_productos if item["categoria"] == categoria]
    
    coordenada_y_fila = 1
    coordenada_x_columna = 0
    
    for item_menu in items_categoria_activa:
        bloque_producto = tk.Frame(
            frame_productos,
            bg=crema_oscuro,
            relief="raised",
            bd=3,
            highlightbackground=cafe_claro,
            highlightthickness=2,
            padx=15,
            pady=15,
            width=200,
            height=220
        )
        bloque_producto.grid(row=coordenada_y_fila, column=coordenada_x_columna, padx=12, pady=12, sticky="nsew")
        bloque_producto.pack_propagate(False)
        
        imagen_miniatura = cargar_imagen_productos(item_menu['nombre'], (120, 90))
        
        if imagen_miniatura:
            soporte_visual = tk.Label(bloque_producto, image=imagen_miniatura, bg=crema_oscuro)
            soporte_visual.pack(pady=(0, 8))
            soporte_visual.image = imagen_miniatura
        else:
            tk.Label(
                bloque_producto,
                text="Producto",
                font=letra_normal,
                bg=crema_oscuro,
                fg=cafe_medio
            ).pack(pady=(0, 8))
        
        nombre_visitable = item_menu['nombre']
        subopciones_talle = item_menu.get("tamanos") or item_menu.get("tamaños")
        rotulo_valor = "Tamaños disponibles" if subopciones_talle else f"${item_menu['precio']:.2f}"
        
        tk.Label(
            bloque_producto,
            text=nombre_visitable,
            font=letra_normal,
            bg=crema_oscuro,
            fg=texto,
            wraplength=160
        ).pack(anchor="center")
        
        tk.Label(
            bloque_producto,
            text=rotulo_valor,
            font=letra_normal,
            bg=crema_oscuro,
            fg=cafe_medio
        ).pack(anchor="center", pady=(5, 10))
        
        boton_accion_anadir = _crear_pulsador_interactivo(
            bloque_producto,
            "Agregar",
            letra_normal,
            rojo,
            texto_claro,
            lambda p=item_menu: agregar_producto(p, pedido_actual, lista_pedido, label_total)
        )
        boton_accion_anadir.pack()
        
        coordenada_x_columna += 1
        if coordenada_x_columna > 2:
            coordenada_x_columna = 0
            coordenada_y_fila += 1
    
    for indice_col in range(3):
        frame_productos.grid_columnconfigure(indice_col, weight=1)

def mostrar_seleccion_tamano(producto, pedido_actual, lista_pedido, label_total):
    subescenario_medidas = _desplegar_marco_flotante(None, f"Elige el tamaño - {producto['nombre']}", "320x400")
    
    tk.Label(
        subescenario_medidas,
        text=f"{producto['nombre']}",
        font=titulo,
        bg=crema,
        fg=rojo
    ).pack(pady=(20, 10))
    
    tk.Label(
        subescenario_medidas,
        text="Selecciona el tamaño:",
        font=letra_normal,
        bg=crema,
        fg=texto
    ).pack(pady=(0, 15))
    
    def asimilar_variacion(etiqueta_volumen, importe_especifico):
        item_modificado = {
            "categoria": producto["categoria"],
            "nombre": f"{producto['nombre']} ({etiqueta_volumen})",
            "precio": importe_especifico
        }
        pedido_actual.append(item_modificado)
        lista_pedido.insert(tk.END, f"{item_modificado['nombre']} - ${item_modificado['precio']:.2f}")
        actualizar_total(pedido_actual, label_total)
        subescenario_medidas.destroy()
    
    panel_opciones_talle = tk.Frame(subescenario_medidas, bg=crema)
    panel_opciones_talle.pack(pady=10)
    
    diccionario_escala = producto.get("tamanos") or producto.get("tamaños", {})
    for especificacion_talle, costo_asociado in diccionario_escala.items():
        boton_opcion = _crear_pulsador_interactivo(
            panel_opciones_talle,
            f"{especificacion_talle} - ${costo_asociado:.2f}",
            letra_normal,
            crema_oscuro,
            texto,
            lambda t=especificacion_talle, pr=costo_asociado: asimilar_variacion(t, pr),
            anchura_x=30,
            altura_y=12
        )
        boton_opcion.pack(pady=5)

def confirmar_pedido(pedido_actual, ventana_padre, lista_pedido, label_total):
    if not pedido_actual:
        messagebox.showwarning("Pedido vacio", "Agrega un producto o pedido")
        return

    escenario_verificacion = _desplegar_marco_flotante(ventana_padre, "Confirmar Pedido", "380x450")

    tk.Label(
        escenario_verificacion,
        text="Detalle del pedido",
        font=subtitulo,
        bg=crema,
        fg=texto
    ).pack(pady=(15, 10))

    visores_resumen_compra = tk.Listbox(escenario_verificacion, width=40, height=15)
    visores_resumen_compra.pack(padx=15, pady=10, fill="both", expand=True)

    for item_solicitado in pedido_actual:
        visores_resumen_compra.insert(tk.END, f"{item_solicitado['nombre']} - ${item_solicitado['precio']:.2f}")

    subtotal_calculado_bruto = sum(item["precio"] for item in pedido_actual)
    tk.Label(
        escenario_verificacion,
        text=f"Total: ${subtotal_calculado_bruto:.2f}",
        font=letra_de_botones,
        bg=crema,
        fg=rojo
    ).pack(pady=(0, 15))

    contenedor_comandos = tk.Frame(escenario_verificacion, bg=crema)
    contenedor_comandos.pack(pady=(0, 15))

    def migrar_hacia_factura():
        escenario_verificacion.destroy()
        mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, subtotal_calculado_bruto)

    btn_fijar = _crear_pulsador_interactivo(
        contenedor_comandos, "Confirmar Pedido", letra_de_botones, rojo, texto_claro, migrar_hacia_factura, 20, 10
    )
    btn_fijar.pack(side="left", padx=5)

    btn_retorno = _crear_pulsador_interactivo(
        contenedor_comandos, "Seguir editando", letra_de_botones, cafe_medio, texto_claro, escenario_verificacion.destroy, 20, 10
    )
    btn_retorno.pack(side="left", padx=5)

def cargar_facturas():
    return _transaccionar_json_lectura(ubicacion_libro_transacciones, [])

def guardar_factura(factura):
    registros_previos = cargar_facturas()
    registros_previos.append(factura)
    _transaccionar_json_escritura(ubicacion_libro_transacciones, registros_previos)

def generar_numero_factura():
    return len(cargar_facturas()) + 1

def cargar_domicilio():
    return _transaccionar_json_lectura(ubicacion_logistica_tarifa, {"tarifa_fija": 1.00, "tarifa_km": 0.50})

def calcular_costo_domicilio(km, tarifa_fija, tarifa_km):
    return (tarifa_km * km) + tarifa_fija

def generar_tabla_de_domicilios(tarifa_fija, tarifa_km, km_maximo=5):
    return [(kilometro, calcular_costo_domicilio(kilometro, tarifa_fija, tarifa_km)) for kilometro in range(1, km_maximo + 1)]

def mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, subtotal):
    pantalla_cobro = _desplegar_marco_flotante(ventana_padre, "Facturacion", "440x820")

    subtotal_impuesto_aplicado = subtotal * factor_recargo_tributario
    monto_flete_calculado = 0.0

    tk.Label(pantalla_cobro, text="DATOS DEL CLIENTE", font=subtitulo, bg=crema, fg=texto).pack(pady=(15, 10))

    bloque_inputs_comprador = tk.Frame(pantalla_cobro, bg=crema)
    bloque_inputs_comprador.pack(padx=20, pady=(0, 10), fill="x")

    def _generar_campo_entrada(rotulo_campo):
        tk.Label(bloque_inputs_comprador, text=rotulo_campo, bg=crema, anchor="w", font=letra_normal).pack(fill="x")
        variable_almacenadora = tk.StringVar()
        tk.Entry(bloque_inputs_comprador, textvariable=variable_almacenadora, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))
        return variable_almacenadora

    nombre_var = _generar_campo_entrada("Nombres completos:")
    cedula_var = _generar_campo_entrada("Cedula:")
    telefono_var = _generar_campo_entrada("Telefono:")
    direccion_var = _generar_campo_entrada("Direccion:")
    correo_var = _generar_campo_entrada("Correo Electronico:")

    visor_feedback_notificacion = tk.Label(bloque_inputs_comprador, text="", fg=rojo, bg=crema, font=letra_normal)
    visor_feedback_notificacion.pack()

    tk.Label(pantalla_cobro, text="Detalle de facturacion", font=subtitulo, bg=crema, fg=texto).pack(pady=(10, 5))

    listado_desglose_compra = tk.Listbox(pantalla_cobro, width=45, height=6, font=letra_normal)
    listado_desglose_compra.pack(padx=20, pady=(0, 10), fill="both", expand=True)

    for articulo_comprado in pedido_actual:
        listado_desglose_compra.insert(tk.END, f"{articulo_comprado['nombre']} - ${articulo_comprado['precio']:.2f}")

    tk.Label(pantalla_cobro, text="Servicio a domicilio", font=letra_normal, bg=crema, fg=cafe_oscuro).pack(pady=(10, 5))

    flag_despliegue_entrega = tk.BooleanVar()
    panel_parametrizacion_flete = tk.Frame(pantalla_cobro, bg=crema)

    parametros_envio = cargar_domicilio()
    monto_base_estatico = parametros_envio.get("tarifa_fija", 1.0)
    monto_por_distancia = parametros_envio.get("tarifa_km", 0.5)

    tk.Label(
        panel_parametrizacion_flete,
        text=f"Tarifa/km: ${monto_por_distancia:.2f} - Tarifa fija: ${monto_base_estatico:.2f}",
        bg=crema,
        fg=cafe_medio,
        font=letra_pequena
    ).pack(pady=(2, 6))

    tk.Label(panel_parametrizacion_flete, text="Distancia (km): ", bg=crema, anchor="w", font=letra_normal).pack(fill="x")

    kilometraje_ingresado_var = tk.StringVar()
    tk.Entry(
        panel_parametrizacion_flete,
        textvariable=kilometraje_ingresado_var,
        width=15,
        font=letra_normal,
        relief="solid",
        bd=1
    ).pack(pady=(0, 5))

    rotulo_costo_envio = tk.Label(panel_parametrizacion_flete, text="Costo de envio: $0.00", bg=crema, font=letra_normal)
    rotulo_costo_envio.pack()

    receptaculo_esquema_tarifario = tk.Listbox(panel_parametrizacion_flete, width=30, height=5, font=letra_pequena)

    def refrescar_indicador_monetario():
        monto_consolidado_final = subtotal + subtotal_impuesto_aplicado + monto_flete_calculado
        label_total_final.config(text=f"Total: ${monto_consolidado_final:.2f}")

    def computar_flete_desplazamiento():
        nonlocal monto_flete_calculado
        cadena_lectura_km = kilometraje_ingresado_var.get().strip()

        if cadena_lectura_km == "":
            visor_feedback_notificacion.config(text="Ingresa la distancia en km")
            return
        try:
            magnitud_distancia = float(cadena_lectura_km)
        except ValueError:
            visor_feedback_notificacion.config(text="La distancia debe ser un numero")
            return
        if magnitud_distancia < 0:
            visor_feedback_notificacion.config(text="La distancia no puede ser negativa")
            return

        monto_flete_calculado = calcular_costo_domicilio(magnitud_distancia, monto_base_estatico, monto_por_distancia)
        rotulo_costo_envio.config(text=f"Costo de envio: ${monto_flete_calculado:.2f}")
        visor_feedback_notificacion.config(text="")
        refrescar_indicador_monetario()

    def desplegar_matriz_tarifas():
        receptaculo_esquema_tarifario.delete(0, tk.END)
        esquema_distancias = generar_tabla_de_domicilios(monto_base_estatico, monto_por_distancia, km_maximo=5)
        for km, costo in esquema_distancias:
            receptaculo_esquema_tarifario.insert(tk.END, f"f({km}) = {monto_por_distancia}({km}) + {monto_base_estatico} = ${costo:.2f}")
        receptaculo_esquema_tarifario.pack(pady=(5, 5))

    _crear_pulsador_interactivo(
        panel_parametrizacion_flete, "Calcular envio", letra_normal, crema_oscuro, texto, computar_flete_desplazamiento, 10, 5
    ).pack(pady=(0, 5))

    _crear_pulsador_interactivo(
        panel_parametrizacion_flete, "Ver tabla (1-5 km)", letra_normal, crema_oscuro, texto, desplegar_matriz_tarifas, 10, 5
    ).pack(pady=(0, 5))

    def alternar_logistica_flete():
        nonlocal monto_flete_calculado
        if flag_despliegue_entrega.get():
            panel_parametrizacion_flete.pack(padx=20, pady=(0, 10), fill="x")
        else:
            monto_flete_calculado = 0.0
            kilometraje_ingresado_var.set("")
            rotulo_costo_envio.config(text="Costo de envio: $0.00")
            receptaculo_esquema_tarifario.delete(0, tk.END)
            panel_parametrizacion_flete.pack_forget()
            refrescar_indicador_monetario()

    tk.Checkbutton(
        pantalla_cobro,
        text="Es domicilio?",
        variable=flag_despliegue_entrega,
        bg=crema,
        fg=texto,
        font=letra_normal,
        command=alternar_logistica_flete
    ).pack()

    tk.Label(pantalla_cobro, text=f"Subtotal: ${subtotal:.2f}", bg=crema, font=letra_normal).pack(pady=(10, 0))
    tk.Label(pantalla_cobro, text=f"Iva (15%): ${subtotal_impuesto_aplicado:.2f}", bg=crema, font=letra_normal).pack()

    label_total_final = tk.Label(
        pantalla_cobro,
        text=f"Total: ${(subtotal + subtotal_impuesto_aplicado):.2f}",
        font=titulo,
        bg=crema,
        fg=rojo
    )
    label_total_final.pack(pady=(5, 10))

    bloque_ejecucion_factura = tk.Frame(pantalla_cobro, bg=crema)
    bloque_ejecucion_factura.pack(pady=(0, 15))

    def asentar_emision_factura():
        nombre_str = nombre_var.get().strip()
        cedula_str = cedula_var.get().strip()
        telefono_str = telefono_var.get().strip()
        direccion_str = direccion_var.get().strip()
        correo_str = correo_var.get().strip()

        if not all([nombre_str, cedula_str, telefono_str, direccion_str, correo_str]):
            visor_feedback_notificacion.config(text="Completa todos los datos del cliente")
            return

        if flag_despliegue_entrega.get() and monto_flete_calculado == 0.0:
            visor_feedback_notificacion.config(text="Calcular el costo de envio antes de confirmar")
            return

        secuencial_factura = generar_numero_factura()
        gran_total_liquidado = subtotal + subtotal_impuesto_aplicado + monto_flete_calculado

        registro_comprobante = {
            "numero": secuencial_factura,
            "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "cliente": {
                "nombre": nombre_str,
                "cedula": cedula_str,
                "telefono": telefono_str,
                "direccion": direccion_str,
                "correo": correo_str
            },
            "detalle": pedido_actual.copy(),
            "subtotal": subtotal,
            "iva": subtotal_impuesto_aplicado,
            "domicilio": monto_flete_calculado,
            "total": gran_total_liquidado
        }
        guardar_factura(registro_comprobante)

        messagebox.showinfo(
            "Factura generada",
            f"Factura N° {secuencial_factura} generada con exito. Total: ${gran_total_liquidado:.2f}"
        )

        pedido_actual.clear()
        lista_pedido.delete(0, tk.END)
        actualizar_total(pedido_actual, label_total)
        pantalla_cobro.destroy()

    _crear_pulsador_interactivo(
        bloque_ejecucion_factura, "Confirmar Factura", letra_grande, rojo, texto_claro, asentar_emision_factura, 20, 10
    ).pack(side="left", padx=5)

    _crear_pulsador_interactivo(
        bloque_ejecucion_factura, "Cancelar", letra_grande, cafe_medio, texto_claro, pantalla_cobro.destroy, 20, 10
    ).pack(side="left", padx=5)

def mostrar_historial(ventana_padre):
    pantalla_auditoria = _desplegar_marco_flotante(ventana_padre, "Historial de Facturas", "500x600")

    tk.Label(pantalla_auditoria, text="Historial de facturas", font=titulo, bg=crema, fg=rojo).pack(pady=(15, 10))

    panel_filtro_busqueda = tk.Frame(pantalla_auditoria, bg=crema)
    panel_filtro_busqueda.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(panel_filtro_busqueda, text="Ingrese numero de factura o cliente", bg=crema, anchor="w", font=letra_normal).pack(fill="x")

    parametro_busqueda_var = tk.StringVar()
    tk.Entry(panel_filtro_busqueda, textvariable=parametro_busqueda_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(5, 5))

    panel_acciones_historial = tk.Frame(panel_filtro_busqueda, bg=crema)
    panel_acciones_historial.pack(pady=5)

    lista_resultados_coincidencias = tk.Listbox(pantalla_auditoria, width=60, height=15, font=letra_normal)
    lista_resultados_coincidencias.pack(padx=20, pady=(5, 10), fill="both", expand=True)

    etiqueta_estado_auditoria = tk.Label(pantalla_auditoria, text="", bg=crema, fg=cafe_medio, font=letra_normal)
    etiqueta_estado_auditoria.pack()

    def renderizar_lista_comprobantes(comprobantes):
        lista_resultados_coincidencias.delete(0, tk.END)
        if not comprobantes:
            etiqueta_estado_auditoria.config(text="No se encuentra factura")
            return
        etiqueta_estado_auditoria.config(text=f"{len(comprobantes)} factura(s) encontrada(s)")
        for comp in comprobantes:
            lista_resultados_coincidencias.insert(
                tk.END,
                f"N°{comp['numero']} | {comp['fecha']} | "
                f"{comp['cliente']['nombre']} ({comp['cliente']['cedula']}) | "
                f"Total: ${comp['total']:.2f}"
            )

    def ejecutar_despliegue_total():
        renderizar_lista_comprobantes(cargar_facturas())

    def ejecutar_filtrado():
        criterio_evaluado = parametro_busqueda_var.get().strip()

        if criterio_evaluado == "":
            etiqueta_estado_auditoria.config(text="Ingrese la cedula o nombre del cliente para buscar:")
            return

        registros_totales = cargar_facturas()
        
        if criterio_evaluado.isdigit():
            identificador_num = int(criterio_evaluado)
            coincidencias = [f for f in registros_totales if f["numero"] == identificador_num]
        else:
            busqueda_minuscula = criterio_evaluado.lower()
            coincidencias = [
                f for f in registros_totales
                if busqueda_minuscula in f['cliente']["nombre"].lower()
                or busqueda_minuscula in f['cliente']["cedula"].lower()
            ]

        renderizar_lista_comprobantes(coincidencias)

    def inspeccionar_factura_especifica(evento_pulsacion):
        marcado = lista_resultados_coincidencias.curselection()
        if not marcado:
            return

        texto_cadena = lista_resultados_coincidencias.get(marcado[0])
        extraer_id_bruto = texto_cadena.split("|")[0].replace("N°", "").strip()

        try:
            id_factura_buscada = int(extraer_id_bruto)
        except ValueError:
            return

        objeto_factura = next((f for f in cargar_facturas() if f["numero"] == id_factura_buscada), None)

        if objeto_factura is None:
            return

        ventana_inspeccion = _desplegar_marco_flotante(pantalla_auditoria, f"Factura N° {objeto_factura['numero']}", "360x560")

        tk.Label(
            ventana_inspeccion,
            text=f"Factura N°{objeto_factura['numero']}",
            font=titulo,
            bg=crema,
            fg=rojo
        ).pack(pady=(15, 5))

        datos_perfil_cliente = objeto_factura["cliente"]
        tk.Label(ventana_inspeccion, text=f"Nombre: {datos_perfil_cliente.get('nombre', '')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"Cedula: {datos_perfil_cliente.get('cedula', '')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"Telefono: {datos_perfil_cliente.get('telefono', '-')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"Direccion: {datos_perfil_cliente.get('direccion', '-')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"Correo: {datos_perfil_cliente.get('correo', '')}", bg=crema, font=letra_normal).pack(pady=(0, 10))

        visor_items_facturados = tk.Listbox(ventana_inspeccion, width=40, height=8, font=letra_normal)
        visor_items_facturados.pack(padx=15, pady=(0, 10), fill="both", expand=True)
        
        for elem in objeto_factura["detalle"]:
            visor_items_facturados.insert(tk.END, f"{elem['nombre']} - ${elem['precio']:.2f}")

        tk.Label(ventana_inspeccion, text=f"Subtotal: ${objeto_factura['subtotal']:.2f}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"IVA: ${objeto_factura['iva']:.2f}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_inspeccion, text=f"Domicilio: ${objeto_factura.get('domicilio', 0):.2f}", bg=crema, font=letra_normal).pack()

        tk.Label(
            ventana_inspeccion,
            text=f"Total: ${objeto_factura['total']:.2f}",
            font=subtitulo,
            bg=crema,
            fg=rojo
        ).pack(pady=(5, 15))

    lista_resultados_coincidencias.bind("<Double-1>", inspeccionar_factura_especifica)

    tk.Label(
        pantalla_auditoria,
        text="Presione doble click para visualizar completa la factura",
        bg=crema,
        fg=cafe_medio,
        font=letra_pequena
    ).pack(pady=(0, 5))

    _crear_pulsador_interactivo(
        panel_acciones_historial, "Buscar", letra_grande, rojo, texto_claro, ejecutar_filtrado, 20, 8
    ).pack(side="left", padx=5)

    _crear_pulsador_interactivo(
        panel_acciones_historial, "Ver todas", letra_de_botones, cafe_medio, texto_claro, ejecutar_despliegue_total, 20, 8
    ).pack(side="left", padx=5)

    ejecutar_despliegue_total()