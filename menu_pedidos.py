##ventana de recoleccion de pedidos 

import tkinter as tk
from colores import *
from herramientas import (cargar_menu, mostrar_categoria, confirmar_pedido, eliminar_producto, mostrar_historial)

def abrir_menu(usuario_actual=None):
    menu_productos=cargar_menu()
    categorias=[]
    for producto in menu_productos:
        if producto["categoria"] not in categorias:
            categorias.append(producto["categoria"])

    pedido_actual=[]

    menu_ventana=tk.Tk()
    menu_ventana.title(f"Menú - Romereus Pizzeria ({usuario_actual if usuario_actual else 'Invitado'})")
    menu_ventana.geometry("1080x720")
    menu_ventana.config(bg=crema)

    frame_categorias=tk.Frame(menu_ventana, bg=cafe_oscuro_fondo)
    frame_categorias.pack(side="top", fill="x")

    frame_productos=tk.Frame(
        menu_ventana,
        bg=crema,
        padx=15,
        pady=15
    )
    frame_productos.pack(side="left", fill="both", expand=True)

    frame_pedido=tk.Frame(
        menu_ventana,
        bg=blanco_oscuro,
        width=280,
        padx=15,
        pady=15
    )
    frame_pedido.pack(side="right", fill="y")
    frame_pedido.pack_propagate(False)

    tk.Label(
        frame_pedido,
        text="Pedido Actual",
        font=subtitulo,
        bg=blanco_oscuro,
        fg=texto
    ).pack(anchor="w", pady=(0, 10))

    lista_pedido=tk.Listbox(frame_pedido, width=30, height=18, font=letra_normal)
    lista_pedido.pack(fill="both", expand=True)

    label_total=tk.Label(
        frame_pedido,
        text="Total: $0.00",
        font=letra_de_botones,
        bg=blanco_oscuro,
        fg=rojo
    )
    label_total.pack(pady=(10, 10))

    for categoria in categorias:
        boton_categoria=tk.Button(
            frame_categorias,
            text=categoria,
            font=letra_de_botones,
            bg=cafe_oscuro_fondo,
            fg=texto_claro,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda c=categoria: mostrar_categoria(
                c, frame_productos, menu_productos, pedido_actual, lista_pedido, label_total
            )
        )
        boton_categoria.pack(side="left")

    frame_acciones_pedido=tk.Frame(frame_pedido, bg=blanco_oscuro)
    frame_acciones_pedido.pack(fill="x", side="bottom", pady=(10, 0))

    def cerrar_sesion():
        menu_ventana.destroy()
        from login import abrir_login
        abrir_login()

    boton_confirmar=tk.Button(
        frame_acciones_pedido,
        text="Confirmar Pedido",
        font=letra_de_botones,
        bg=rojo,
        fg=texto_claro,
        relief="raised",
        bd=2,
        pady=8,
        cursor="hand2",
        command=lambda: confirmar_pedido(pedido_actual, menu_ventana, lista_pedido, label_total)
    )
    boton_confirmar.pack(fill="x", pady=(0, 5))

    boton_eliminar=tk.Button(
        frame_acciones_pedido,
        text="Eliminar Producto",
        font=letra_normal,
        bg=rojo_pizza,
        fg=texto_claro,
        relief="raised",
        bd=2,
        pady=5,
        cursor="hand2",
        command=lambda: eliminar_producto(pedido_actual, lista_pedido, label_total)
    )
    boton_eliminar.pack(fill="x", pady=(0, 5))

    boton_historial=tk.Button(
        frame_acciones_pedido,
        text="Historial Facturas",
        font=letra_normal,
        bg=cafe_medio,
        fg=texto_claro,
        relief="raised",
        bd=2,
        pady=5,
        cursor="hand2",
        command=lambda: mostrar_historial(menu_ventana)
    )
    boton_historial.pack(fill="x", pady=(0, 5))

    boton_logout=tk.Button(
        frame_acciones_pedido,
        text="Cerrar Sesión",
        font=letra_normal,
        bg=cafe_oscuro,
        fg=texto_claro,
        relief="raised",
        bd=2,
        pady=5,
        cursor="hand2",
        command=cerrar_sesion
    )
    boton_logout.pack(fill="x")

    if categorias:
        mostrar_categoria(categorias[0], frame_productos, menu_productos, pedido_actual, lista_pedido, label_total)

    menu_ventana.mainloop()

if __name__ == "__main__":
    abrir_menu()