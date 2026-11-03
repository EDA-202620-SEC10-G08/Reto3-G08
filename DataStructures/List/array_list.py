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
        "elements": [],
        "size": 0
    }
    return newlist

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    return my_list["elements"][pos]

def is_present (my_list, element, cmp_function):    
    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range (0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
               keyexist = True
               break
        if keyexist:
          return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

def size(my_list):
    return my_list["size"]

def first_element(my_list):
    return my_list["elements"][0]

def is_empty(my_list):
    return my_list["size"] == 0

def last_element(my_list):
    return my_list["elements"][my_list["size"] - 1]

def remove_last(my_list):
    element = my_list["elements"].pop()
    my_list["size"] -= 1
    return element

def change_info(my_list, index, newinfo):
    my_list["elements"][index] = newinfo
    return my_list

def remove_first(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    element = my_list["elements"].pop(0)
    my_list["size"] -= 1
    return element

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise IndexError("list index out of range")
    my_list["elements"].insert(pos, element)
    my_list["size"] += 1
    return my_list

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    del my_list["elements"][pos]
    my_list["size"] -= 1
    return my_list

def exchange(my_list, pos_1, pos_2):
    size = my_list["size"]
    if pos_1 < 0 or pos_1 >= size or pos_2 < 0 or pos_2 >= size:
        raise IndexError("list index out of range")
    elements = my_list["elements"]
    elements[pos_1], elements[pos_2] = elements[pos_2], elements[pos_1]
    return my_list

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list["size"]:
        raise IndexError("list index out of range")
    sublist = new_list()
    sublist["elements"] = my_list["elements"][pos_i:pos_i + num_elements]
    sublist["size"] = len(sublist["elements"])
    return sublist

def selection_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena un ArrayList usando el algoritmo Selection Sort.
    """
    size = my_list["size"]
    elements = my_list["elements"]

    for i in range(size - 1):
        min_index = i
        for j in range(i + 1, size):
            if sort_criteria(elements[j], elements[min_index]):
                min_index = j
        if min_index != i:
            elements[i], elements[min_index] = elements[min_index], elements[i]

    return my_list



def insertion_sort(my_list, sort_crit=default_sort_criteria):
    """_summary_

    Args:
        my_list (_type_): _description_
        sort_crit (_type_, optional): _description_. Defaults to default_sort_criteria.

    Returns:
        _type_: _description_
    """

    size = my_list["size"]
    elements = my_list["elements"]

    for i in range(1, size):
        current = elements[i]
        j = i - 1
        while j >= 0 and sort_crit(current, elements[j]):
            elements[j + 1] = elements[j]
            j -= 1
        elements[j + 1] = current

    return my_list

def shell_sort(my_list, cmp_function=default_sort_criteria):
    n = size(my_list)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = get_element(my_list, i)
            j = i
            while j >= gap and cmp_function(temp, get_element(my_list, j - gap)):
                change_info(my_list, j, get_element(my_list, j - gap))
                j -= gap
            change_info(my_list, j, temp)
        gap //= 2
    return my_list



def merge(left, right, sort_criteria):
    """
    Combina dos ArrayList ya ordenados en un único ArrayList ordenado.
    """
    merged = new_list()
    i = 0
    j = 0
    left_size = size(left)
    right_size = size(right)

    while i < left_size and j < right_size:
        left_elem = get_element(left, i)
        right_elem = get_element(right, j)
        if sort_criteria(left_elem, right_elem):
            merged = add_last(merged, left_elem)
            i += 1
        else:
            merged = add_last(merged, right_elem)
            j += 1

    while i < left_size:
        merged = add_last(merged, get_element(left, i))
        i += 1

    while j < right_size:
        merged = add_last(merged, get_element(right, j))
        j += 1

    return merged

 
def merge_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena un ArrayList usando el algoritmo Merge Sort.
    """
    if size(my_list) <= 1:
        return my_list

    mid = size(my_list) // 2
    left_half = sub_list(my_list, 0, mid)
    right_half = sub_list(my_list, mid, size(my_list) - mid)

    left_sorted = merge_sort(left_half, sort_criteria)
    right_sorted = merge_sort(right_half, sort_criteria)

    return merge(left_sorted, right_sorted, sort_criteria)


def concatenate(less, equal, greater):
    """
    Concatena las sublistas menores, iguales y mayores al pivote en un
    único ArrayList.
    """
    result = new_list()
    for i in range(size(less)):
        result = add_last(result, get_element(less, i))
    for i in range(size(equal)):
        result = add_last(result, get_element(equal, i))
    for i in range(size(greater)):
        result = add_last(result, get_element(greater, i))
    return result


def quick_sort(my_list, sort_criteria=default_sort_criteria):
    """
    Ordena un ArrayList usando el algoritmo Quick Sort.
    """
    if size(my_list) <= 1:
        return my_list

    pivot = get_element(my_list, 0)
    less_than_pivot = new_list()
    equal_to_pivot = new_list()
    greater_than_pivot = new_list()

    equal_to_pivot = add_last(equal_to_pivot, pivot)

    for i in range(1, size(my_list)):
        current = get_element(my_list, i)
        if sort_criteria(current, pivot):
            less_than_pivot = add_last(less_than_pivot, current)
        elif sort_criteria(pivot, current):
            greater_than_pivot = add_last(greater_than_pivot, current)
        else:
            equal_to_pivot = add_last(equal_to_pivot, current)

    sorted_less = quick_sort(less_than_pivot, sort_criteria)
    sorted_greater = quick_sort(greater_than_pivot, sort_criteria)

    return concatenate(sorted_less, equal_to_pivot, sorted_greater)