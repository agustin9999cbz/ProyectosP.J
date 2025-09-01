import json
import csv
import os

def pedir_numero(mensaje, tipo=float):
    """Pide un número al usuario y valida su tipo (int o float)."""
    valor = input(mensaje)
    try:
        return tipo(valor)
    except ValueError:
        print(f"Error: el valor debe ser un {tipo.__name__}.")
        return None

def cargar_inventario():
    """Carga el inventario desde un archivo JSON si existe."""
    if os.path.exists("inventario.json"):
        with open("inventario.json", "r") as archivo:
            return json.load(archivo)
    return []

def guardar_inventario(inventario):
    """Guarda el inventario actual en un archivo JSON."""
    with open("inventario.json", "w") as archivo:
        json.dump(inventario, archivo, indent=4)

def generar_id(inventario):
    """Genera un ID único para un nuevo producto."""
    if not inventario:
        return 1
    return max(p["id"] for p in inventario) + 1

def agregar_producto(inventario):
    """Agrega un nuevo producto al inventario."""
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    precio = pedir_numero("Precio: ", float)
    stock = pedir_numero("Stock: ", int)

    if precio is None or stock is None:
        return

    producto = {
        "id": generar_id(inventario),
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
    }

    inventario.append(producto)
    print("Producto agregado.")

def modificar_producto(inventario):
    """Modifica un producto existente por su ID."""
    id_buscar = pedir_numero("ID del producto a modificar: ", int)
    if id_buscar is None:
        return

    for producto in inventario:
        if producto["id"] == id_buscar:
            producto["nombre"] = input("Nuevo nombre: ") or producto["nombre"]
            producto["categoria"] = input("Nueva categoría: ") or producto["categoria"]

            precio = input("Nuevo precio: ")
            if precio:
                try:
                    producto["precio"] = float(precio)
                except ValueError:
                    print("Precio inválido, no se modificó.")

            stock = input("Nuevo stock: ")
            if stock:
                try:
                    producto["stock"] = int(stock)
                except ValueError:
                    print("Stock inválido, no se modificó.")

            print("Producto modificado.")
            return

    print("Producto no encontrado.")

def eliminar_producto(inventario):
    """Elimina un producto por su ID."""
    id_buscar = pedir_numero("ID del producto a eliminar: ", int)
    if id_buscar is None:
        return

    for producto in inventario:
        if producto["id"] == id_buscar:
            inventario.remove(producto)
            print("Producto eliminado.")
            return

    print("Producto no encontrado.")

def listar_productos(inventario):
    """Muestra todos los productos del inventario, con orden opcional."""
    if not inventario:
        print("No hay productos.")
        return

    orden = input("Ordenar por (nombre/precio)? Dejar vacío para sin orden: ")
    if orden in ["nombre", "precio"]:
        inventario = sorted(inventario, key=lambda x: x[orden])

    for p in inventario:
        print(f"ID: {p['id']} | Nombre: {p['nombre']} | Categoría: {p['categoria']} | "
              f"Precio: ${p['precio']} | Stock: {p['stock']}")

def buscar_producto(inventario):
    """Busca productos por nombre o categoría."""
    palabra = input("Buscar por nombre o categoría: ").lower()
    encontrados = [p for p in inventario if palabra in p["nombre"].lower() or palabra in p["categoria"].lower()]

    if not encontrados:
        print("No se encontraron coincidencias.")
        return

    for p in encontrados:
        print(f"ID: {p['id']} | Nombre: {p['nombre']} | Categoría: {p['categoria']} | "
              f"Precio: ${p['precio']} | Stock: {p['stock']}")

def exportar_a_csv(inventario):
    """Exporta el inventario a un archivo CSV."""
    with open("inventario.csv", "w", newline="") as archivo:
        campos = ["id", "nombre", "categoria", "precio", "stock"]
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(inventario)
    print("Exportado a inventario.csv")

def exportar_a_json(inventario):
    """Exporta el inventario a un archivo JSON adicional."""
    with open("inventario_exportado.json", "w") as archivo:
        json.dump(inventario, archivo, indent=4)
    print("Exportado a inventario_exportado.json")

def menu():
    """Función principal del menú del programa."""
    inventario = cargar_inventario()
    opciones = {
        "1": agregar_producto,
        "2": modificar_producto,
        "3": eliminar_producto,
        "4": listar_productos,
        "5": buscar_producto,
        "6": exportar_a_csv,
        "7": exportar_a_json
    }

    while True:
        print("\nMenú:")
        print("1. Agregar producto")
        print("2. Modificar producto")
        print("3. Eliminar producto")
        print("4. Listar productos")
        print("5. Buscar producto")
        print("6. Exportar a CSV")
        print("7. Exportar a JSON")
        print("0. Salir")

        opcion = input("Opción: ")

        if opcion == "0":
            guardar_inventario(inventario)
            print("Inventario guardado. ¡Hasta luego!")
            break

        accion = opciones.get(opcion)
        if accion:
            accion(inventario)
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
