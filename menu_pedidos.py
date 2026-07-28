##ventana de recoleccion de pedidos 

import json
import os
import tkinter as tk
from tkinter import messagebox

ARCHIVO_MENU="menu.json"

def cargar_menu():
    if not os.path.exists(ARCHIVO_MENU):
        return []
    try:
        with open(ARCHIVO_MENU, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return[]

menu_productos=cargar_menu()
categorias=[]
for producto in menu_productos:
    if producto["categoria"] not in categorias:
        categorias.append(producto["categoria"])

pedido_actual=[]

menu=tk.Tk()
menu.title("Menú-Pizzeria")
menu.geometry("900x500")
menu.config(bg="#f4f6f8")

Frame_categorias = tk.Frame(menu, bg="#2b2d42")
Frame_categorias.pack(side="top", fill="x")

frame_productos=tk.Frame(menu,
                         bg="#f4f6f8",
                         padx=15,
                         pady=15
                         )
frame_productos.pack(side="left", fill="both", expand=True)

frame_pedido=tk.Frame(menu,
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

lista_pedido=tk.Listbox(frame_pedido, width=30, height=18)
lista_pedido.pack(fill="both", expand=True)

label_total=tk.Label(
    frame_pedido,
    text="Total: $0.00",
    font=("Segoe UI", 12, "bold"),
    bg="#ffffff"
)
label_total.pack(pady=(10, 10))

def agregar_producto(producto):
    pedido_actual.append(producto)
    lista_pedido.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")
    actualizar_total()

def actualizar_total():
    total=sum(p["precio"] for p in pedido_actual)
    label_total.config(text=f"Total: ${total}")

def mostrar_categoria(categoria):
    for widget in frame_productos.winfo_children():
        widget.destroy()

    tk.Label(
        frame_productos,
        text=categoria,
        font=("Segoe UI", 15, "bold"),
        bg="#f4f6f8"
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    productos_filtrados=[
        p for p in menu_productos if p["categoria"] == categoria
    ]

    fila=1
    columna=0

    for producto in productos_filtrados:
        boton=tk.Button(
            frame_productos,
            text=f"{producto['nombre']} - ${producto['precio']}",
            width=18,
            height=3,
            bg="#edf2f7",
            command=lambda p=producto:agregar_producto(p)
        )
        boton.grid(row=fila, column=columna, padx=8, pady=8)
        columna +=1
        if columna > 2:
            columna =0
            fila +=1

for categoria in categorias:
    boton_categoria=tk.Button(
        Frame_categorias,
        text=categoria,
        font=("Segoe UI", 10, "bold"),
        bg="#2b2d42",
        relief="flat",
        padx=15,
        pady=10,
        command=lambda c=categoria: mostrar_categoria(c)
    )
    boton_categoria.pack(side="left")

def confirmar_pedido():
    if not pedido_actual:
        messagebox.showwarning("Pedido vacio", "Agrega un producto o pedido")
        return

    print("Pedido a confirmar:", pedido_actual)
    messagebox.showinfo("Pedido", "Aqui se abre la ventana de confirmacion")

boton_confirmar=tk.Button(
    frame_pedido,
    text="Confirmar Pedido",
    font=("Segoe UI", 11, "bold"),
    bg="#2b2d42",
    fg="white",
    command=confirmar_pedido
)
boton_confirmar.pack(fill="x", side="bottom")

if categorias:
    mostrar_categoria(categorias[0])

menu.mainloop()
