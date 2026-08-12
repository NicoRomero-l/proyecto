<<<<<<< HEAD
=======
##ventana de login 

>>>>>>> cdfd3f53a63972ca271a950fab50f2b68c9e7cb4
import tkinter as tk
from tkinter import messagebox
from herramientas import (cargar_usuarios, login_usuario, guardar_recordar, cargar_recordar, borrar_recordar)
from colores import *
from imagenes import (cargar_logos, cargar_icono_usuario, cargar_icono_contrasena, cargar_icono_login)

def boton_estilo(parent, texto_boton, comando, color_fondo=rojo, icono=None):
    btn=tk.Button(
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
        btn.config(image=icono, compound="left")
        parent.image=icono
    
    def hover_on(e):
        btn.config(bg=rojo_fuerte_claro if color_fondo == rojo else cafe_claro)
    
    def hover_off(e):
        btn.config(bg=color_fondo)
    
    btn.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off)
    
    return btn

def abrir_login():
    login=tk.Tk()
    login.title("Romereus Pizzeria - Login")
    login.geometry("440x540")
    login.config(bg=crema)
    
    frame_logo=tk.Frame(login, bg=crema)
    frame_logo.pack(pady=(30, 10))
    
    logo_img=cargar_logos((200, 70))
    
    if logo_img:
        label_logo=tk.Label(frame_logo, image=logo_img, bg=crema)
        label_logo.pack()
        label_logo.image=logo_img
    else:
        tk.Label(
            frame_logo,
            text="ROMERAUS",
            font=("Georgia", 34, "bold"),
            bg=crema,
            fg=rojo
        ).pack()
        
        tk.Frame(
            frame_logo,
            bg=rojo,
            height=2,
            width=180
        ).pack(pady=(3, 3))
        
        tk.Label(
            frame_logo,
            text="Pizzeria & Restaurante",
            font=("Georgia", 12, "italic"),
            bg=crema,
            fg=cafe_oscuro
        ).pack()
    
    tarjeta=tk.Frame(
        login,
        bg=crema_oscuro,
        relief="raised",
        bd=3,
        highlightbackground=cafe_claro,
        highlightthickness=2,
        padx=35,
        pady=25
    )
    tarjeta.pack(padx=35, pady=(10, 25), fill="both", expand=True)
    
    usuarios=cargar_usuarios()
    usuario_var=tk.StringVar()
    contrasena_var=tk.StringVar()
    recordar_var=tk.BooleanVar()
    
    icono_user=cargar_icono_usuario()
    icono_pass=cargar_icono_contrasena()

    frame_user=tk.Frame(tarjeta, bg=crema_oscuro)
    frame_user.pack(fill="x", pady=(0, 3))
    
    if icono_user:
        tk.Label(frame_user, image=icono_user, bg=crema_oscuro).pack(side="left", padx=(0, 5))
        frame_user.image=icono_user
    
    tk.Label(
        frame_user,
        text="Usuario",
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        anchor="w"
    ).pack(side="left")
    
    entrada_usuario=tk.Entry(
        tarjeta,
        textvariable=usuario_var,
        font=letra_normal,
        bg=crema,
        relief="solid",
        bd=2
    )
    entrada_usuario.pack(fill="x", pady=(0, 15))

    frame_pass=tk.Frame(tarjeta, bg=crema_oscuro)
    frame_pass.pack(fill="x", pady=(0, 3))
    
    if icono_pass:
        tk.Label(frame_pass, image=icono_pass, bg=crema_oscuro).pack(side="left", padx=(0, 5))
        frame_pass.image=icono_pass
    
    tk.Label(
        frame_pass,
        text="Contraseña",
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        anchor="w"
    ).pack(side="left")
    
    entrada_contrasena=tk.Entry(
        tarjeta,
        textvariable=contrasena_var,
        font=letra_normal,
        bg=crema,
        relief="solid",
        bd=2,
        show="*"
    )
    entrada_contrasena.pack(fill="x", pady=(0, 15))
    
    tk.Checkbutton(
        tarjeta,
        text="Recordarme",
        variable=recordar_var,
        bg=crema_oscuro,
        fg=texto,
        font=letra_normal,
        selectcolor=crema,
        activebackground=crema_oscuro
    ).pack(anchor="w", pady=(0, 15))
    
    label_estado=tk.Label(
        tarjeta,
        text="",
        fg=rojo,
        bg=crema_oscuro,
        font=letra_normal
    )
    label_estado.pack()
    
    def entrar():
        usuario=usuario_var.get().strip()
        contrasena=contrasena_var.get().strip()
        
        if usuario == "" or contrasena == "":
            label_estado.config(text="Complete todos los campos")
            return
        
        if login_usuario(usuario, contrasena, usuarios):
            if recordar_var.get():
                guardar_recordar(usuario, contrasena)
            else:
                borrar_recordar()
            
            messagebox.showinfo("Bienvenido", f"Hola {usuario}")
            login.destroy()
            from menu_pedidos import abrir_menu
            abrir_menu(usuario)
        else:
            label_estado.config(text="Usuario o contrasena incorrectos")
    
    frame_botones=tk.Frame(tarjeta, bg=crema_oscuro)
    frame_botones.pack(pady=(15, 0))
    
    icono_login=cargar_icono_login()
    btn_login=boton_estilo(frame_botones, " Ingresar", entrar, rojo, icono_login)
    btn_login.pack(side="left", padx=5)
    
    datos_guardados=cargar_recordar()
    if datos_guardados:
        usuario_var.set(datos_guardados.get("usuario", ""))
        contrasena_var.set(datos_guardados.get("contrasena", ""))
        recordar_var.set(True)
    
    login.bind("<Return>", lambda e: entrar())
    login.mainloop()

if __name__ == "__main__":
    abrir_login()