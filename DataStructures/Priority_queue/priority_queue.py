from DataStructures.Priority_queue import pq_entry as pqe
from DataStructures.List import array_list as al

def default_compare_higher_value(father_node, child_node):
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    return False

def exchange(my_heap, pos_1, pos_2):
    al.exchange(my_heap["elements"], pos_1, pos_2)
    return my_heap["elements"]

def new_heap(is_min_pq=True):
    if is_min_pq:
        cmp = default_compare_lower_value
    else:
        cmp = default_compare_higher_value
    heap = {
        "elements": al.new_list(),
        "size": 0,
        "cmp_function": cmp
    }
    al.add_first(heap["elements"], None)
    return heap

def insert(my_heap, priority, value):
    entrada = pqe.new_pq_entry(priority, value)
    al.add_last(my_heap["elements"], entrada)
    my_heap["size"] += 1
    swim(my_heap, my_heap["size"])  
    return my_heap

def swim(my_heap, pos):
    while pos // 2 != 0:
        padre_pos = pos // 2
        elem_hijo = al.get_element(my_heap["elements"], pos)
        elem_padre = al.get_element(my_heap["elements"], padre_pos)
        if not my_heap["cmp_function"](elem_padre, elem_hijo):
            exchange(my_heap, pos, padre_pos)
            pos = padre_pos
        else:
            break
    return my_heap

def size(my_heap):
    return my_heap["size"]
        
def is_empty(my_heap):
    if size(my_heap) == 0:
        return True
    else:
        return False

def priority(my_heap, parent, child):
    return my_heap["cmp_function"](parent, child)

def sink(my_heap, pos):
    while (pos*2) <= size(my_heap):
        elem_hijo = al.get_element(my_heap["elements"], pos*2)
        elem_padre = al.get_element(my_heap["elements"], pos)
        pos_hijo = pos*2
        if (pos*2 + 1) <= size(my_heap) and not priority(my_heap, elem_hijo, al.get_element(my_heap["elements"], pos*2 + 1)):
            elem_hijo = al.get_element(my_heap["elements"], pos*2 + 1)
            pos_hijo = pos*2 + 1
        if not priority(my_heap, elem_padre, elem_hijo):
            exchange(my_heap, pos, pos_hijo)
            pos = pos_hijo
        else:
            break
    return my_heap
       

def remove(my_heap):
    if is_empty(my_heap):
        return None
    raiz = al.get_element(my_heap["elements"], 1)
    exchange(my_heap, 1, my_heap["size"])
    al.remove_last(my_heap["elements"])
    my_heap["size"] -= 1
    sink(my_heap, 1)
    return pqe.get_value(raiz)

def get_first_priority(my_heap):
    if is_empty(my_heap):
        return None
    return pqe.get_value(al.get_element(my_heap["elements"], 1))

def is_present_value(my_heap, value):
    for i in range(1, size(my_heap)+1):
        elemento = al.get_element(my_heap["elements"], i)
        if pqe.get_value(elemento) == value:
            return i
    return -1

def contains(my_heap, value):
    if is_present_value(my_heap, value) != -1:
        return True
    return False

def improve_priority(my_heap, priority, value):
    pos = is_present_value(my_heap, value)
    if pos != -1:
        pqe.set_priority(al.get_element(my_heap["elements"], pos), priority)
        swim(my_heap, pos)
    return my_heap
