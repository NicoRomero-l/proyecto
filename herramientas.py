## ventana de herramientas, aunque no es una ventana :b
## simplemente es de donde va a sacar las funciones todo mi programa

# Funciones del sistema

import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from colores import *
from imagenes import cargar_imagen_productos, cargar_icono_categoria

#===========================================================
# Variables del Login
#===========================================================
archivo_usuarios="usuarios.json"
archivo_recordar="recordar.json"

#===========================================================
# Variable del Menu
#===========================================================
archivo_menu="menu.json"

#===========================================================
# Variable de las Facturas
#===========================================================
archivo_facturas="facturacion.json"
iva_porcentaje=0.15

#===========================================================
# Variable del domicilio
#===========================================================
archivo_domicilio="domicilio.json"

#===========================================================
# Funciones del Login
#===========================================================

def cargar_usuarios():
    if not os.path.exists(archivo_usuarios):
        return {}
    try:
        with open(archivo_usuarios, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def login_usuario(usuario, contrasena, usuarios):
    contrasena_guardada=usuarios.get(usuario)
    return contrasena_guardada is not None and contrasena_guardada == contrasena

def guardar_recordar(usuario, contrasena):
    datos={"usuario": usuario, "contrasena": contrasena}
    with open(archivo_recordar, "w", encoding="utf-8") as f:
        json.dump(datos, f)

def cargar_recordar():
    if not os.path.exists(archivo_recordar):
        return None
    try:
        with open(archivo_recordar, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def borrar_recordar():
    if os.path.exists(archivo_recordar):
        os.remove(archivo_recordar)

#===========================================================
# Funciones del Menu
#===========================================================

def cargar_menu():
    if not os.path.exists(archivo_menu):
        return []
    try:
        with open(archivo_menu, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def actualizar_total(pedido_actual, label_total):
    total=sum(p["precio"] for p in pedido_actual)
    label_total.config(text=f"Total: ${total:.2f}")

def agregar_producto(producto, pedido_actual, lista_pedido, label_total):
    tamanos=producto.get("tamanos") or producto.get("tamaños")
    if tamanos:
        mostrar_seleccion_tamano(producto, pedido_actual, lista_pedido, label_total)
        return
    
    pedido_actual.append(producto)
    lista_pedido.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f}")
    actualizar_total(pedido_actual, label_total)

def eliminar_producto(pedido_actual, lista_pedido, label_total):
    seleccion=lista_pedido.curselection()
    if not seleccion:
        messagebox.showinfo("Nada seleccionado", "Selecciona un producto de la lista para eliminar")
        return
    
    indice=seleccion[0]
    producto_eliminado=pedido_actual.pop(indice)
    lista_pedido.delete(indice)
    actualizar_total(pedido_actual, label_total)
    messagebox.showinfo("Producto eliminado", f"Se eliminó: {producto_eliminado['nombre']}")

#===========================================================
# Mostrar categoria con imagenes
#===========================================================

def mostrar_categoria(categoria, frame_productos, menu_productos, pedido_actual, lista_pedido, label_total):
    for widget in frame_productos.winfo_children():
        widget.destroy()
    
    icono_cat=cargar_icono_categoria(categoria)
    
    frame_titulo=tk.Frame(frame_productos, bg=crema)
    frame_titulo.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
    
    if icono_cat:
        label_icono=tk.Label(frame_titulo, image=icono_cat, bg=crema)
        label_icono.pack(side="left")
        frame_titulo.image=icono_cat
    
    tk.Label(
        frame_titulo,
        text=f" {categoria}",
        font=titulo,
        bg=crema,
        fg=rojo
    ).pack(side="left")
    
    productos_filtrados=[p for p in menu_productos if p["categoria"] == categoria]
    
    fila=1
    columna=0
    
    for producto in productos_filtrados:
        tarjeta=tk.Frame(
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
        tarjeta.grid(row=fila, column=columna, padx=12, pady=12, sticky="nsew")
        tarjeta.pack_propagate(False)
        
        img_producto=cargar_imagen_productos(producto['nombre'], (120, 90))
        
        if img_producto:
            label_img=tk.Label(tarjeta, image=img_producto, bg=crema_oscuro)
            label_img.pack(pady=(0, 8))
            label_img.image=img_producto
        else:
            tk.Label(
                tarjeta,
                text="Producto",
                font=letra_normal,
                bg=crema_oscuro,
                fg=cafe_medio
            ).pack(pady=(0, 8))
        
        nombre_texto=producto['nombre']
        tamanos=producto.get("tamanos") or producto.get("tamaños")
        precio_texto="Tamaños disponibles" if tamanos else f"${producto['precio']:.2f}"
        
        tk.Label(
            tarjeta,
            text=nombre_texto,
            font=letra_normal,
            bg=crema_oscuro,
            fg=texto,
            wraplength=160
        ).pack(anchor="center")
        
        tk.Label(
            tarjeta,
            text=precio_texto,
            font=letra_normal,
            bg=crema_oscuro,
            fg=cafe_medio
        ).pack(anchor="center", pady=(5, 10))
        
        boton_filtraciones=tk.Button(
            tarjeta,
            text="Agregar",
            font=letra_normal,
            bg=rojo,
            fg=texto_claro,
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda p=producto: agregar_producto(p, pedido_actual, lista_pedido, label_total)
        )
        boton_filtraciones.pack()
        
        def hover_on(e, b=boton_filtraciones):
            b.config(bg=rojo_fuerte_claro)
        def hover_off(e, b=boton_filtraciones):
            b.config(bg=rojo)
        
        boton_filtraciones.bind("<Enter>", hover_on)
        boton_filtraciones.bind("<Leave>", hover_off)
        
        columna+=1
        if columna > 2:
            columna=0
            fila+=1
    
    for i in range(3):
        frame_productos.grid_columnconfigure(i, weight=1)

def mostrar_seleccion_tamano(producto, pedido_actual, lista_pedido, label_total):
    ventana_tamano=tk.Toplevel()
    ventana_tamano.title(f"Elige el tamaño - {producto['nombre']}")
    ventana_tamano.geometry("320x400")
    ventana_tamano.config(bg=crema)
    
    tk.Label(
        ventana_tamano,
        text=f"{producto['nombre']}",
        font=titulo,
        bg=crema,
        fg=rojo
    ).pack(pady=(20, 10))
    
    tk.Label(
        ventana_tamano,
        text="Selecciona el tamaño:",
        font=letra_normal,
        bg=crema,
        fg=texto
    ).pack(pady=(0, 15))
    
    def elegir(tamano, precio):
        producto_con_tamano={
            "categoria": producto["categoria"],
            "nombre": f"{producto['nombre']} ({tamano})",
            "precio": precio
        }
        pedido_actual.append(producto_con_tamano)
        lista_pedido.insert(tk.END, f"{producto_con_tamano['nombre']} - ${producto_con_tamano['precio']:.2f}")
        actualizar_total(pedido_actual, label_total)
        ventana_tamano.destroy()
    
    frame_tamanos=tk.Frame(ventana_tamano, bg=crema)
    frame_tamanos.pack(pady=10)
    
    tamanos=producto.get("tamanos") or producto.get("tamaños", {})
    for tamano, precio in tamanos.items():
        btn=tk.Button(
            frame_tamanos,
            text=f"{tamano} - ${precio:.2f}",
            font=letra_normal,
            bg=crema_oscuro,
            fg=texto,
            relief="raised",
            bd=2,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda t=tamano, pr=precio: elegir(t, pr)
        )
        btn.pack(pady=5)
        
        def hover_on(e, b=btn):
            b.config(bg=cafe_claro)
        def hover_off(e, b=btn):
            b.config(bg=crema_oscuro)
        
        btn.bind("<Enter>", hover_on)
        btn.bind("<Leave>", hover_off)

#===========================================================
# Funcion para confirmar pedido
#===========================================================

def confirmar_pedido(pedido_actual, ventana_padre, lista_pedido, label_total):
    if not pedido_actual:
        messagebox.showwarning("Pedido vacio", "Agrega un producto o pedido")
        return

    ventana_confirmar=tk.Toplevel(ventana_padre)
    ventana_confirmar.title("Confirmar Pedido")
    ventana_confirmar.geometry("380x450")
    ventana_confirmar.config(bg=crema)

    tk.Label(
        ventana_confirmar,
        text="Detalle del pedido",
        font=subtitulo,
        bg=crema,
        fg=texto
    ).pack(pady=(15, 10))

    lista_detalle=tk.Listbox(ventana_confirmar, width=40, height=15)
    lista_detalle.pack(padx=15, pady=10, fill="both", expand=True)

    for producto in pedido_actual:
        lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f}")

    total=sum(p["precio"] for p in pedido_actual)
    tk.Label(
        ventana_confirmar,
        text=f"Total: ${total:.2f}",
        font=letra_de_botones,
        bg=crema,
        fg=rojo
    ).pack(pady=(0, 15))

    frame_botones=tk.Frame(ventana_confirmar, bg=crema)
    frame_botones.pack(pady=(0, 15))

    def ir_a_facturacion():
        ventana_confirmar.destroy()
        mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, total)

    def seguir_editando():
        ventana_confirmar.destroy()

    tk.Button(
        frame_botones,
        text="Confirmar Pedido",
        font=letra_de_botones,
        bg=rojo,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=10,
        cursor="hand2",
        command=ir_a_facturacion
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Seguir editando",
        font=letra_de_botones,
        bg=cafe_medio,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=10,
        cursor="hand2",
        command=seguir_editando
    ).pack(side="left", padx=5)

#===========================================================
# Funciones de facturas
#===========================================================

def cargar_facturas():
    if not os.path.exists(archivo_facturas):
        return []
    try:
        with open(archivo_facturas, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_factura(factura):
    facturas=cargar_facturas()
    facturas.append(factura)
    with open(archivo_facturas, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)

def generar_numero_factura():
    facturas=cargar_facturas()
    return len(facturas) + 1

#===========================================================
# Funcion para calcular envios a domicilio (funcion afin)
#===========================================================

def cargar_domicilio():
    if not os.path.exists(archivo_domicilio):
        return {"tarifa_fija": 1.00, "tarifa_km": 0.50}
    try:
        with open(archivo_domicilio, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"tarifa_fija": 1.00, "tarifa_km": 0.50}

def calcular_costo_domicilio(km, tarifa_fija, tarifa_km):
    return (tarifa_km * km) + tarifa_fija

def generar_tabla_de_domicilios(tarifa_fija, tarifa_km, km_maximo=5):
    tabla=[]
    for km in range(1, km_maximo + 1):
        costo=calcular_costo_domicilio(km, tarifa_fija, tarifa_km)
        tabla.append((km, costo))
    return tabla

#===========================================================
# Funcion para mostrar la ventana de facturacion
#===========================================================

def mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, subtotal):
    ventana_facturacion=tk.Toplevel(ventana_padre)
    ventana_facturacion.title("Facturacion")
    ventana_facturacion.geometry("440x820")
    ventana_facturacion.config(bg=crema)

    iva=subtotal * iva_porcentaje
    costo_domicilio=0.0

    tk.Label(
        ventana_facturacion,
        text="DATOS DEL CLIENTE",
        font=subtitulo,
        bg=crema,
        fg=texto
    ).pack(pady=(15, 10))

    frame_datos=tk.Frame(ventana_facturacion, bg=crema)
    frame_datos.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(frame_datos, text="Nombres completos:", bg=crema, anchor="w", font=letra_normal).pack(fill="x")
    nombre_var=tk.StringVar()
    tk.Entry(frame_datos, textvariable=nombre_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Cedula:", bg=crema, anchor="w", font=letra_normal).pack(fill="x")
    cedula_var=tk.StringVar()
    tk.Entry(frame_datos, textvariable=cedula_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Telefono:", bg=crema, anchor="w", font=letra_normal).pack(fill="x")
    telefono_var=tk.StringVar()
    tk.Entry(frame_datos, textvariable=telefono_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Direccion:", bg=crema, anchor="w", font=letra_normal).pack(fill="x")
    direccion_var=tk.StringVar()
    tk.Entry(frame_datos, textvariable=direccion_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Correo Electronico:", bg=crema, anchor="w", font=letra_normal).pack(fill="x")
    correo_var=tk.StringVar()
    tk.Entry(frame_datos, textvariable=correo_var, width=35, font=letra_normal, relief="solid", bd=1).pack(pady=(0, 8))

    label_estado=tk.Label(frame_datos, text="", fg=rojo, bg=crema, font=letra_normal)
    label_estado.pack()

    tk.Label(
        ventana_facturacion,
        text="Detalle de facturacion",
        font=subtitulo,
        bg=crema,
        fg=texto
    ).pack(pady=(10, 5))

    lista_detalle=tk.Listbox(ventana_facturacion, width=45, height=6, font=letra_normal)
    lista_detalle.pack(padx=20, pady=(0, 10), fill="both", expand=True)

    for producto in pedido_actual:
        lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f}")

    #===========================================================
    # Servicio a domicilio (funcion afin) f(x)=m*x + b
    #===========================================================
    tk.Label(
        ventana_facturacion,
        text="Servicio a domicilio",
        font=letra_normal,
        bg=crema,
        fg=cafe_oscuro
    ).pack(pady=(10, 5))

    domicilio_var=tk.BooleanVar()
    frame_domicilio=tk.Frame(ventana_facturacion, bg=crema)

    datos_domicilio=cargar_domicilio()
    tarifa_fija=datos_domicilio.get("tarifa_fija", 1.0)
    tarifa_km=datos_domicilio.get("tarifa_km", 0.5)

    tk.Label(
        frame_domicilio,
        text=f"Tarifa/km: ${tarifa_km:.2f} - Tarifa fija: ${tarifa_fija:.2f}",
        bg=crema,
        fg=cafe_medio,
        font=letra_pequena
    ).pack(pady=(2, 6))

    tk.Label(
        frame_domicilio,
        text="Distancia (km): ",
        bg=crema,
        anchor="w",
        font=letra_normal
    ).pack(fill="x")

    km_var=tk.StringVar()
    tk.Entry(
        frame_domicilio,
        textvariable=km_var,
        width=15,
        font=letra_normal,
        relief="solid",
        bd=1
    ).pack(pady=(0, 5))

    label_costo_domicilio=tk.Label(frame_domicilio, text="Costo de envio: $0.00", bg=crema, font=letra_normal)
    label_costo_domicilio.pack()

    lista_tabla=tk.Listbox(frame_domicilio, width=30, height=5, font=letra_pequena)

    def actualizar_total_visual():
        total_actual=subtotal + iva + costo_domicilio
        label_total_final.config(text=f"Total: ${total_actual:.2f}")

    def calcular_envio():
        nonlocal costo_domicilio
        km_texto=km_var.get().strip()

        if km_texto == "":
            label_estado.config(text="Ingresa la distancia en km")
            return
        try:
            km=float(km_texto)
        except ValueError:
            label_estado.config(text="La distancia debe ser un numero")
            return
        if km < 0:
            label_estado.config(text="La distancia no puede ser negativa")
            return

        costo_domicilio=calcular_costo_domicilio(km, tarifa_fija, tarifa_km)
        label_costo_domicilio.config(text=f"Costo de envio: ${costo_domicilio:.2f}")
        label_estado.config(text="")
        actualizar_total_visual()

    def ver_tabla():
        lista_tabla.delete(0, tk.END)
        tabla=generar_tabla_de_domicilios(tarifa_fija, tarifa_km, km_maximo=5)
        for km, costo in tabla:
            lista_tabla.insert(tk.END, f"f({km}) = {tarifa_km}({km}) + {tarifa_fija} = ${costo:.2f}")
        lista_tabla.pack(pady=(5, 5))

    tk.Button(
        frame_domicilio,
        text="Calcular envio",
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        relief="raised",
        bd=2,
        padx=10,
        pady=5,
        cursor="hand2",
        command=calcular_envio
    ).pack(pady=(0, 5))

    tk.Button(
        frame_domicilio,
        text="Ver tabla (1-5 km)",
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        relief="raised",
        bd=2,
        padx=10,
        pady=5,
        cursor="hand2",
        command=ver_tabla
    ).pack(pady=(0, 5))

    def toggle_domicilio():
        nonlocal costo_domicilio
        if domicilio_var.get():
            frame_domicilio.pack(padx=20, pady=(0, 10), fill="x")
        else:
            costo_domicilio=0.0
            km_var.set("")
            label_costo_domicilio.config(text="Costo de envio: $0.00")
            lista_tabla.delete(0, tk.END)
            frame_domicilio.pack_forget()
            actualizar_total_visual()

    tk.Checkbutton(
        ventana_facturacion,
        text="Es domicilio?",
        variable=domicilio_var,
        bg=crema,
        fg=texto,
        font=letra_normal,
        command=toggle_domicilio
    ).pack()

    #===========================================================
    # Totales
    #===========================================================
    tk.Label(ventana_facturacion, text=f"Subtotal: ${subtotal:.2f}", bg=crema, font=letra_normal).pack(pady=(10, 0))
    tk.Label(ventana_facturacion, text=f"Iva (15%): ${iva:.2f}", bg=crema, font=letra_normal).pack()

    label_total_final=tk.Label(
        ventana_facturacion,
        text=f"Total: ${(subtotal + iva):.2f}",
        font=titulo,
        bg=crema,
        fg=rojo
    )
    label_total_final.pack(pady=(5, 10))

    frame_botones=tk.Frame(ventana_facturacion, bg=crema)
    frame_botones.pack(pady=(0, 15))

    def confirmar_factura():
        nombre=nombre_var.get().strip()
        cedula=cedula_var.get().strip()
        telefono=telefono_var.get().strip()
        direccion=direccion_var.get().strip()
        correo=correo_var.get().strip()

        if nombre == "" or cedula == "" or telefono == "" or direccion == "" or correo == "":
            label_estado.config(text="Completa todos los datos del cliente")
            return

        if domicilio_var.get() and costo_domicilio == 0.0:
            label_estado.config(text="Calcular el costo de envio antes de confirmar")
            return

        numero=generar_numero_factura()
        total_final=subtotal + iva + costo_domicilio

        factura={
            "numero": numero,
            "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "cliente": {
                "nombre": nombre,
                "cedula": cedula,
                "telefono": telefono,
                "direccion": direccion,
                "correo": correo
            },
            "detalle": pedido_actual.copy(),
            "subtotal": subtotal,
            "iva": iva,
            "domicilio": costo_domicilio,
            "total": total_final
        }
        guardar_factura(factura)

        messagebox.showinfo(
            "Factura generada",
            f"Factura N° {numero} generada con exito. Total: ${total_final:.2f}"
        )

        pedido_actual.clear()
        lista_pedido.delete(0, tk.END)
        actualizar_total(pedido_actual, label_total)
        ventana_facturacion.destroy()

    def cancelar():
        ventana_facturacion.destroy()

    tk.Button(
        frame_botones,
        text="Confirmar Factura",
        font=letra_grande,
        bg=rojo,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=10,
        cursor="hand2",
        command=confirmar_factura
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Cancelar",
        font=letra_grande,
        bg=cafe_medio,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=10,
        cursor="hand2",
        command=cancelar
    ).pack(side="left", padx=5)

#===========================================================
# Mostrar Historial
#===========================================================

def mostrar_historial(ventana_padre):
    ventana_historial=tk.Toplevel(ventana_padre)
    ventana_historial.title("Historial de Facturas")
    ventana_historial.geometry("500x600")
    ventana_historial.config(bg=crema)

    tk.Label(
        ventana_historial,
        text="Historial de facturas",
        font=titulo,
        bg=crema,
        fg=rojo
    ).pack(pady=(15, 10))

    frame_busqueda=tk.Frame(ventana_historial, bg=crema)
    frame_busqueda.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(
        frame_busqueda,
        text="Ingrese numero de factura o cliente",
        bg=crema,
        anchor="w",
        font=letra_normal
    ).pack(fill="x")

    busqueda_var=tk.StringVar()
    tk.Entry(
        frame_busqueda,
        textvariable=busqueda_var,
        width=35,
        font=letra_normal,
        relief="solid",
        bd=1
    ).pack(pady=(5, 5))

    frame_botones_historial=tk.Frame(frame_busqueda, bg=crema)
    frame_botones_historial.pack(pady=5)

    lista_resultados=tk.Listbox(ventana_historial, width=60, height=15, font=letra_normal)
    lista_resultados.pack(padx=20, pady=(5, 10), fill="both", expand=True)

    label_info=tk.Label(ventana_historial, text="", bg=crema, fg=cafe_medio, font=letra_normal)
    label_info.pack()

    def mostrar_en_lista(facturas):
        lista_resultados.delete(0, tk.END)
        if not facturas:
            label_info.config(text="No se encuentra factura")
            return
        label_info.config(text=f"{len(facturas)} factura(s) encontrada(s)")
        for factura in facturas:
            lista_resultados.insert(
                tk.END,
                f"N°{factura['numero']} | {factura['fecha']} | "
                f"{factura['cliente']['nombre']} ({factura['cliente']['cedula']}) | "
                f"Total: ${factura['total']:.2f}"
            )

    def ver_todas():
        facturas=cargar_facturas()
        mostrar_en_lista(facturas)

    def buscar():
        texto_busqueda=busqueda_var.get().strip()

        if texto_busqueda == "":
            label_info.config(text="Ingrese la cedula o nombre del cliente para buscar:")
            return

        facturas=cargar_facturas()
        
        if texto_busqueda.isdigit():
            numero_buscado=int(texto_busqueda)
            resultados=[f for f in facturas if f["numero"] == numero_buscado]
        else:
            texto_minusculas=texto_busqueda.lower()
            resultados=[
                f for f in facturas
                if texto_minusculas in f['cliente']["nombre"].lower()
                or texto_minusculas in f['cliente']["cedula"].lower()
            ]

        mostrar_en_lista(resultados)

    def ver_detalle(event):
        seleccion=lista_resultados.curselection()
        if not seleccion:
            return

        texto_seleccionado=lista_resultados.get(seleccion[0])
        numero_texto=texto_seleccionado.split("|")[0].replace("N°", "").strip()

        try:
            numero_buscado=int(numero_texto)
        except ValueError:
            return

        facturas=cargar_facturas()
        factura=next((f for f in facturas if f["numero"] == numero_buscado), None)

        if factura is None:
            return

        ventana_detalle=tk.Toplevel(ventana_historial)
        ventana_detalle.title(f"Factura N° {factura['numero']}")
        ventana_detalle.geometry("360x560")
        ventana_detalle.config(bg=crema)

        tk.Label(
            ventana_detalle,
            text=f"Factura N°{factura['numero']}",
            font=titulo,
            bg=crema,
            fg=rojo
        ).pack(pady=(15, 5))

        cliente=factura["cliente"]
        tk.Label(ventana_detalle, text=f"Nombre: {cliente.get('nombre', '')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"Cedula: {cliente.get('cedula', '')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"Telefono: {cliente.get('telefono', '-')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"Direccion: {cliente.get('direccion', '-')}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"Correo: {cliente.get('correo', '')}", bg=crema, font=letra_normal).pack(pady=(0, 10))

        lista_detalle_factura=tk.Listbox(ventana_detalle, width=40, height=8, font=letra_normal)
        lista_detalle_factura.pack(padx=15, pady=(0, 10), fill="both", expand=True)
        
        for producto in factura["detalle"]:
            lista_detalle_factura.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f}")

        tk.Label(ventana_detalle, text=f"Subtotal: ${factura['subtotal']:.2f}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"IVA: ${factura['iva']:.2f}", bg=crema, font=letra_normal).pack()
        tk.Label(ventana_detalle, text=f"Domicilio: ${factura.get('domicilio', 0):.2f}", bg=crema, font=letra_normal).pack()

        tk.Label(
            ventana_detalle,
            text=f"Total: ${factura['total']:.2f}",
            font=subtitulo,
            bg=crema,
            fg=rojo
        ).pack(pady=(5, 15))

    lista_resultados.bind("<Double-1>", ver_detalle)

    tk.Label(
        ventana_historial,
        text="Presione doble click para visualizar completa la factura",
        bg=crema,
        fg=cafe_medio,
        font=letra_pequena
    ).pack(pady=(0, 5))

    tk.Button(
        frame_botones_historial,
        text="Buscar",
        font=letra_grande,
        bg=rojo,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=8,
        cursor="hand2",
        command=buscar
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones_historial,
        text="Ver todas",
        font=letra_de_botones,
        bg=cafe_medio,
        fg=texto_claro,
        relief="raised",
        bd=2,
        padx=20,
        pady=8,
        cursor="hand2",
        command=ver_todas
    ).pack(side="left", padx=5)

    ver_todas()