import sqlite3 as sql

# =========================
# Funciones Base de Datos
# =========================
def crearBD():
    try:
        conn = sql.connect("negocio.db")
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creando base de datos:", e)

def creartabla():
    try:
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS clientes(
                idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombreCliente TEXT NOT NULL,
                dni INTEGER NOT NULL UNIQUE
            )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS pedidos(
                idPedido INTEGER PRIMARY KEY AUTOINCREMENT,
                rubro TEXT NOT NULL,
                precio FLOAT NOT NULL,
                numCliente INTEGER NOT NULL,
                FOREIGN KEY(numCliente) REFERENCES clientes(idCliente)
            )"""
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creando tablas:", e)

def crearregs_clientes(lista_clientes):
    try:
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        instruccion = "INSERT INTO clientes (nombreCliente, dni) VALUES (?, ?)"
        cursor.executemany(instruccion, lista_clientes)
        conn.commit()
        conn.close()
    except sql.IntegrityError:
        print("Error: ya existe un cliente con ese DNI.")
    except Exception as e:
        print("Error insertando clientes:", e)

def crearregs_pedidos(lista_pedidos):
    try:
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        instruccion = "INSERT INTO pedidos (rubro, precio, numCliente) VALUES (?, ?, ?)"
        cursor.executemany(instruccion, lista_pedidos)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error insertando pedidos:", e)

# =========================
# Funciones CRUD Clientes
# =========================
def alta_clientes():
    try:
        nombre = input("Ingrese el nombre del nuevo cliente: ").strip()
        dni = int(input("Ingrese el DNI del nuevo cliente: "))
        crearregs_clientes([(nombre, dni)])
        print("Cliente nuevo creado.")
    except ValueError:
        print("Error: DNI debe ser un número.")
    except Exception as e:
        print("Error creando cliente:", e)

def baja_clientes():
    try:
        id_a_borrar = int(input("Ingrese el ID del cliente a borrar: "))
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE idCliente = ?", (id_a_borrar,))
        if cursor.rowcount == 0:
            print("No se encontró el cliente con ese ID.")
        else:
            print("Cliente borrado exitosamente.")
        conn.commit()
        conn.close()
    except ValueError:
        print("Error: ID debe ser un número.")
    except Exception as e:
        print("Error borrando cliente:", e)

def modificacion_clientes():
    try:
        id_a_modificar = int(input("Ingrese el ID del cliente a modificar: "))
        campo = input("Ingrese campo a modificar (nombreCliente / dni): ").strip()
        if campo not in ["nombreCliente", "dni"]:
            print("Campo inválido.")
            return
        valor_modificado = input("Ingrese el nuevo valor: ").strip()
        if campo == "dni":
            valor_modificado = int(valor_modificado)
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE clientes SET {campo} = ? WHERE idCliente = ?", (valor_modificado, id_a_modificar))
        if cursor.rowcount == 0:
            print("No se encontró el cliente con ese ID.")
        else:
            print("Cliente modificado exitosamente.")
        conn.commit()
        conn.close()
    except ValueError:
        print("Error: DNI o ID debe ser un número.")
    except Exception as e:
        print("Error modificando cliente:", e)

def listado_clientes():
    try:
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        if datos:
            for d in datos:
                print(d)
        else:
            print("No hay clientes cargados.")
    except Exception as e:
        print("Error mostrando clientes:", e)

def seleccion_clientes():
    try:
        conn = sql.connect("negocio.db")
        cursor = conn.cursor()
        dni_limite = int(input("Mostrar clientes con DNI menor a: "))
        cursor.execute("SELECT * FROM clientes WHERE dni < ?", (dni_limite,))
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        if datos:
            for d in datos:
                print(d)
        else:
            print("No se encontraron clientes con ese criterio.")
    except ValueError:
        print("Error: el valor debe ser un número.")
    except Exception as e:
        print("Error en selección de clientes:", e)

# =========================
# Menú Interactivo
# =========================
def menu_interactivo():
    while True:
        print("\nMenú Clientes:")
        print("1: ALTA\n2: BAJA\n3: MODIFICACIÓN\n4: LISTADO\n5: SELECCIÓN\n6: SALIR")
        opcion = input("Opción elegida: ").strip()
        if opcion == "1":
            alta_clientes()
        elif opcion == "2":
            baja_clientes()
        elif opcion == "3":
            modificacion_clientes()
        elif opcion == "4":
            listado_clientes()
        elif opcion == "5":
            seleccion_clientes()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Ingrese una opción válida!!")

# =========================
# Programa principal
# =========================
if __name__ == "__main__":
    crearBD()
    creartabla()
    # Lista inicial de clientes y pedidos
    lista_clientes = [("Juan Perez", 37100100), ("Pedro Gonzalez", 37200200)]
    lista_pedidos = [("jardin", 500540.80, 1), ("textil", 1000289.60, 2)]
    crearregs_clientes(lista_clientes)
    crearregs_pedidos(lista_pedidos)
    menu_interactivo()
