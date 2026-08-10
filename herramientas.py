## ventana de herramientas, aunque no es una ventana :b
## simplemente es de donde va a sacar las funciones todo mi programa

import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

#===========================================================
# Variables del Login
#===========================================================
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_RECORDAR = "recordar.json"

#===========================================================
# Variable del Menú
#===========================================================
ARCHIVO_MENU = "menu.json"

#===========================================================
# Variable de las Facturas
#===========================================================
ARCHIVO_FACTURAS = "facturacion.json"
IVA_PORCENTAJE=0.15

#===========================================================
# Variable del domicilio "Función Afín(tema matemático)"
#===========================================================
ARCHIVO_DOMICILIO = "domicilio.json"

#===========================================================
# Funciones del Login
#===========================================================
def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def login_usuario(usuario, contraseña, usuarios):
    contraseña_guardada = usuarios.get(usuario)
    return contraseña_guardada is not None and contraseña_guardada == contraseña

def guardar_recordar(usuario, contraseña):
    datos = {"usuario": usuario, "contraseña": contraseña}
    with open(ARCHIVO_RECORDAR, "w", encoding="utf-8") as f:
        json.dump(datos, f)

def cargar_recordar():
    if not os.path.exists(ARCHIVO_RECORDAR):
        return None
    try:
        with open(ARCHIVO_RECORDAR, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def borrar_recordar():
    if os.path.exists(ARCHIVO_RECORDAR):
        os.remove(ARCHIVO_RECORDAR)

#===========================================================
# Funciones del Menú
#===========================================================
def cargar_menu():
    if not os.path.exists(ARCHIVO_MENU):
        return []
    try:
        with open(ARCHIVO_MENU, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def actualizar_total(pedido_actual, label_total):
    total = sum(p["precio"] for p in pedido_actual)
    label_total.config(text=f"Total: ${total:.2f}")

def agregar_producto(producto, pedido_actual, lista_pedido, label_total):
    if "tamaños" in producto:
        mostrar_seleccion_tamaño(producto, pedido_actual, lista_pedido, label_total)
        return

    pedido_actual.append(producto)
    lista_pedido.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")
    actualizar_total(pedido_actual, label_total)

def eliminar_producto(pedido_actual, lista_pedido, label_total):
    seleccion=lista_pedido.curselection()
    if not seleccion:
        messagebox.showinfo("Nada seleccionado", "Seleccione algo en la lista para eliminarlo")
        return

    indice=seleccion[0]
    pedido_actual.pop(indice)
    lista_pedido.delete(indice)
    actualizar_total(pedido_actual, label_total)

def mostrar_categoria(categoria, frame_productos, menu_productos, pedido_actual, lista_pedido, label_total):
    for widget in frame_productos.winfo_children():
        widget.destroy()

    tk.Label(
        frame_productos,
        text=categoria,
        font=("Segoe UI", 15, "bold"),
        bg="#f4f6f8"
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    productos_filtrados = [
        p for p in menu_productos if p["categoria"] == categoria
    ]

    fila = 1
    columna = 0

    for producto in productos_filtrados:
        if "tamaños" in producto:
            texto_boton=f"{producto['nombre']} (elije tamaño)"
        else:
            texto_boton=f"{producto['nombre']} - ${producto['precio']}"
        
        boton = tk.Button(
            frame_productos,
            text=texto_boton,
            width=18,
            height=3,
            bg="#edf2f7",
            command=lambda p=producto: agregar_producto(p, pedido_actual, lista_pedido, label_total)
        )
        boton.grid(row=fila, column=columna, padx=8, pady=8)

        columna += 1
        if columna > 2:
            columna = 0
            fila += 1

#===========================================================
# Funcion para elejir el tamaño de la pizza
#===========================================================

def mostrar_seleccion_tamaño(producto, pedido_actual, lista_pedido, label_total):
    ventana_tamaño=tk.Toplevel()
    ventana_tamaño.title(f"Elije el tamaño - {producto['nombre']}")
    ventana_tamaño.geometry("300x350")
    ventana_tamaño.config(bg="#ffffff")

    tk.Label(
        ventana_tamaño,
        text=producto['nombre'],
        font=("Segoe UI", 13, "bold"),
        bg="#ffffff"
    ).pack(pady=(15, 10))

    def elejir(tamaño, precio):
        producto_con_tamaño={
            "categoria":producto["categoria"],
            "nombre":f"{producto['nombre']} ({tamaño})",
            "precio":precio
        }
        pedido_actual.append(producto_con_tamaño)
        lista_pedido.insert(tk.END, f"{producto_con_tamaño['nombre']} - ${producto_con_tamaño['precio']}")
        actualizar_total(pedido_actual, label_total)
        ventana_tamaño.destroy()

    for tamaño, precio in producto["tamaños"].items():
        tk.Button(
            ventana_tamaño,
            text=f"{tamaño} - ${precio}",
            width=20,
            height=2,
            bg="#edf2f7",
            command=lambda t=tamaño, pr=precio: elejir(t, pr)
        ).pack(pady=5)

#===========================================================
# Funciones de facturas
#===========================================================
def cargar_facturas():
    if not os.path.exists(ARCHIVO_FACTURAS):
        return []
    try:
        with(open(ARCHIVO_FACTURAS, "r", encoding="utf-8")) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return[]

def guardar_factura(factura):
    facturas = cargar_facturas()
    facturas.append(factura)
    with open(ARCHIVO_FACTURAS, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)

def generar_numero_factura():
    facturas=cargar_facturas()
    return len(facturas) + 1

#===========================================================
# Funcion para calcular envios a domicilio (función afín)
#===========================================================

def cargar_domicilio():
    if not os.path.exists(ARCHIVO_DOMICILIO):
        return {"tarifa_fija": 1.00, "tarifa_km": 0.50}
    try:
        with open(ARCHIVO_DOMICILIO, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"tarifa_fija": 1.00, "tarifa_km": 0.50}

def calcular_costo_domicilio(km, tarifa_fija, tarifa_km):
    costo=(tarifa_km*km)+tarifa_fija
    return costo

def generar_tabla_de_domicilios(tarifa_fija, tarifa_km, km_maximo=5):
    tabla=[]
    for km in range(1, km_maximo +1):
        costo=calcular_costo_domicilio(km, tarifa_fija, tarifa_km)
        tabla.append((km, costo))
    return tabla

#===========================================================
# Funcion para confirmar el pedido
#===========================================================

def confirmar_pedido(pedido_actual, ventana_padre, lista_pedido, label_total):
    if not pedido_actual:
        messagebox.showwarning("Pedido vacio", "Agrega un producto o pedido")
        return

    ventana_confirmar = tk.Toplevel(ventana_padre)
    ventana_confirmar.title("Confirmar Pedido")
    ventana_confirmar.geometry("380x450")
    ventana_confirmar.config(bg="#ffffff")

    tk.Label(
        ventana_confirmar,
        text="Detalle del pedido",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
    ).pack(pady=(15, 10))

    lista_detalle = tk.Listbox(ventana_confirmar, width=40, height=15)
    lista_detalle.pack(padx=15, pady=10, fill="both", expand=True)

    for producto in pedido_actual:
        lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")

    total = sum(p["precio"] for p in pedido_actual)
    tk.Label(
        ventana_confirmar,
        text=f"Total: ${total:.2f}",
        font=("Segoe UI", 13, "bold"),
        bg="#ffffff"
    ).pack(pady=(0, 15))

    frame_botones = tk.Frame(ventana_confirmar, bg="#ffffff")
    frame_botones.pack(pady=(0, 15))

    def ir_a_facturacion():
        ventana_confirmar.destroy()
        mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, total)

    def seguir_editando():
        ventana_confirmar.destroy()

    tk.Button(
        frame_botones,
        text="Confirmar Pedido",
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        fg="white",
        width=15,
        command=ir_a_facturacion
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Seguir editando",
        font=("Segoe UI", 10, "bold"),
        bg="#edf2f7",
        width=15,
        command=seguir_editando
    ).pack(side="left", padx=5)

#===========================================================
# Funcion para mostrar la ventana de facturacion
#===========================================================

def mostrar_facturacion(pedido_actual, ventana_padre, lista_pedido, label_total, subtotal):
    ventana_facturacion=tk.Toplevel(ventana_padre)
    ventana_facturacion.title("Facturacion")
    ventana_facturacion.geometry("440x780")
    ventana_facturacion.config(bg="#ffffff")

    iva=subtotal*IVA_PORCENTAJE
    costo_domicilio=0.0

    tk.Label(
        ventana_facturacion,
        text="DATOS DEL CLIENTE",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff"
    ).pack(pady=(15, 10))

    frame_datos=tk.Frame(ventana_facturacion, bg="#ffffff")
    frame_datos.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(frame_datos, text="Nombres completos:", bg="#ffffff", anchor="w").pack(fill="x")
    nombre_var = tk.StringVar()
    tk.Entry(frame_datos, textvariable=nombre_var, width=35).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Cédula:", bg="#ffffff", anchor="w").pack(fill="x")
    cedula_var = tk.StringVar()
    tk.Entry(frame_datos, textvariable=cedula_var, width=35).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Teléfono:", bg="#ffffff", anchor="w").pack(fill="x")
    telefono_var = tk.StringVar()
    tk.Entry(frame_datos, textvariable=telefono_var, width=35).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Dirección:", bg="#ffffff", anchor="w").pack(fill="x")
    direccion_var = tk.StringVar()
    tk.Entry(frame_datos, textvariable=direccion_var, width=35).pack(pady=(0, 8))

    tk.Label(frame_datos, text="Correo Electrónico:", bg="#ffffff", anchor="w").pack(fill="x")
    correo_var = tk.StringVar()
    tk.Entry(frame_datos, textvariable=correo_var, width=35).pack(pady=(0, 8))

    label_estado=tk.Label(frame_datos,
                           text="",
                           fg="red",
                           bg="#ffffff"
                           )
    label_estado.pack()

    #Aqui va el detalle del pedido, como se va a impirmir 
    tk.Label(
        ventana_facturacion,
        text="Detalle de facturación",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff"
    ).pack(pady=(10, 5))

    lista_detalle=tk.Listbox(ventana_facturacion, width=45, height=6)
    lista_detalle.pack(padx=20, pady=(0, 10), fill="both", expand=True)

    for producto in pedido_actual:
        lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")

#===========================================================
# Funcion para mostrar la ventana de domicilio 
## modulo matematico "(Función Afín: f(x) = m·x + b)"
#===========================================================
    tk.Label(
        ventana_facturacion,
        text="Servicio a domicilio",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
    ).pack(pady=(10 ,5))

    domicilio_var=tk.BooleanVar()
    frame_domicilio=tk.Frame(ventana_facturacion, bg="#ffffff")

    datos_domicio=cargar_domicilio()
    tarifa_fija=datos_domicio["tarifa_fija"]
    tarifa_km=datos_domicio["tarifa_km"]

    tk.Label(
        frame_domicilio,
        text=f"Tarifa/km: ${tarifa_km} - Tarifa fija: ${tarifa_fija}",
        bg="#ffffff",
        fg="#555555",
        font=("Segoe UI", 8)
        ).pack(pady=(2, 6))

    tk.Label(
        frame_domicilio,
        text="Distancia(km): ",
        bg="#ffffff",
        anchor="w"
    ).pack(fill="x")

    km_var=tk.StringVar()

    tk.Entry(
        frame_domicilio,
        textvariable=km_var,
        width=15
    ).pack(pady=(0, 5))

    label_costo_domicilio=tk.Label(frame_domicilio, text="Costo de envio: $0.00 ", bg="#ffffff")
    label_costo_domicilio.pack()

    lista_tabla=tk.Listbox(frame_domicilio, width=30, height=5)

    def calcular_envio():
        nonlocal costo_domicilio
        km_texto=km_var.get().strip()

        if km_texto=="":
            label_estado.config(text="Ingresa la distancia en km")
            return
        try:
            km=float(km_texto)
        except ValueError:
            label_estado.config(text="La distancia debe ser un número")
            return
        if km<0:
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
            lista_tabla.insert(tk.END, f"f({km}) = {tarifa_km:.2f}({km}) + {tarifa_fija:.2f} = ${costo:.2f}")
        lista_tabla.pack(pady=(5, 5))

    tk.Button(frame_domicilio, text="Calcular envío", bg="#edf2f7", command=calcular_envio).pack(pady=(0, 5))
    tk.Button(frame_domicilio, text="Ver tabla (1-5 km)", bg="#edf2f7", command=ver_tabla).pack(pady=(0, 5))

    def toggle_domicilio():
        if domicilio_var.get():
            frame_domicilio.pack(padx=20, pady=(0, 10), fill="x")
        else:
            nonlocal costo_domicilio
            costo_domicilio=0.0
            km_var.set("")
            label_costo_domicilio.config(text="Costo de envio: $0.00")
            lista_tabla.delete(0, tk.END)
            frame_domicilio.pack_forget()
            actualizar_total_visual()

    tk.Checkbutton(
        ventana_facturacion,
        text="¿Es domicilio?",
        variable=domicilio_var,
        bg="#ffffff",
        command=toggle_domicilio
    ).pack()

#=======================================================
# Totales
#=======================================================

    tk.Label(ventana_facturacion, text=f"subtotal: ${subtotal:.2f}", bg="#ffffff").pack(pady=(10, 0))
    tk.Label(ventana_facturacion, text=f"Iva (15%): ${iva:.2f}", bg="#ffffff").pack()

    label_total_final=tk.Label(
        ventana_facturacion,
        text=f"Total: ${subtotal + iva:.2f}",
        font=("Segoe UI", 13, "bold"),
        bg="#ffffff"
    )
    label_total_final.pack(pady=(5, 10))

    def actualizar_total_visual():
        total_actual=subtotal+iva+costo_domicilio
        label_total_final.config(text=f"Total: ${total_actual:.2f}")

    frame_botones=tk.Frame(ventana_facturacion, bg="#ffffff")
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
        total_final=subtotal+iva+costo_domicilio

        factura={
            "numero":numero,
            "fecha":datetime.now().strftime("%d-%m-%Y %H:%M"),
            "cliente":{
                "nombre":nombre,
                "cedula":cedula,
                "telefono":telefono,
                "direccion":direccion,
                "correo":correo
            },
            "detalle":pedido_actual.copy(),
            "subtotal":subtotal,
            "iva":iva,
            "domicilio":costo_domicilio,
            "total":total_final
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
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        fg="white",
        width=15,
        command=confirmar_factura
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Cancelar",
        font=("Segoe UI", 10, "bold"),
        bg="#edf2f7",
        width=15,
        command=cancelar
    ).pack(side="left", padx=5)

#=======================================================
# Mostral Historial
#=======================================================

def mostrar_historial(ventana_padre):
    ventana_hisotrial=tk.Toplevel(ventana_padre)
    ventana_hisotrial.title("Historial de Facturas")
    ventana_hisotrial.geometry("480x550")
    ventana_hisotrial.config(bg="#ffffff")

    tk.Label(
        ventana_hisotrial,
        text="Historial de facturas",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff"
    ).pack(pady=(15, 10))

    frame_busqueda=tk.Frame(ventana_hisotrial, bg="#ffffff")
    frame_busqueda.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(
        frame_busqueda,
        text="Ingrese numero de factura o cliente",
        bg="#ffffff",
        anchor="w"
    ).pack(fill="x")

    busqueda_var=tk.StringVar()
    tk.Entry(
        frame_busqueda,
        textvariable=busqueda_var,
        width=35
    ).pack(pady=(5, 5))

    lista_resultados=tk.Listbox(ventana_hisotrial, width=60, height=15)
    lista_resultados.pack(padx=20, pady=(5, 10), fill="both", expand=True)

    label_info=tk.Label(ventana_hisotrial, text="", bg="#ffffff", fg="#555555")
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
        texto=busqueda_var.get().strip()

        if texto == "":
            label_info.config(text="Ingrese la cédula o nombre del cliente para buscar:")
            return

        facturas=cargar_facturas()
        
        if texto.isdigit():
            numero_buscado=int(texto)
            resultados=[f for f in facturas if f["numero"] == numero_buscado]
        else:
            texto_minusculas=texto.lower()
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
        numero_texto=texto_seleccionado.split("|")[0].replace("N°","").strip()

        try:
            numero_buscado=int(numero_texto)
        except ValueError:
            return

        facturas=cargar_facturas()
        factura=next((f for f in facturas if f["numero"] == numero_buscado), None)

        if factura is None:
            return

        ventana_detalle=tk.Toplevel(ventana_hisotrial)
        ventana_detalle.title(f"Factura N° {factura['numero']}")
        ventana_detalle.geometry("360x560")
        ventana_detalle.config(bg="#ffffff")

        tk.Label(
            ventana_detalle,
            text=f"Factura N°{factura['numero']}",
            font=("Segoe UI", 15, "bold"),
            bg="#ffffff"
        ).pack(pady=(15, 5))

        cliente=factura["cliente"]
        tk.Label(ventana_detalle, text=f"Nombre: {cliente.get('nombre', '')}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"Cédula: {cliente.get('cedula', '')}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"Teléfono: {cliente.get('telefono', '-')}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"Dirección: {cliente.get('direccion', '-')}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"Correo: {cliente.get('correo', '')}", bg="#ffffff").pack(pady=(0, 10))

        lista_detalle_factura=tk.Listbox(ventana_detalle, width=40, height=8)
        lista_detalle_factura.pack(padx=15, pady=(0 ,10), fill="both", expand=True)
        
        for producto in factura["detalle"]:
            lista_detalle_factura.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")

        tk.Label(ventana_detalle, text=f"Subtotal: ${factura['subtotal']:.2f}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"IVA: ${factura['iva']:.2f}", bg="#ffffff").pack()
        tk.Label(ventana_detalle, text=f"Domicilio: ${factura.get('domicilio', 0):.2f}", bg="#ffffff").pack()

        tk.Label(
            ventana_detalle,
            text=f"Total: ${factura['total']:.2f}",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=(5, 15))

    lista_resultados.bind("<Double-1>", ver_detalle)

    tk.Label(
        ventana_hisotrial,
        text="Presione doble click para visualizar completa la factura",
        bg="#ffffff",
        fg="#888888",
        font=("Segoe UI", 8)
    ).pack(pady=(0, 5))

    frame_botones_historial=tk.Frame(ventana_hisotrial, bg="#ffffff")
    frame_botones_historial.pack(pady=(5, 15))

    tk.Button(
        frame_botones_historial,
        text="Buscar",
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        fg="white",
        width=15,
        command=buscar
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones_historial,
        text="Ver todas",
        font=("Segoe UI", 10, "bold"),
        bg="#edf2f7",
        width=15,
        command=ver_todas
    ).pack(side="left", padx=5)

    ver_todas()