<<<<<<< HEAD
=======
## cargador de imagenes y logotipos

>>>>>>> cdfd3f53a63972ca271a950fab50f2b68c9e7cb4
import os 
from PIL import Image, ImageTk

ruta_imagenes="imagenes"

def cargar_imagen(ruta, tamano=None):
    ruta_completa=os.path.join(ruta_imagenes, ruta)
    if not os.path.exists(ruta_completa):
        return None

    try:
        img=Image.open(ruta_completa)
        if tamano:
            img=img.resize(tamano, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error al cargar imagen {ruta}: {e}")
        return None

def cargar_logos(tamano=(200, 70)):
    return cargar_imagen("logo.jpeg", tamano)

def cargar_icono_categoria(categoria, tamano=(28, 28)):
    mapa={
        "Pizzas": "pizzas.png",
        "Combos": "combos.png",
        "Bebidas": "bebidas.png",
        "Postres": "postres.png",
        "Otros": "otros.png"
    }
    archivo=mapa.get(categoria, "default.png")
    return cargar_imagen(os.path.join("categorias", archivo), tamano)

def cargar_imagen_productos(nombre, tamano=(120, 90)):
    nombre_archivo=nombre.lower().replace(" ", "_").replace("(", "").replace(")", "")
    return cargar_imagen(os.path.join("productos", f"{nombre_archivo}.png"), tamano)

def cargar_icono_usuario(tamano=(20, 20)):
    return cargar_imagen("icono_usuario.png", tamano)

def cargar_icono_contrasena(tamano=(20, 20)):
    return cargar_imagen("icono_contrasena.png", tamano)

def cargar_icono_login(tamano=(20, 20)):
    return cargar_imagen("icono_login.png", tamano)

def cargar_icono_logout(tamano=(16, 16)):
    return cargar_imagen("icono_logout.png", tamano)

def cargar_icono_check(tamano=(20, 20)):
    return cargar_imagen("icono_check.png", tamano)

def cargar_icono_historial(tamano=(20, 20)):
    return cargar_imagen("icono_historial.png", tamano)

def cargar_icono_borrar(tamano=(16, 16)):
    return cargar_imagen("icono_borrar.png", tamano)