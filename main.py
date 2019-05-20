from ObdII import *
from Obd_kind2 import *
import subprocess


def find_files(file_name):
    """only works for Debian based Linux distros"""
    command = ['locate', file_name]

    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()
    search_results = output.split()

    search_results.sort()
    print(search_results)

    return search_results


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
                i += 1
            else:
                my_list[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            my_list[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            my_list[k] = righthalf[j]
            j += 1
            k += 1


esperienze = list()  # lista di oggetti
paths = find_files("torqueTrackLog")
groups = {
    1: "Volkswagen polo 2004",  # 1
    2: "Lancia Phedra 2010",  # 2 (Cinghio(?))
    # 3: "Renault Megane diesel", # 11 (Simone Peluffo)
    3: "Fiat 500L 2018 Benzina",  # 11 (noi)
    4: "Fiat Panda 2012 Benzina-GPL",  # 14 (Cosimo Bromo)
    5: "boh", # 15 (Dario(?))
    6: "bohpt2"
}

if not paths:
    raise Exception("nessun file con quel nome sul computer")

if __name__ == "__main__":
    for key, value in groups.items():
        try:
            esperienze.append(Obd2Analyzer(paths[key - 1], key, value))
        except ValueError:
            esperienze.append(Obd2Analyzer2(paths[key - 1], key, value))

    mergeSort(esperienze)
    print(*esperienze, sep="\n")
    for i in range(len(esperienze)):
        esperienze[i].plotConsumo()

