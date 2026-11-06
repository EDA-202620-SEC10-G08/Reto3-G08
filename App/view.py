import sys
from App import logic


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
    marca = input("Marca a analizar (ej: Nike): ").strip()
    desc_min = int(input("Descuento mínimo (%): "))
    desc_max = int(input("Descuento máximo (%): "))
    tiempo, total, costo, ordenes = logic.req_1(control, marca, desc_min, desc_max)
    print("\nTiempo de ejecución (ms):", round(tiempo, 2))
    print("Número total de órdenes:", total)
    print("Costo total final (USD):", round(costo, 2))
    if total == 0:
        print("No hay órdenes que cumplan el filtro.")
    else:
        if total > 10:
            print("Mostrando las primeras 5 y las últimas 5 órdenes:")
        filas = []
        i = 0
        while i < total:
            if total <= 10 or i < 5 or i >= total - 5:
                v = ordenes["elements"][i]
                filas.append([v["order_id"], v["order_date"], v["brand"],
                              v["model_name"], v["category"], v["country"],
                              v["sales_channel"], v["discount_percent"],
                              v["final_price_usd"]])
            i += 1
        imprimir_tabla(["order_id", "Fecha", "Marca", "Modelo", "Categoría",
                        "País", "Canal", "Descuento %", "Precio final USD"], filas)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
