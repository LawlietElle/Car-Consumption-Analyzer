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

# ... riempire groups da file, a manina, o come cazzo te pare


# esempio
groups = {1: "Nave spaziale", 2: "Incrociatore Galattico"}
paths = list()
esperienze = list()  # lista di oggetti


for file in os.listdir(os.getcwd()):
    if file.endswith(".csv") or file.endswith(".xlsx"):
        paths.append(os.getcwd() + "/" + file)

if not paths:
    raise FileNotFoundError

if __name__ == "__main__":
    for key, value in groups.items():
        esperienze.append(Obd2Analyzer(paths[key - 1]))

    mergeSort(esperienze)
    for ind in range(len(groups)):
        print("gruppo : {}\tveicolo: {}\tconsumo: {} L/km".format(ind + 1, groups[ind + 1], esperienze[ind]))
        esperienze[ind].plotConsumo()
