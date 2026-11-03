from DataStructures.Tree import rbt_node
from DataStructures.List import single_linked_list as sll

def new_map():
    my_rbt = {"root": None,
              "type": "RBT"
    }
    return my_rbt

def put(my_rbt, key, value):
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] =rbt_node.BLACK
    return my_rbt

def insert_node(root, key, value):
    if root == None:
        return rbt_node.new_node(key, value, rbt_node.RED)
    else:
        comparacion = default_compare(key, root)
        if comparacion == 0:
            root["value"] = value
        elif comparacion == 1:
            root["right"] = insert_node(root["right"], key, value)
        else:
            root["left"] = insert_node(root["left"], key, value)
    
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
    root["size"] = 1 + size_tree(root["right"]) + size_tree(root["left"])
    return root


def default_compare(key, element):
    if key == rbt_node.get_key(element):
      return 0
    elif key > rbt_node.get_key(element):
      return 1
    return -1


def rotate_left(node_rbt):
    x = node_rbt["right"]
    node_rbt["right"] = x["left"]
    x["left"] = node_rbt
    color_x = x["color"]
    color_h = node_rbt["color"]
    x["color"] = color_h
    node_rbt["color"] = color_x
    node_rbt["size"] = 1 + size_tree(node_rbt["right"]) + size_tree(node_rbt["left"])
    x["size"] = 1 + size_tree(x["right"]) + size_tree(x["left"])
    return x
    
def rotate_right(node_rbt):
    x = node_rbt["left"]
    node_rbt["left"] = x["right"]
    x["right"] = node_rbt
    color_x = x["color"]
    color_h = node_rbt["color"]
    x["color"] = color_h
    node_rbt["color"] = color_x
    node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])
    x["size"] = 1 + size_tree(x["left"]) + size_tree(x["right"])
    return x
    

def flip_colors(node_rbt):
    flip_node_color(node_rbt)
    flip_node_color(node_rbt["right"])
    flip_node_color(node_rbt["left"])
    return node_rbt


def flip_node_color(node_rbt):
    if is_red(node_rbt):
        rbt_node.change_color(node_rbt, 1)
    else:
        rbt_node.change_color(node_rbt, 0)
    return node_rbt


def size_tree(root):
    if root == None:
        return 0
    else:
        return root["size"]

def is_red(node_rbt):
    if node_rbt == None:
        return False
    return rbt_node.is_red(node_rbt)
        





def get(my_rbt, key):
    return get_node(my_rbt["root"], key)



def get_node(root, key):
    if root == None:
        return None
    else:
        compara = default_compare(key, root)
        if compara == 0:
            return rbt_node.get_value(root)
        elif compara == 1:
            return get_node(root["right"], key)
        else:
            return get_node(root["left"], key)



def contains(my_rbt, key):
    return get_node(my_rbt["root"], key) is not None


def size(my_rbt):
    return size_tree(my_rbt["root"])


def is_empty(my_rbt):
    return my_rbt["root"] is None

def key_set(my_rbt):
    key_list = sll.new_list()
    return key_set_tree(my_rbt["root"], key_list)

def key_set_tree(root, key_list):
    if root != None:
        key_set_tree(root["left"], key_list)
        sll.add_last(key_list, root["key"])
        key_set_tree(root["right"], key_list)
    return key_list

def value_set(my_rbt):
    value_list = sll.new_list()
    return value_set_tree(my_rbt["root"], value_list)

def value_set_tree(root, value_list):
    if root is not None:
        value_set_tree(root["left"], value_list)
        sll.add_last(value_list, root["value"])
        value_set_tree(root["right"], value_list)
    return value_list

def get_min(my_rbt):
    node = get_min_node(my_rbt["root"])
    return rbt_node.get_key(node)

def get_min_node(root):
    if root == None:
        return None
    if root["left"] == None:
        return root
    return get_min_node(root["left"])
        

def get_max(my_rbt):
    node = get_max_node(my_rbt["root"])
    return rbt_node.get_key(node)

def get_max_node(root):
    if root is not None and root["right"] is not None:
        return get_max_node(root["right"])
    return root

def height(my_rbt):
    return height_tree(my_rbt["root"])

def height_tree(root):
    if root == None:
        return 0
    return 1 + max(height_tree(root["right"]), height_tree(root["left"]))

def keys(my_rbt, key_initial, key_final):
    list_key = sll.new_list()
    return keys_range(my_rbt["root"], key_initial, key_final, list_key)

def keys_range(root, key_initial, key_final, list_key):
    if root is not None:
        if key_initial < root["key"]:
            keys_range(root["left"], key_initial, key_final, list_key)
        if key_initial <= root["key"] <= key_final:
            sll.add_last(list_key, root["key"])
        if key_final > root["key"]:
            keys_range(root["right"], key_initial, key_final, list_key)
    return list_key


def values(my_rbt, key_initial, key_final):
    value_list = sll.new_list()
    return values_range(my_rbt["root"], key_initial, key_final, value_list)


def values_range(root, key_initial, key_final, value_list):
    if root != None:
        if root["key"] > key_initial:
            values_range(root["left"], key_initial, key_final, value_list)
        if key_initial <= root["key"] <= key_final:
            sll.add_last(value_list, root["value"])
        if root["key"] < key_final:
            values_range(root["right"], key_initial, key_final, value_list)
    return value_list

