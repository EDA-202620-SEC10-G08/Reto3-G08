from DataStructures.Tree import bst_node as bst_node
from DataStructures.List import single_linked_list as sll


def new_map():
    return {"root": None}

def default_compare(key, element):
   if key == bst_node.get_key(element):
      return 0
   elif key > bst_node.get_key(element):
      return 1
   return -1

def insert_node(root, key, value):
    if root is None:
        return bst_node.new_node(key, value)
    
    compara = default_compare(key, root)

    if compara == 1:
        root["right"] = insert_node(root["right"], key, value)
    
    elif compara == -1:
        root["left"] = insert_node(root["left"], key, value)
    
    else:
        root["value"] = value 
        
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root

def put(my_bst, key, value):
    
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst
    
def get_node(root, key):   
    if root is None:
        return None
    if key == root["key"]:
        return root
    elif key < root["key"]:
        return get_node(root["left"], key)
    else:
        return get_node(root["right"], key)

def get(my_bst, key):
    nodo = get_node(my_bst["root"], key)
    return bst_node.get_value(nodo)

def size(my_bst):
    return size_tree(my_bst["root"])

def size_tree(root):
    if root is None:
        return 0
    else:
        return root["size"]

def contains(my_bst, key):
    res = get_node(my_bst["root"], key)
    if res is None:
        return False
    else:
        return True
    
def is_empty(my_bst):
    if my_bst["root"] == None:
        return True
    else:
        return False

def key_set(my_bst):
    lista = sll.new_list()
    key_set_tree(my_bst["root"], lista)
    return lista 

def key_set_tree(root, key_list):

    if root is not None:
        key_set_tree(root["left"], key_list)
        sll.add_last(key_list,bst_node.get_key(root))
        key_set_tree(root["right"], key_list)

    return key_list


def value_set(my_bst):
    lista = sll.new_list()
    value_set_tree(my_bst["root"], lista)
    return lista

def value_set_tree(root, value_list):
    if root is None:
        return value_list
    
    value_set_tree(root["left"], value_list)
    sll.add_last(value_list, bst_node.get_value(root))
    value_set_tree(root["right"], value_list)
    
    return value_list
    
def get_min(my_bst):
    return get_min_node(my_bst["root"])

def get_min_node(root):
    if root is None:
        return None
    elif root["left"] is None:
        return bst_node.get_key(root)
    elif root["left"] is not None:
        return get_min_node(root["left"])
    

def get_max(my_bst):
    return get_max_node(my_bst["root"])

def get_max_node(root):
    if root == None:
        return None
    if root["right"] == None:
        return bst_node.get_key(root)
    if root["right"] != None:
        return get_max_node(root["right"])

def delete_min_tree(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    root["size"] = size_tree(root["left"]) + size_tree(root["right"]) + 1
    return root

def delete_min(my_bst):
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst


def delete_max(my_bst):
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst

def delete_max_tree(root):
    if root == None:
        return None
    elif root["right"] != None:
        root["right"] = delete_max_tree(root["right"])
    else:
        return root["left"]
    
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root

def height(my_bst):
    return height_tree(my_bst["root"])

def height_tree(root):
    if root is None:
        return 0
    if root["left"] is None and root["right"] is None:
        return 0
    izq = height_tree(root["left"])
    der = height_tree(root["right"])
    return 1 + max(izq, der)

def keys(my_bst, key_initial, key_final):
    list_key = sll.new_list()
    return keys_range(my_bst["root"], key_initial, key_final, list_key)

def keys_range(root, key_initial, key_final, list_key):
    if root == None:
        return list_key
    if root["key"] > key_initial:
        keys_range(root["left"], key_initial, key_final, list_key)
    if root["key"] >= key_initial and root["key"] <= key_final:
        sll.add_last(list_key, bst_node.get_key(root))
    if root["key"] < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)
    return list_key

def values(my_bst, key_initial, key_final):
    lista = sll.new_list()
    values_range(my_bst["root"], key_initial, key_final, lista)
    return lista

def values_range(root, key_initial, key_final, list_value):
    if root is None:
        return list_value
    if key_initial < root["key"]:
        values_range(root["left"], key_initial, key_final, list_value)
    if key_initial <= root["key"] and root["key"] <= key_final:
        sll.add_last(list_value, bst_node.get_value(root))
    if key_final > root["key"]:
        values_range(root["right"], key_initial, key_final, list_value)
    return list_value
