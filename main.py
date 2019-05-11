import os
from ObdII import *


def mergeSort(my_list):
    if len(my_list) > 1:
        mid = len(my_list) // 2
        lefthalf = my_list[:mid]
        righthalf = my_list[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i = j = k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                my_list[k] = lefthalf[i]
                i = i + 1
            else:
                my_list[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while i < len(lefthalf):
            my_list[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            my_list[k] = righthalf[j]
            j = j + 1
            k = k + 1


paths = list()
esperienze = list()  # lista di oggetti

# ... riempire groups da file, a manina, o come cazzo te pare
# esempio
groups = {1: "Nave spaziale", 2: "Incrociatore Galattico", 3: "Nave da guerra"}

for file in os.listdir(os.getcwd()):
    if ".csv" in file or ".xlsx" in file:
        paths.append(os.getcwd() + "/" + file)

if not paths:
    raise FileNotFoundError

if __name__ == "__main__":
    for key, value in groups.items():
        esperienze.append(Obd2Analyzer(paths[key - 1], key, value))

    mergeSort(esperienze)
    print(*esperienze, sep="\n")
    for i in range(len(esperienze)):
        esperienze[i].plotConsumo()
