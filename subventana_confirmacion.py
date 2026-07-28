## subventana de confirmacion 
## esto va dentro de la funcion confirmar_pedido 

import tkinter as tk
from tkinter import messagebox

ventana_confirmar= tk.Toplevel(menu)
ventana_confirmar.title("Confirmar Pedido")
ventana_confirmar.geometry("380x450")
ventana_confirmar.config(bg="#ffffff")

tk.Label(
    ventana_confirmar,
    text="Detalle del pedido",
    font=("Segoe UI", 14, "bold"),
    bg="#ffffff",
).pack(pady=(15, 10))

lista_detalle= tk.Listbox(ventana_confirmar, width=40, height=15)
lista_detalle.pack(padx=15, pady=10, fill="both", expand=True)

for producto in pedido_actual:
    lista_detalle.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")

total=sum(p["precio"] for p in pedido_actual)
tk.Label(
    ventana_confirmar,
    text=f"Total:{total}",
    font=("Segoe UI", 13, "bold"),
    bg="#ffffff"
).pack(pady=(0, 15))

frame_botones = tk.Frame(ventana_confirmar, bg="#ffffff")
frame_botones.pack(pady=(0, 15))

def confirmar_definitivo():
    messagebox.showinfo("Pedido confirmado", "Tu pedido fue confirmado con éxito")
    pedido_actual.clear()
    lista_pedido.delete(0, tk.END)
    actualizar_total()
    ventana_confirmar.destroy()

def seguir_editando():
    ventana_confirmar.destroy()

tk.Button(
    frame_botones,
    text="Confirmar Pedido",
    font=("Segoe UI", 10, "bold"),
    bg="#2b2d42",
    fg="white",
    width=15,
    command=confirmar_definitivo
).pack(side="left", padx=5)

tk.Button(
    frame_botones,
    text="Seguir editando",
    font=("Segoe UI", 10, "bold"),
    bg="#edf2f7",
    width=15,
    command=seguir_editando
).pack(side="left", padx=5)
