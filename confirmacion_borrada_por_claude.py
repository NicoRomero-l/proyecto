## esta funcion estaba repititiva y obsoleta, incompleta y no dejaba que se ejecute la ventana para tomar los pedidos de los clientes 



#===========================================================
# Funcion para confirmar el pedido
#===========================================================
def mostrar_facturacion(pedido_actual, ventana_padre, lista_pedidos, label_total, total):
    ventana_facturacion=tk.Toplevel(ventana_padre)
    ventana_facturacion.title("Facturación")
    ventana_facturacion.geometry("400x400")
    ventana_facturacion.config(bg="#ffffff")

    tk.Label(
        ventana_facturacion,
        text="Datos del Cleinte",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff"
    ).pack(pady=(15, 10))

    frame_datos = tk.Frame(ventana_facturacion, bg="#ffffff")
    frame_datos.pack(padx=20, pady=(0, 10), fill="x")

    lista_detalle = tk.Listbox(ventana_facturacion, width=40, height=12)
    lista_detalle.pack(padx=15, pady=10, fill="both", expand=True)

    for producto in pedido_actual:
        lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")

    total= sum(p["precio"] for p in pedido_actual)
    tk.Label(
        ventana_facturacion,
        text=f"Total: ${total}",
        font=("Segoe UI", 13, "bold"),
        bg="#ffffff"
    ).pack(pady=(0, 15))

    frame_botones=tk.Frame(ventana_facturacion, bg="#ffffff")
    frame_botones.pack(pady=(0, 15))

    def ir_a_facturacion():
        ventana_facturacion.destroy()
        mostrar_facturacion(pedido_actual, ventana_padre, lista_pedidos, label_total, total)

    def seguir_editando():
        ventana_facturacion.destroy()

    tk.Button(
        frame_botones,
        text="Confirmar Pedido",
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        fg="white",
        width= 15,
        command=ir_a_facturacion
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Seguir Editando",
        font=("Segoe UI", 10, "bold"),
        bg="#edf2f7",
        fg="white",
        width= 15,
        command=seguir_editando
    ).pack(side="left", padx=5)

