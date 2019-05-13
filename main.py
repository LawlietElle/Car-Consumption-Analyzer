from ObdII import *
import subprocess


def find_files(file_name):
    """only works for Debian based Linux distros"""
    command = ['locate', file_name]

    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()
    search_results = output.split()

    search_results.sort()

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
    1: "Incrociatore Galattico",
    2: "Fiat 500L 2018 Benzina",
    3: "Fiat Panda 2012 Benzina-GPL"
}
"""
for file in os.listdir(os.getcwd()):
    if ".csv" in file or ".xlsx" in file:
        paths.append(os.getcwd() + "/" + file)
"""


if not paths:
    raise FileNotFoundError

if __name__ == "__main__":
    for key, value in groups.items():
        esperienze.append(Obd2Analyzer(paths[key - 1], key, value))

    mergeSort(esperienze)
    print(*esperienze, sep="\n")
    for i in range(len(esperienze)):
        esperienze[i].plotConsumo()
