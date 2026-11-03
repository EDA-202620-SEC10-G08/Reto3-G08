import random
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
   capacity = mf.next_prime(int(num_elements / load_factor))
   table = lt.new_list()
   for _ in range(capacity):
      table = lt.add_last(table, sl.new_list())

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


def put(my_map, key, value):
   hash_value = mf.hash_value(my_map, key)
   bucket = lt.get_element(my_map["table"], hash_value)
   pos = sl.is_present(bucket, key, default_compare)
   if pos != -1:
      sl.change_info(bucket, pos, me.new_map_entry(key, value))
   else:
      sl.add_last(bucket, me.new_map_entry(key, value))
      my_map["size"] += 1
      my_map["current_factor"] = my_map["size"] / my_map["capacity"]
      if my_map["current_factor"] >= my_map["limit_factor"]:
         my_map = rehash(my_map)
   return my_map


def contains(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   bucket = lt.get_element(my_map["table"], hash_value)
   return sl.is_present(bucket, key, default_compare) != -1


def get(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   bucket = lt.get_element(my_map["table"], hash_value)
   pos = sl.is_present(bucket, key, default_compare)
   if pos == -1:
      return None
   entry = sl.get_element(bucket, pos)
   return me.get_value(entry)


def remove(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   bucket = lt.get_element(my_map["table"], hash_value)
   pos = sl.is_present(bucket, key, default_compare)
   if pos != -1:
      sl.delete_element(bucket, pos)
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
      bucket = lt.get_element(my_map["table"], i)
      for j in range(sl.size(bucket)):
         entry = sl.get_element(bucket, j)
         keys = lt.add_last(keys, me.get_key(entry))
   return keys


def value_set(my_map):
   values = lt.new_list()
   for i in range(my_map["capacity"]):
      bucket = lt.get_element(my_map["table"], i)
      for j in range(sl.size(bucket)):
         entry = sl.get_element(bucket, j)
         values = lt.add_last(values, me.get_value(entry))
   return values


def rehash(my_map):
   old_table = my_map["table"]
   my_map["capacity"] = mf.next_prime(2 * my_map["capacity"])
   my_map["table"] = lt.new_list()
   for _ in range(my_map["capacity"]):
      my_map["table"] = lt.add_last(my_map["table"], sl.new_list())
   my_map["size"] = 0
   my_map["current_factor"] = 0

   for i in range(lt.size(old_table)):
      bucket = lt.get_element(old_table, i)
      for j in range(sl.size(bucket)):
         entry = sl.get_element(bucket, j)
         my_map = put(my_map, me.get_key(entry), me.get_value(entry))
   return my_map
