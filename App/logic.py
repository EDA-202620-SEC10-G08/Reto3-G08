import time
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
import csv
import os



def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    return {"lista_ventas": al.new_list(),
            "mapa_canales": mlp.new_map(2,0.5)
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
        
    return catalog
        
    

# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


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
