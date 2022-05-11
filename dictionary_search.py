import random
import dictionary_load

dict=dictionary_load.load_data()
list=dict.get("測試1")
random.shuffle(list)
#random.shuffle(list)
print(list)


