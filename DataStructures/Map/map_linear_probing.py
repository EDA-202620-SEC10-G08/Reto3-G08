import random
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
   capacity = mf.next_prime(int(num_elements / load_factor))
   table = lt.new_list()
   for _ in range(capacity):
      table = lt.add_last(table, me.new_map_entry(None, None))

   my_map = {
      "prime": prime,
      "capacity": capacity,
      "scale": random.randint(1, prime - 1),
      "shift": random.randint(0, prime - 1),
      "table": table,
      "current_factor": 0,
      "limit_factor": load_factor,
      "size": 0
   }
   return my_map


def default_compare(key, entry):
   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1


def is_available(table, pos):
   entry = lt.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False


def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = lt.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, lt.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail


def rehash(my_map):
   old_table = my_map["table"]
   my_map["capacity"] = mf.next_prime(2 * my_map["capacity"])
   my_map["table"] = lt.new_list()
   for _ in range(my_map["capacity"]):
      my_map["table"] = lt.add_last(my_map["table"], me.new_map_entry(None, None))
   my_map["size"] = 0
   my_map["current_factor"] = 0

   for i in range(lt.size(old_table)):
      entry = lt.get_element(old_table, i)
      key = me.get_key(entry)
      if key is not None and key != "__EMPTY__":
         my_map = put(my_map, key, me.get_value(entry))
   return my_map


def put(my_map, key, value):
   hash_value = mf.hash_value(my_map, key)
   occupied, pos = find_slot(my_map, key, hash_value)
   lt.change_info(my_map["table"], pos, me.new_map_entry(key, value))
   if not occupied:
      my_map["size"] += 1
      my_map["current_factor"] = my_map["size"] / my_map["capacity"]
      if my_map["current_factor"] >= my_map["limit_factor"]:
         my_map = rehash(my_map)
   return my_map


def contains(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   occupied, _ = find_slot(my_map, key, hash_value)
   return occupied


def get(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   occupied, pos = find_slot(my_map, key, hash_value)
   if not occupied:
      return None
   entry = lt.get_element(my_map["table"], pos)
   return me.get_value(entry)


def remove(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   occupied, pos = find_slot(my_map, key, hash_value)
   if occupied:
      lt.change_info(my_map["table"], pos, me.new_map_entry("__EMPTY__", "__EMPTY__"))
      my_map["size"] -= 1
      my_map["current_factor"] = my_map["size"] / my_map["capacity"]
   return my_map


def size(my_map):
   return my_map["size"]


def is_empty(my_map):
   return my_map["size"] == 0


def key_set(my_map):
   keys = lt.new_list()
   for i in range(my_map["capacity"]):
      entry = lt.get_element(my_map["table"], i)
      key = me.get_key(entry)
      if key is not None and key != "__EMPTY__":
         keys = lt.add_last(keys, key)
   return keys


def value_set(my_map):
   values = lt.new_list()
   for i in range(my_map["capacity"]):
      entry = lt.get_element(my_map["table"], i)
      key = me.get_key(entry)
      if key is not None and key != "__EMPTY__":
         values = lt.add_last(values, me.get_value(entry))
   return values
