from PIL import Image, ImageTk
import os 


ruta_imagenes="imagenes"

def cargar_imagen(ruta, tamaño=None):
    ruta_completa = os.path.join(ruta_imagenes, ruta)
    if not os.path.exists(ruta_completa):
        return None

    try:
        img = Image.open(ruta_completa)
        if tamaño:
            img = img.resize(tamaño, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error al cargar imagen {ruta}: {e}")
        return None

def cargar_logos(tamaño=(28, 20)):
    return cargar_imagen ("logo.jpeg", tamaño)

def cargar_icono_categoria(categoria, tamaño=(28, 28)):
    mapa={
        "Pizzas":"pizzas.png",
        "Combos":"combos.png",
        "Bebidas":"bebidas.png",
        "Postres":"postres.png",
        "Otros":"otros.png"
    }
    archivo=mapa.get(categoria,"default.png")
    return cargar_imagen(f"categorias{archivo}", tamaño)

def cargar_imagen_productos(nombre, tamaño=(80, 60)):
    nombre_archivo = nombre.lower().replace(" ", "_").replace("(", "").replace(")", "")
    return cargar_imagen(f"productos/{nombre_archivo}.png", tamaño)

def cargar_icono_usuario(tamaño=(20, 20)):
    return cargar_imagen("icono_usuario", tamaño)

def cargar_icono_contraseña(tamaño=(20, 20)):
    return cargar_imagen("icono_contraseña", tamaño)

def cargar_icono_login(tamaño=(20, 20)):
    return cargar_imagen("icono_login", tamaño)

def cargar_icono_logout(tamaño=(16,16)):
    return cargar_imagen("icono_logout", tamaño)

def cargar_icono_check(tamaño=(20,20)):
    return cargar_imagen("icono_check", tamaño)

def cargar_icono_historial(tamaño=(20,20)):
    return cargar_imagen("icono_historial", tamaño)

def cargar_icono_borrar(tamaño=(16,16)):
    return cargar_imagen("icono_borrar", tamaño)

