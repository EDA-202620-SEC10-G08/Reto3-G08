def default_sort_criteria(element1, element2):
    """
    Criterio de ordenamiento por defecto.
    Compara dos elementos y retorna True si element1 < element2.
    """
    if element1 < element2:
        return True
    return False


def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0
    }
    return newlist

def is_empty(my_list):
    return my_list["size"] == 0

def size(my_list):
    return my_list["size"]

def add_first(my_list, element):
    node = {"info": element, "next": my_list["first"]}
    my_list["first"] = node
    if my_list["size"] == 0:
        my_list["last"] = node
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    node = {"info": element, "next": None}
    if my_list["size"] == 0:
        my_list["first"] = node
        my_list["last"] = node
    else:
        my_list["last"]["next"] = node
        my_list["last"] = node
    my_list["size"] += 1
    return my_list

def first_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["first"]["info"]

def last_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["last"]["info"]

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]


def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1

    if not is_in_array:
        count = -1
    return count

def remove_first(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    node = my_list["first"]
    my_list["first"] = node["next"]
    if my_list["first"] is None:
        my_list["last"] = None
    my_list["size"] -= 1
    return node["info"]

def remove_last(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    if my_list["size"] == 1:
        node = my_list["first"]
        my_list["first"] = None
        my_list["last"] = None
    else:
        prev = my_list["first"]
        while prev["next"] is not my_list["last"]:
            prev = prev["next"]
        node = my_list["last"]
        prev["next"] = None
        my_list["last"] = prev
    my_list["size"] -= 1
    return node["info"]

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise IndexError("list index out of range")
    if pos == 0:
        return add_first(my_list, element)
    if pos == my_list["size"]:
        return add_last(my_list, element)
    prev = my_list["first"]
    count = 0
    while count < pos - 1:
        prev = prev["next"]
        count += 1
    node = {"info": element, "next": prev["next"]}
    prev["next"] = node
    my_list["size"] += 1
    return my_list

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    if pos == 0:
        my_list["first"] = my_list["first"]["next"]
        if my_list["first"] is None:
            my_list["last"] = None
    else:
        prev = my_list["first"]
        count = 0
        while count < pos - 1:
            prev = prev["next"]
            count += 1
        removed = prev["next"]
        prev["next"] = removed["next"]
        if removed is my_list["last"]:
            my_list["last"] = prev
    my_list["size"] -= 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    node = my_list["first"]
    count = 0
    while count < pos:
        node = node["next"]
        count += 1
    node["info"] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    list_size = my_list["size"]
    if pos_1 < 0 or pos_1 >= list_size or pos_2 < 0 or pos_2 >= list_size:
        raise IndexError("list index out of range")
    node_1 = my_list["first"]
    count = 0
    while count < pos_1:
        node_1 = node_1["next"]
        count += 1
    node_2 = my_list["first"]
    count = 0
    while count < pos_2:
        node_2 = node_2["next"]
        count += 1
    temp = node_1["info"]
    node_1["info"] = node_2["info"]
    node_2["info"] = temp
    return my_list

def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    sublist = new_list()
    node = my_list["first"]
    count = 0
    while count < pos:
        node = node["next"]
        count += 1
    count = 0
    while node is not None and count < num_elements:
        sublist = add_last(sublist, node["info"])
        node = node["next"]
        count += 1
    return sublist

def selection_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena una SingleLinkedList usando el algoritmo Selection Sort.
    Recorre los nodos con punteros e intercambia únicamente el campo "info".
    """
    node_i = my_list["first"]
    while node_i is not None and node_i["next"] is not None:
        min_node = node_i
        node_j = node_i["next"]
        while node_j is not None:
            if sort_criteria(node_j["info"], min_node["info"]):
                min_node = node_j
            node_j = node_j["next"]
        if min_node is not node_i:
            node_i["info"], min_node["info"] = min_node["info"], node_i["info"]
        node_i = node_i["next"]
    return my_list


def insertion_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena una SingleLinkedList usando el algoritmo Insertion Sort.
    """
    nodes = []
    node = my_list["first"]
    while node is not None:
        nodes.append(node)
        node = node["next"]

    for i in range(1, len(nodes)):
        current = nodes[i]["info"]
        j = i - 1
        while j >= 0 and sort_criteria(current, nodes[j]["info"]):
            nodes[j + 1]["info"] = nodes[j]["info"]
            j -= 1
        nodes[j + 1]["info"] = current

    return my_list


def shell_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena una SingleLinkedList usando el algoritmo Shell Sort.
    """
    n = size(my_list)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = get_element(my_list, i)
            j = i
            while j >= gap and sort_criteria(temp, get_element(my_list, j - gap)):
                change_info(my_list, j, get_element(my_list, j - gap))
                j -= gap
            change_info(my_list, j, temp)
        gap //= 2
    return my_list

def merge(left, right, sort_criteria):
    """
    Combina dos SingleLinkedList ya ordenadas en una única lista ordenada,
    recorriendo los nodos de cada una con punteros.
    """
    merged = new_list()
    node_left = left["first"]
    node_right = right["first"]

    while node_left is not None and node_right is not None:
        if sort_criteria(node_left["info"], node_right["info"]):
            merged = add_last(merged, node_left["info"])
            node_left = node_left["next"]
        else:
            merged = add_last(merged, node_right["info"])
            node_right = node_right["next"]

    while node_left is not None:
        merged = add_last(merged, node_left["info"])
        node_left = node_left["next"]

    while node_right is not None:
        merged = add_last(merged, node_right["info"])
        node_right = node_right["next"]

    return merged


def merge_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena una SingleLinkedList usando el algoritmo Merge Sort.
    """
    if my_list["size"] <= 1:
        return my_list

    mid = my_list["size"] // 2
    left_half = sub_list(my_list, 0, mid)
    right_half = sub_list(my_list, mid, my_list["size"] - mid)

    left_sorted = merge_sort(left_half, sort_criteria)
    right_sorted = merge_sort(right_half, sort_criteria)

    return merge(left_sorted, right_sorted, sort_criteria)


def concatenate(less, equal, greater):
    """
    Concatena las sublistas menores, iguales y mayores al pivote en una
    única SingleLinkedList, recorriendo los nodos de cada una.
    """
    result = new_list()
    node = less["first"]
    while node is not None:
        result = add_last(result, node["info"])
        node = node["next"]

    node = equal["first"]
    while node is not None:
        result = add_last(result, node["info"])
        node = node["next"]

    node = greater["first"]
    while node is not None:
        result = add_last(result, node["info"])
        node = node["next"]

    return result


def quick_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena una SingleLinkedList usando el algoritmo Quick Sort.
    """
    if my_list["size"] <= 1:
        return my_list

    pivot = first_element(my_list)
    less_than_pivot = new_list()
    equal_to_pivot = new_list()
    greater_than_pivot = new_list()

    equal_to_pivot = add_last(equal_to_pivot, pivot)

    # Se recorre desde el segundo nodo para no comparar el pivote consigo
    # mismo (si no, con criterios no estrictos como <= o >= el pivote se
    # reinsertaría en su propia sublista y la recursión nunca terminaría).
    node = my_list["first"]["next"]
    while node is not None:
        if sort_criteria(node["info"], pivot):
            less_than_pivot = add_last(less_than_pivot, node["info"])
        elif sort_criteria(pivot, node["info"]):
            greater_than_pivot = add_last(greater_than_pivot, node["info"])
        else:
            equal_to_pivot = add_last(equal_to_pivot, node["info"])
        node = node["next"]

    sorted_less = quick_sort(less_than_pivot, sort_criteria)
    sorted_greater = quick_sort(greater_than_pivot, sort_criteria)

    return concatenate(sorted_less, equal_to_pivot, sorted_greater)

