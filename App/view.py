import sys
from App import logic
from DataStructures.List import single_linked_list as sll
from DataStructures.List import array_list as al


def new_logic():
    """
        Se crea una instancia del controlador
    """
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    archivos = ["global_sports_footwear_sales-small.csv",
                "global_sports_footwear_sales-medium.csv",
                "global_sports_footwear_sales-large.csv"]
    print("Seleccione el archivo: 1- small, 2- medium, 3- large")
    opcion = int(input())
    if opcion < 1 or opcion > 3:
        print("Opción errónea, se usará small.")
        opcion = 1
    inicio = logic.get_time()
    logic.load_data(control, archivos[opcion - 1])
    fin = logic.get_time()
    print("Tiempo de carga (ms):", round(logic.delta_time(inicio, fin), 2))
    print("Total de registros cargados:", control["lista_ventas"]["size"])
    resumen = logic.resumen_carga(control)
    columnas = ["order_id", "Fecha", "Marca", "Modelo", "Categoría",
                "Precio final USD", "Unidades", "Ingreso USD", "País", "Canal"]
    for titulo, v in [("Venta con menor precio final", resumen["menor"]),
                      ("Venta con mayor precio final", resumen["mayor"])]:
        print("\n" + titulo + ":")
        imprimir_tabla(["order_id", "Marca", "Modelo", "Categoría",
                        "Precio final USD", "País"],
                       [[v["order_id"], v["brand"], v["model_name"], v["category"],
                         v["final_price_usd"], v["country"]]])
    for titulo, lista in [("Primeros 5 registros cargados", resumen["primeros_5"]),
                          ("Últimos 5 registros cargados", resumen["ultimos_5"])]:
        filas = []
        for i in range(al.size(lista)):
            v = al.get_element(lista, i)
            filas.append([v["order_id"], v["order_date"], v["brand"], v["model_name"],
                          v["category"], v["final_price_usd"], v["units_sold"],
                          v["revenue_usd"], v["country"], v["sales_channel"]])
        print("\n" + titulo + ":")
        imprimir_tabla(columnas, filas)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def imprimir_tabla(columnas, filas):
    """
    Imprime una tabla de texto alineada (sin librerías externas)
    """
    anchos = []
    for i in range(len(columnas)):
        ancho = len(columnas[i])
        for fila in filas:
            if len(str(fila[i])) > ancho:
                ancho = len(str(fila[i]))
        anchos.append(ancho)
    linea = "+" + "+".join("-" * (a + 2) for a in anchos) + "+"
    print(linea)
    print("| " + " | ".join(columnas[i].ljust(anchos[i]) for i in range(len(columnas))) + " |")
    print(linea)
    for fila in filas:
        print("| " + " | ".join(str(fila[i]).ljust(anchos[i]) for i in range(len(columnas))) + " |")
    print(linea)


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # Paso 1: pedir los datos al usuario
    marca = input("Marca a analizar (ej: Nike): ").strip()
    desc_min = int(input("Descuento mínimo (%): "))
    desc_max = int(input("Descuento máximo (%): "))

    # Paso 2: llamar a la lógica
    resultado = logic.req_1(control, marca, desc_min, desc_max)

    # Paso 3: mostrar el resumen
    print("\nTiempo de ejecución (ms):", round(resultado["tiempo"], 2))
    print("Número total de órdenes:", resultado["total_num_pedidos"])
    print("Costo total final (USD):", resultado["costo_total"])

    if resultado["total_num_pedidos"] == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        if resultado["total_num_pedidos"] > 10:
            print("Mostrando las primeras 5 y las últimas 5 órdenes:")

        # Paso 4: armar las filas de la tabla (primeras 5 y últimas 5)
        filas = []
        for lista in (resultado["primeros_5"], resultado["ultimos_5"]):
            for i in range(sll.size(lista)):
                v = sll.get_element(lista, i)
                filas.append([v["order_id"], v["order_date"], v["brand"],
                              v["model_name"], v["category"], v["country"],
                              v["sales_channel"], v["discount_percent"],
                              v["final_price_usd"]])
        imprimir_tabla(["order_id", "Fecha", "Marca", "Modelo", "Categoría",
                        "País", "Canal", "Descuento %", "Precio final USD"], filas)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    pais = input("País a analizar (ej: USA): ").strip()
    calif_min = float(input("Calificación mínima (ej: 3.5): "))
    calif_max = float(input("Calificación máxima (ej: 5.0): "))
    resultado = logic.req_2(control, pais, calif_min, calif_max)

    print("\nTiempo de ejecución (ms):", round(resultado["tiempo"], 2))
    print("Número total de órdenes:", resultado["total_num_pedidos"])
    print("Costo total final (USD):", resultado["costo_total"])

    if resultado["total_num_pedidos"] == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        if resultado["total_num_pedidos"] > 10:
            print("Mostrando las primeras 5 y las últimas 5 órdenes:")
        filas = []
        for lista in (resultado["primeros_5"], resultado["ultimos_5"]):
            for i in range(sll.size(lista)):
                v = sll.get_element(lista, i)
                filas.append([v["order_id"], v["order_date"], v["brand"],
                              v["model_name"], v["country"], v["sales_channel"],
                              v["customer_rating"], v["final_price_usd"],
                              v["revenue_usd"]])
        imprimir_tabla(["order_id", "Fecha", "Marca", "Modelo", "País", "Canal",
                        "Calificación", "Precio final USD", "Ingresos USD"], filas)

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    canal_venta = input("Indique canal de venta: ").strip()
    categoria = input("Indique categoría: ").strip()
    precio_min = float(input("Indique precio mínimo: "))
    precio_max = float(input("Indique precio máximo: "))

    resultado = logic.req_3(control, canal_venta, categoria, precio_min, precio_max)

    print("Tiempo de ejecución:", round(resultado["tiempo"], 2))
    print("Número total de órdenes:", resultado["total_num_pedidos"])
    print("Costo total final:", resultado["costo_total"])

    if resultado["total_num_pedidos"] == 0:
        print("No hay órdenes que cumplan el filtro.")
        return

    if resultado["total_num_pedidos"] > 10:
        print("Mostrando las primeras 5 y las últimas 5 órdenes:")

    filas = []
    for nombre in ["primeros_5", "ultimos_5"]:
        lista = resultado[nombre]
        for i in range(sll.size(lista)):
            p = sll.get_element(lista, i)
            filas.append([p["order_id"], p["order_date"], p["brand"],
                          p["model_name"], p["category"], p["sales_channel"],
                          p["country"], p["final_price_usd"], p["units_sold"]])

    imprimir_tabla(["order_id", "Fecha", "Marca", "Modelo", "Categoría",
                    "Canal", "País", "Precio final USD", "Unidades"], filas)

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    fecha_min = input("Fecha inicial AAAA-MM-DD: ").strip()
    fecha_max = input("Fecha final AAAA-MM-DD: ").strip()
    nivel_economico = input("Nivel de ingresos del cliente (Low, Medium o High): ").strip()
    n = int(input("Cantidad N de marcas: "))
    resultado = logic.req_4(control, fecha_min, fecha_max, n, nivel_economico)

    print()
    print("Tiempo de ejecución (ms):", round(resultado["tiempo"], 2))
    print("Número total de marcas consideradas:", resultado["marcas_en_filtro"])

    if resultado["total_marcas"] == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        filas_marcas = []
        filas_ordenes = []
        for i in range(al.size(resultado["marcas"])):
            m = al.get_element(resultado["marcas"], i)
            o = m["mayor_orden"]
            filas_marcas.append([m["marca"], m["total"],
                                 round(m["precio_promedio"], 2),
                                 round(m["revenue_promedio"], 2)])
            filas_ordenes.append([m["marca"], o["order_id"], o["order_date"],
                                  o["brand"] + " " + o["model_name"],
                                  o["country"], o["sales_channel"],
                                  o["final_price_usd"], o["revenue_usd"]])
        print()
        print("Marcas con mayor número de órdenes:")
        imprimir_tabla(["Marca", "Órdenes", "Precio final promedio USD",
                        "Ingreso promedio USD"], filas_marcas)
        print()
        print("Orden con mayor ingreso generado de cada marca:")
        imprimir_tabla(["Marca", "order_id", "Fecha", "Marca y modelo", "País",
                        "Canal", "Precio final USD", "Ingreso USD"], filas_ordenes)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    pais = input("País a analizar (ej: Germany): ").strip()
    fecha_ini = input("Fecha inicial AAAA-MM-DD (ej: 2021-01-01): ").strip()
    fecha_fin = input("Fecha final AAAA-MM-DD (ej: 2023-12-31): ").strip()
    n = int(input("Cantidad N de marcas (ej: 5): "))
    resultado = logic.req_5(control, pais, fecha_ini, fecha_fin, n)

    print("\nTiempo de ejecución (ms):", round(resultado["tiempo"], 2))
    print("Número total de marcas consideradas:", resultado["marcas_en_filtro"])

    if resultado["total_marcas"] == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        filas_marcas = []
        filas_ordenes = []
        for i in range(al.size(resultado["marcas"])):
            m = al.get_element(resultado["marcas"], i)
            o = m["mayor_orden"]
            filas_marcas.append([m["marca"], m["total"],
                                 round(m["rating_promedio"], 3),
                                 round(m["revenue_promedio"], 2)])
            filas_ordenes.append([m["marca"], o["order_id"], o["order_date"],
                                  o["brand"] + " " + o["model_name"],
                                  o["country"], o["sales_channel"],
                                  o["units_sold"], o["customer_rating"]])
        print("\nMarcas con mejor calificación promedio:")
        imprimir_tabla(["Marca", "Órdenes", "Calificación promedio",
                        "Ingreso promedio USD"], filas_marcas)
        print("\nOrden con más unidades vendidas de cada marca:")
        imprimir_tabla(["Marca", "order_id", "Fecha", "Marca y modelo", "País",
                        "Canal", "Unidades", "Calificación"], filas_ordenes)


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    fecha_ini = input("Fecha inicial AAAA-MM-DD (ej: 2021-01-01): ").strip()
    fecha_fin = input("Fecha final AAAA-MM-DD (ej: 2023-12-31): ").strip()
    precio_min = float(input("Precio base mínimo (ej: 50.0): "))
    precio_max = float(input("Precio base máximo (ej: 200.0): "))
    n = int(input("Cantidad N de marcas (ej: 5): "))
    resultado = logic.req_6(control, fecha_ini, fecha_fin, precio_min, precio_max, n)

    print("\nTiempo de ejecución (ms):", round(resultado["tiempo"], 2))
    print("Número total de marcas en el filtro:", resultado["marcas_en_filtro"])

    if resultado["total_marcas"] == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        filas_marcas = []
        filas_ordenes = []
        for i in range(al.size(resultado["marcas"])):
            m = al.get_element(resultado["marcas"], i)
            o = m["orden_cercana"]
            filas_marcas.append([m["marca"], m["total"],
                                 round(m["descuento_promedio"], 3),
                                 round(m["desviacion"], 3)])
            filas_ordenes.append([m["marca"], o["order_id"], o["order_date"],
                                  o["brand"] + " " + o["model_name"],
                                  o["country"], o["sales_channel"],
                                  o["discount_percent"]])
        print("\nMarcas más consistentes en descuentos:")
        imprimir_tabla(["Marca", "Órdenes", "Descuento promedio %",
                        "Desviación estándar"], filas_marcas)
        print("\nOrden con el descuento más cercano al promedio de cada marca:")
        imprimir_tabla(["Marca", "order_id", "Fecha", "Marca y modelo", "País",
                        "Canal", "Descuento %"], filas_ordenes)

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)