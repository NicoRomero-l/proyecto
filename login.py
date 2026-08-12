import tkinter as tk
from tkinter import messagebox
from herramientas import (cargar_usuarios, login_usuario, guardar_recordar, cargar_recordar, borrar_recordar)
from colores import *
from imagenes import (cargar_logos, cargar_icono_usuario, cargar_icono_contrasena, cargar_icono_login)

def boton_estilo(parent, texto_boton, comando, color_fondo=rojo, icono=None):
    pulsador = tk.Button(
        parent,
        text=texto_boton,
        command=comando,
        font=letra_de_botones,
        bg=color_fondo,
        fg=texto_claro,
        relief="raised",
        bd=3,
        padx=30,
        pady=12,
        cursor="hand2"
    )
    
    if icono:
        pulsador.config(image=icono, compound="left")
        parent.image = icono
    
    pulsador.bind("<Enter>", lambda evento: pulsador.config(bg=rojo_fuerte_claro if color_fondo == rojo else cafe_claro))
    pulsador.bind("<Leave>", lambda evento: pulsador.config(bg=color_fondo))
    
    return pulsador

def abrir_login():
    escenario_autenticacion = tk.Tk()
    escenario_autenticacion.title("Romereus Pizzeria - Login")
    escenario_autenticacion.geometry("440x540")
    escenario_autenticacion.config(bg=crema)
    
    bloque_emblema = tk.Frame(escenario_autenticacion, bg=crema)
    bloque_emblema.pack(pady=(30, 10))
    
    recurso_grafico_logo = cargar_logos((200, 70))
    
    if recurso_grafico_logo:
        rotulo_logo = tk.Label(bloque_emblema, image=recurso_grafico_logo, bg=crema)
        rotulo_logo.pack()
        rotulo_logo.image = recurso_grafico_logo
    else:
        tk.Label(
            bloque_emblema,
            text="ROMERAUS",
            font=("Georgia", 34, "bold"),
            bg=crema,
            fg=rojo
        ).pack()
        
        tk.Frame(bloque_emblema, bg=rojo, height=2, width=180).pack(pady=(3, 3))
        
        tk.Label(
            bloque_emblema,
            text="Pizzeria & Restaurante",
            font=("Georgia", 12, "italic"),
            bg=crema,
            fg=cafe_oscuro
        ).pack()
    
    tarjeta_credenciales = tk.Frame(
        escenario_autenticacion,
        bg=crema_oscuro,
        relief="raised",
        bd=3,
        highlightbackground=cafe_claro,
        highlightthickness=2,
        padx=35,
        pady=25
    )
    tarjeta_credenciales.pack(padx=35, pady=(10, 25), fill="both", expand=True)
    
    banco_identidades = cargar_usuarios()
    cadena_usuario_var = tk.StringVar()
    cadena_clave_var = tk.StringVar()
    bandera_recordar_var = tk.BooleanVar()
    
    icono_user = cargar_icono_usuario()
    icono_pass = cargar_icono_contrasena()

    def _construir_campo_formulario(padre_contenedor, etiqueta_rotulo, variable_almacen, recurso_icono, es_clave=False):
        bloque_fila = tk.Frame(padre_contenedor, bg=crema_oscuro)
        bloque_fila.pack(fill="x", pady=(0, 3))
        
        if recurso_icono:
            tk.Label(bloque_fila, image=recurso_icono, bg=crema_oscuro).pack(side="left", padx=(0, 5))
            bloque_fila.image = recurso_icono
        
        tk.Label(bloque_fila, text=etiqueta_rotulo, bg=crema_oscuro, fg=texto, font=letra_normal, anchor="w").pack(side="left")
        
        campo_entrada = tk.Entry(
            padre_contenedor,
            textvariable=variable_almacen,
            font=letra_normal,
            bg=crema,
            relief="solid",
            bd=2,
            show="*" if es_clave else ""
        )
        campo_entrada.pack(fill="x", pady=(0, 15))

    _construir_campo_formulario(tarjeta_credenciales, "Usuario", cadena_usuario_var, icono_user)
    _construir_campo_formulario(tarjeta_credenciales, "Contraseña", cadena_clave_var, icono_pass, es_clave=True)
    
    tk.Checkbutton(
        tarjeta_credenciales,
        text="Recordarme",
        variable=bandera_recordar_var,
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        selectcolor=crema,
        activebackground=crema_oscuro
    ).pack(anchor="w", pady=(0, 15))
    
    etiqueta_notificaciones = tk.Label(tarjeta_credenciales, text="", fg=rojo, bg=crema_oscuro, font=letra_normal)
    etiqueta_notificaciones.pack()
    
    def ejecutar_validar_ingreso():
        usuario_ingresado = cadena_usuario_var.get().strip()
        clave_ingresada = cadena_clave_var.get().strip()
        
        if usuario_ingresado == "" or clave_ingresada == "":
            etiqueta_notificaciones.config(text="Complete todos los campos")
            return
        
        if login_usuario(usuario_ingresado, clave_ingresada, banco_identidades):
            if bandera_recordar_var.get():
                guardar_recordar(usuario_ingresado, clave_ingresada)
            else:
                borrar_recordar()
            
            messagebox.showinfo("Bienvenido", f"Hola {usuario_ingresado}")
            escenario_autenticacion.destroy()
            from menu_pedidos import abrir_menu
            abrir_menu(usuario_ingresado)
        else:
            etiqueta_notificaciones.config(text="Usuario o contrasena incorrectos")
    
    panel_botones_accion = tk.Frame(tarjeta_credenciales, bg=crema_oscuro)
    panel_botones_accion.pack(pady=(15, 0))
    
    icono_login = cargar_icono_login()
    btn_login = boton_estilo(panel_botones_accion, " Ingresar", ejecutar_validar_ingreso, rojo, icono_login)
    btn_login.pack(side="left", padx=5)
    
    credenciales_persistidas = cargar_recordar()
    if credenciales_persistidas:
        cadena_usuario_var.set(credenciales_persistidas.get("usuario", ""))
        cadena_clave_var.set(credenciales_persistidas.get("contrasena", ""))
        bandera_recordar_var.set(True)
    
    escenario_autenticacion.bind("<Return>", lambda evento: ejecutar_validar_ingreso())
    escenario_autenticacion.mainloop()

if __name__ == "__main__":
    abrir_login()