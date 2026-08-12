## script automatizado para descargar, recortar y adaptar todas las imagenes del menu

import os
import urllib.request
from PIL import Image, ImageOps

directorio_destino_grafico = os.path.join("imagenes", "productos")
os.makedirs(directorio_destino_grafico, exist_ok=True)

catalogo_recursos_remotos = {
ruta_carpeta = os.path.join("imagenes", "productos")
os.makedirs(ruta_carpeta, exist_ok=True)

# enlaces de imagenes de alta calidad ajustados a los nombres exactos de menu.json
imagenes_productos = {
    # Combos
    "combo.png": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=500",
    "combo_individual.png": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=500",
    "combo_pareja.png": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500",
    "combo_familiar.png": "https://images.unsplash.com/photo-1544982503-9f984c14501a?w=500",
    "combo_fiesta.png": "https://images.unsplash.com/photo-1528137871618-79d2761e3fd5?w=500",

    # Bebidas
    "coca-cola.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca_cola.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca-cola_personal.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca_cola_personal.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca-cola_1l.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca_cola_1l.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca-cola_2l.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "coca_cola_2l.png": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "sprite.png": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=500",
    "sprite_personal.png": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=500",
    "fanta.png": "https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=500",
    "fanta_personal.png": "https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=500",
    "jugo_natural.png": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=500",
    "agua.png": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500",
    "agua_sin_gas.png": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500",
    "agua_con_gas.png": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500",

    # Postres
    "volcan_de_chocolate.png": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500",
    "cheesecake.png": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500",
    "helado.png": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=500",
    "tiramisu.png": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500",

    # Pizzas
    "margarita.png": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500",
    "pepperoni.png": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500",
    "hawaiana.png": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500",
    "vegetariana.png": "https://images.unsplash.com/photo-1511688878353-3a2f5be94cd7?w=500",
    "cuatro_quesos.png": "https://images.unsplash.com/photo-1573821663912-569905455b1c?w=500",
    "especial_de_la_casa.png": "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=500",

    # Otros
    "alitas_de_pollo.png": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=500",
    "papas_fritas.png": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=500",
    "pan_de_ajo.png": "https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=500"
}

cabeceras_peticion_http = {"User-Agent": "Mozilla/5.0"}

print("Descargando, ajustando y recortando imagenes para la interfaz...")

for identificador_archivo, url_origen in catalogo_recursos_remotos.items():
    ruta_almacenamiento_final = os.path.join(directorio_destino_grafico, identificador_archivo)
    
    try:
        peticion_web = urllib.request.Request(url_origen, headers=cabeceras_peticion_http)
        with urllib.request.urlopen(peticion_web) as respuesta_servidor, open(ruta_almacenamiento_final, "wb") as flujo_escritura:
            flujo_escritura.write(respuesta_servidor.read())
        
        instancia_matriz_imagen = Image.open(ruta_almacenamiento_final).convert("RGB")
        imagen_normalizada = ImageOps.fit(instancia_matriz_imagen, (160, 100), Image.Resampling.LANCZOS)
        imagen_normalizada.save(ruta_almacenamiento_final, "PNG")
        
        print(f"ok -> {identificador_archivo}")
    except Exception as excepcion_capturada:
        print(f"error con {identificador_archivo}: {excepcion_capturada}")

print("¡Proceso finalizado! Todas las imagenes estan ajustadas en imagenes/productos/")
headers = {"User-Agent": "Mozilla/5.0"}

print("Descargando, ajustando y recortando imagenes para la interfaz...")

for nombre_archivo, url in imagenes_productos.items():
    ruta_destino = os.path.join(ruta_carpeta, nombre_archivo)
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(ruta_destino, "wb") as f:
            f.write(response.read())
        
        # Redimensionado y recorte estandar (160x100) para encajar perfectamente en las tarjetas
        img = Image.open(ruta_destino).convert("RGB")
        img_recortada = ImageOps.fit(img, (160, 100), Image.Resampling.LANCZOS)
        img_recortada.save(ruta_destino, "PNG")
        
        print(f"ok -> {nombre_archivo}")
    except Exception as e:
        print(f"error con {nombre_archivo}: {e}")

print("\n¡Proceso finalizado! Todas las imagenes estan ajustadas en imagenes/productos/")
