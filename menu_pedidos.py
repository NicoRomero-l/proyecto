##ventana de recoleccion de pedidos 

from herramientas import (cargar_menu, mostrar_categoria, confirmar_pedido)
import tkinter as tk

menu_productos = cargar_menu()
categorias = []
for producto in menu_productos:
    if producto["categoria"] not in categorias:
        categorias.append(producto["categoria"])

pedido_actual = []

menu = tk.Tk()
menu.title("Menú-Pizzeria")
menu.geometry("1080x950")
menu.config(bg="#f4f6f8")

Frame_categorias = tk.Frame(menu, bg="#2b2d42")
Frame_categorias.pack(side="top", fill="x")

frame_productos = tk.Frame(menu,
                            bg="#f4f6f8",
                            padx=15,
                            pady=15
                            )
frame_productos.pack(side="left", fill="both", expand=True)

frame_pedido = tk.Frame(menu,
                         bg="#ffffff",
                         width=260,
                         padx=15,
                         pady=15
                         )
frame_pedido.pack(side="right", fill="y")
frame_pedido.pack_propagate(False)

tk.Label(
    frame_pedido,
    text="Pedido Actual",
    font=("Segoe UI", 13, "bold"),
    bg="#ffffff"
).pack(anchor="w", pady=(0, 10))

lista_pedido = tk.Listbox(frame_pedido, width=30, height=18)
lista_pedido.pack(fill="both", expand=True)

label_total = tk.Label(
    frame_pedido,
    text="Total: $0.00",
    font=("Segoe UI", 12, "bold"),
    bg="#ffffff"
)
label_total.pack(pady=(10, 10))

for categoria in categorias:
    boton_categoria = tk.Button(
        Frame_categorias,
        text=categoria,
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        relief="flat",
        padx=15,
        pady=10,
        command=lambda c=categoria: mostrar_categoria(
            c, frame_productos, menu_productos, pedido_actual, lista_pedido, label_total
        )
    )
    boton_categoria.pack(side="left")

boton_confirmar = tk.Button(
    frame_pedido,
    text="Confirmar Pedido",
    font=("Segoe UI", 11, "bold"),
    bg="#2b2d42",
    fg="white",
    command=lambda: confirmar_pedido(pedido_actual, menu, lista_pedido, label_total)
)
boton_confirmar.pack(fill="x", side="bottom")

if categorias:
    mostrar_categoria(categorias[0], frame_productos, menu_productos, pedido_actual, lista_pedido, label_total)

def cerrar_sesion(menu):
    menu.destroy()
    from login import abrir_login
    abrir_login()

tk.Button(
    frame_pedido,
    text="Cerrar Sesión",
    command=lambda: cerrar_sesion(menu)
).pack(side="bottom")

menu.mainloop()