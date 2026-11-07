import time
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Tree import red_black_tree as rbt
import csv
import os



def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    return {"lista_ventas": al.new_list(),
            "mapa_canales": mlp.new_map(2,0.5),
            "indice_marcas": mlp.new_map(10, 0.5)
    }


# Funciones para la carga de datos

csv.field_size_limit(2147483647)
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    
    archivo = data_dir + filename
    input_file = csv.DictReader(open(archivo, encoding="utf-8"))
    for venta in input_file:
        venta["base_price_usd"] = int(venta["base_price_usd"])
        venta["discount_percent"] = int(venta["discount_percent"])
        venta["final_price_usd"] = float(venta["final_price_usd"])
        venta["units_sold"] = int(venta["units_sold"])
        venta["revenue_usd"] = float(venta["revenue_usd"])
        venta["customer_rating"] = float(venta["customer_rating"])
        venta["size"] = int(venta["size"])
        al.add_last(catalog["lista_ventas"], venta)
        indexar_venta_por_marca(catalog, venta)
        
    return catalog
        
    

# Funciones de consulta sobre el catálogo


def indexar_venta_por_marca(catalog, venta):
    """
    REQ 1: Inserta la venta en el RBT de su marca. La llave es la tupla
    (discount_percent, order_date, order_id): el recorrido en orden del arbol
    entrega descuento ascendente y, en empate, fecha ascendente. El order_id
    hace la llave unica para que ninguna venta se sobrescriba.
    """
    arbol = mlp.get(catalog["indice_marcas"], venta["brand"])
    if arbol is None:
        arbol = rbt.new_map()
        mlp.put(catalog["indice_marcas"], venta["brand"], arbol)
    llave = (venta["discount_percent"], venta["order_date"], venta["order_id"])
    rbt.put(arbol, llave, venta)


def req_1(catalog, marca, desc_min, desc_max):
    """
    Retorna el resultado del requerimiento 1: ordenes de una marca con
    descuento en [desc_min, desc_max] (limites incluidos).
    Retorna (tiempo_ms, total_ordenes, costo_total, lista_ordenada)
    """
    inicio = get_time()
    resultado = al.new_list()
    total_costo = 0.0
    arbol = mlp.get(catalog["indice_marcas"], marca)
    if arbol is not None:
        ordenes = rbt.values(arbol,
                             (desc_min, "0000-00-00", ""),
                             (desc_max, "9999-99-99", "~"))
        nodo = ordenes["first"]
        while nodo is not None:
            venta = nodo["info"]
            al.add_last(resultado, venta)
            total_costo += venta["final_price_usd"]
            nodo = nodo["next"]
    fin = get_time()
    return delta_time(inicio, fin), al.size(resultado), total_costo, resultado


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, canal_venta, categoria, precio_min, precio_max):
    """
    Retorna el resultado del requerimiento 3
    """
    tiempo_inicial = get_time()
    
    arbol_precios = rbt.new_map()
    suma_total = 0
    suma_num_pedidos = 0
    
    lista_ventas = catalog["lista_ventas"]
    for i in range(al.size(lista_ventas)):
        venta = al.get_element(lista_ventas, i)
        if venta["sales_channel"] == canal_venta and venta["category"] == categoria and venta["final_price_usd"] >= precio_min and venta["final_price_usd"] <= precio_max:
            suma_total += venta["final_price_usd"]
            suma_num_pedidos += 1
            llave = (venta["final_price_usd"], venta["order_date"], venta["order_id"])
            rbt.put(arbol_precios, llave, venta)
    
    lista_ordenada = rbt.value_set(arbol_precios)
    if sll.size(lista_ordenada) > 10:
        primeros_5 = sll.sub_list(lista_ordenada, 0, 5)
        ultimos_5 = sll.sub_list(lista_ordenada, sll.size(lista_ordenada)-5, 5)
        
    else:
        primeros_5 = lista_ordenada
        ultimos_5 = sll.new_list()
    
    tiempo_final = get_time()
    
    diferencia_tiempo = delta_time(tiempo_inicial, tiempo_final)

    
    return {
        "tiempo":          diferencia_tiempo,
        "total_num_pedidos":   suma_num_pedidos,
        "costo_total":    round(suma_total, 2),
        "primeros_5":        primeros_5,
        "ultimos_5":         ultimos_5,
    }



def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
