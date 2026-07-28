##ventana de login 

import json
import os
import tkinter as tk
from tkinter import messagebox

ARCHIVO_USUARIOS= "usuarios.json"
ARCHIVO_RECORDAR= "recordar.json"

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def login_usuario(usuario, contraseña, usuarios):
    contraseña_guardar=usuarios.get(usuario)
    return contraseña_guardar is not None and contraseña_guardar == contraseña

def guardar_recordar(usuario, contraseña):
    datos={"usuario": usuario, "contraseña": contraseña}
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

login=tk.Tk()
login.title("INICIAR SESION")
login.geometry("500x500")
login.config(bg="#f4f6f8")

usuarios=cargar_usuarios()

usuario_var=tk.StringVar()
contraseña_var=tk.StringVar()
recordarme_var=tk.BooleanVar()

frame= tk.Frame(login, 
                bg="#f4f6f8",
                padx=20
                )
frame.pack(pady=10, fill="both", expand=True)

tk.Label(frame, text="Usuario", bg="#f4f6f8", anchor="w").pack(fill="x")

entrada_usuario=tk.Entry(frame, textvariable=usuario_var, width=30)
entrada_usuario.pack(pady=(0, 10))

tk.Label(frame, 
         text="Contraseña", 
         bg="#f4f6f8", 
         anchor="w").pack(fill="x")

entrada_contraseña=tk.Entry(frame, 
                            textvariable=contraseña_var, 
                            width=30, 
                            show="*")
entrada_contraseña.pack(pady=(0, 10))

recordar_usuario=tk.Checkbutton(
    frame,
    text="Rercordarme",
    variable=recordarme_var,
    bg="#f4f6f8"
)
recordar_usuario.pack(anchor="w", pady=(0, 10))

label_estado=tk.Label(frame, 
                      text="",
                      fg="red",
                      bg="#f4f6f8"
                        )
label_estado.pack()

def entrar():
    usuario=usuario_var.get().strip()
    contraseña=contraseña_var.get().strip()

    if usuario == "" or contraseña == "":
        label_estado.config(text="Completa el usuario y la contraseña")
        return

    if login_usuario (usuario, contraseña, usuarios):
        if recordarme_var.get():
            guardar_recordar(usuario, contraseña)
        else:
            borrar_recordar()

        messagebox.showinfo("Bienvenido", f"Hola {usuario}")
        login.destroy()
    else:
        label_estado.config(text="Usuario o contarseña incorrectos.")

boton_login=tk.Button(frame, text="Iniciar Sesión",
                      command=entrar,
                      width=25
                      )
boton_login.pack(pady=(0, 10))

datos_guardados= cargar_recordar()

if datos_guardados:
    usuario_var.set(datos_guardados["usuario"])
    contraseña_var.set(datos_guardados["contraseña"])
    recordarme_var.set(True)

login.bind("<Return>", lambda event: entrar())

login.mainloop()
