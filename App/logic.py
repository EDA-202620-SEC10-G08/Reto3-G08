import time
import math
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Priority_queue import priority_queue as pq
import csv
import os



def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    return {"lista_ventas": al.new_list(),
            "mapa_canales": mlp.new_map(2,0.5),
            "indice_marcas": mlp.new_map(10, 0.5),
            "indice_paises": mlp.new_map(10, 0.5)
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
        indexar_venta_por_pais(catalog, venta)
        
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


def indexar_venta_por_pais(catalog, venta):
    """
    REQ 2: Inserta la venta en el RBT de su pais. La llave es la tupla
    (customer_rating, order_date, order_id): el arbol entrega calificacion
    ascendente y, en empate, fecha ascendente (el req_2 lo invierte).
    """
    arbol = mlp.get(catalog["indice_paises"], venta["country"])
    if arbol is None:
        arbol = rbt.new_map()
        mlp.put(catalog["indice_paises"], venta["country"], arbol)
    llave = (venta["customer_rating"], venta["order_date"], venta["order_id"])
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


def req_2(catalog, pais, calif_min, calif_max):
    """
    Retorna el resultado del requerimiento 2: ordenes de un pais con
    calificacion en [calif_min, calif_max], de la mayor calificacion a la menor
    y, en empate, de la fecha mas reciente a la mas antigua.
    """
    tiempo_inicial = get_time()

    lista_desc = sll.new_list()
    suma_total = 0

    arbol = mlp.get(catalog["indice_paises"], pais)
    if arbol is not None:
        # El RBT entrega las ordenes de menor a mayor
        ordenes = rbt.values(arbol,
                             (calif_min, "0000-00-00", ""),
                             (calif_max, "9999-99-99", "~"))
        nodo = ordenes["first"]
        while nodo is not None:
            venta = nodo["info"]
            # add_first las va dejando al reves: de mayor a menor
            sll.add_first(lista_desc, venta)
            suma_total += venta["final_price_usd"]
            nodo = nodo["next"]

    total = sll.size(lista_desc)
    if total > 10:
        primeros_5 = sll.sub_list(lista_desc, 0, 5)
        ultimos_5 = sll.sub_list(lista_desc, total - 5, 5)
    else:
        primeros_5 = lista_desc
        ultimos_5 = sll.new_list()

    tiempo_final = get_time()

    return {
        "tiempo":            delta_time(tiempo_inicial, tiempo_final),
        "total_num_pedidos": total,
        "costo_total":       round(suma_total, 2),
        "primeros_5":        primeros_5,
        "ultimos_5":         ultimos_5,
    }



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



def req_4(catalog, fecha_min, fecha_max, n, nivel_economico):
    """
    Retorna el resultado del requerimiento 4
    """
    
    tiempo_inicial = get_time()
    lista_ventas = catalog["lista_ventas"]
    mapa_marcas = mlp.new_map(6,0.5)

    for i in range(al.size(lista_ventas)):
        venta = al.get_element(lista_ventas, i)
        if venta["order_date"] >= fecha_min and venta["order_date"] <= fecha_max and venta["customer_income_level"] == nivel_economico:
            marca = venta["brand"]
            datos = mlp.get(mapa_marcas, marca)
            if datos is None:
                datos = {"marca": marca,
                      "total": 0,
                      "suma_precio": 0,
                      "suma_revenue": 0,
                      "mayor_orden": venta
                }
                mlp.put(mapa_marcas, marca, datos)
            datos["total"] += 1
            datos["suma_precio"] += venta["final_price_usd"]
            datos["suma_revenue"] += venta["revenue_usd"]
            
            mayor = datos["mayor_orden"]

            if venta["revenue_usd"] > mayor["revenue_usd"]:
                datos["mayor_orden"] = venta
            elif venta["revenue_usd"] == mayor["revenue_usd"] and venta["order_date"] > mayor["order_date"]:
                datos["mayor_orden"] = venta
    
    cola = pq.new_heap(True)
    lista_marcas = mlp.value_set(mapa_marcas)
    for i in range (al.size(lista_marcas)):
        datos = al.get_element(lista_marcas, i)
        pq.insert(cola, (-datos["total"], datos["marca"]), datos)
        
    resultado = al.new_list()
    
    while al.size(resultado) < n and not pq.is_empty(cola):
        datos = pq.remove(cola)
        datos["precio_promedio"] = datos["suma_precio"] / datos["total"]
        datos["revenue_promedio"] = datos["suma_revenue"] / datos["total"]
        al.add_last(resultado, datos)
    
       
    tiempo_final = get_time()
    
    diferencia_tiempo = delta_time(tiempo_inicial, tiempo_final)
    
    
    return {
        "tiempo":       diferencia_tiempo,
        "total_marcas": al.size(resultado),
        "marcas":       resultado,
    }


def req_5(catalog, pais, fecha_ini, fecha_fin, n):
    """
    Retorna el resultado del requerimiento 5: las N marcas con mejor calificacion
    promedio en un pais y un rango de fechas (AAAA-MM-DD, limites incluidos).
    """
    tiempo_inicial = get_time()

    # PASO 1: agrupar por marca las ventas que cumplen el filtro.
    # Tabla de hash: llave = marca, valor = diccionario con los acumulados.
    mapa_marcas = mlp.new_map(10, 0.5)
    lista_ventas = catalog["lista_ventas"]
    for i in range(al.size(lista_ventas)):
        venta = al.get_element(lista_ventas, i)
        if venta["country"] == pais and fecha_ini <= venta["order_date"] <= fecha_fin:
            marca = venta["brand"]
            datos = mlp.get(mapa_marcas, marca)
            if datos is None:
                datos = {"marca": marca,
                         "total": 0,
                         "suma_rating": 0,
                         "suma_revenue": 0,
                         "mayor_orden": venta}
                mlp.put(mapa_marcas, marca, datos)
            datos["total"] += 1
            datos["suma_rating"] += venta["customer_rating"]
            datos["suma_revenue"] += venta["revenue_usd"]

            # Orden con mas unidades vendidas (si empatan, la de mayor order_id)
            mayor = datos["mayor_orden"]
            if venta["units_sold"] > mayor["units_sold"]:
                datos["mayor_orden"] = venta
            elif venta["units_sold"] == mayor["units_sold"] and venta["order_id"] > mayor["order_id"]:
                datos["mayor_orden"] = venta

    # PASO 2: meter cada marca en una cola de prioridad (min-heap).
    # La prioridad es una tupla (-promedio, nombre): como es un min-heap, el
    # promedio mas alto (el mas negativo) sale primero y, si empatan, sale
    # primero el nombre que va antes en el alfabeto.
    cola = pq.new_heap(True)
    lista_marcas = mlp.value_set(mapa_marcas)
    for i in range(al.size(lista_marcas)):
        datos = al.get_element(lista_marcas, i)
        datos["rating_promedio"] = datos["suma_rating"] / datos["total"]
        datos["revenue_promedio"] = datos["suma_revenue"] / datos["total"]
        pq.insert(cola, (-datos["rating_promedio"], datos["marca"]), datos)

    # PASO 3: sacar las N mejores
    resultado = al.new_list()
    while not pq.is_empty(cola) and al.size(resultado) < n:
        al.add_last(resultado, pq.remove(cola))

    tiempo_final = get_time()

    return {
        "tiempo":           delta_time(tiempo_inicial, tiempo_final),
        "marcas_en_filtro": mlp.size(mapa_marcas),
        "total_marcas":     al.size(resultado),
        "marcas":           resultado,
    }


def req_6(catalog, fecha_ini, fecha_fin, precio_min, precio_max, n):
    """
    Retorna el resultado del requerimiento 6: las N marcas mas consistentes en
    descuentos (menor desviacion estandar poblacional de discount_percent) para
    un rango de fechas y un rango de precios base (limites incluidos).
    """
    tiempo_inicial = get_time()

    # PASO 1: agrupar por marca las ventas que cumplen el filtro.
    # Tabla de hash: llave = marca, valor = diccionario con la lista de ventas.
    mapa_marcas = mlp.new_map(10, 0.5)
    lista_ventas = catalog["lista_ventas"]
    for i in range(al.size(lista_ventas)):
        venta = al.get_element(lista_ventas, i)
        if (fecha_ini <= venta["order_date"] <= fecha_fin
                and precio_min <= venta["base_price_usd"] <= precio_max):
            marca = venta["brand"]
            datos = mlp.get(mapa_marcas, marca)
            if datos is None:
                datos = {"marca": marca, "ventas": al.new_list(), "suma_descuentos": 0}
                mlp.put(mapa_marcas, marca, datos)
            al.add_last(datos["ventas"], venta)
            datos["suma_descuentos"] += venta["discount_percent"]

    # PASO 2: por cada marca calcular promedio, desviacion estandar y la orden
    # cuyo descuento esta mas cerca del promedio. Luego meterla en la cola de
    # prioridad (min-heap) con prioridad (desviacion, promedio, nombre):
    # sale primero la menor desviacion y, si empatan, el menor promedio.
    cola = pq.new_heap(True)
    lista_marcas = mlp.value_set(mapa_marcas)
    for i in range(al.size(lista_marcas)):
        datos = al.get_element(lista_marcas, i)
        ventas = datos["ventas"]
        total = al.size(ventas)
        promedio = datos["suma_descuentos"] / total

        # Desviacion estandar poblacional
        suma_cuadrados = 0
        for j in range(total):
            venta = al.get_element(ventas, j)
            suma_cuadrados += (venta["discount_percent"] - promedio) ** 2
        desviacion = math.sqrt(suma_cuadrados / total)

        # Orden con el descuento mas cercano al promedio (empate: menor order_id)
        cercana = al.get_element(ventas, 0)
        for j in range(1, total):
            venta = al.get_element(ventas, j)
            dif = abs(venta["discount_percent"] - promedio)
            dif_cercana = abs(cercana["discount_percent"] - promedio)
            if dif < dif_cercana:
                cercana = venta
            elif dif == dif_cercana and venta["order_id"] < cercana["order_id"]:
                cercana = venta

        datos["total"] = total
        datos["descuento_promedio"] = promedio
        datos["desviacion"] = desviacion
        datos["orden_cercana"] = cercana
        pq.insert(cola, (desviacion, promedio, datos["marca"]), datos)

    # PASO 3: sacar las N mas consistentes
    resultado = al.new_list()
    while not pq.is_empty(cola) and al.size(resultado) < n:
        al.add_last(resultado, pq.remove(cola))

    tiempo_final = get_time()

    return {
        "tiempo":           delta_time(tiempo_inicial, tiempo_final),
        "marcas_en_filtro": mlp.size(mapa_marcas),
        "total_marcas":     al.size(resultado),
        "marcas":           resultado,
    }


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