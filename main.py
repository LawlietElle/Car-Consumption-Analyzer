from pkg.ObdII import *
import subprocess
import os
import matplotlib.pyplot as plt


def find_files(file_name):
    """only works for Debian based Linux distros"""
    command = ['locate', file_name]

    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()
    search_results = output.split()

    search_results.sort()
    return search_results


esperienze = list()  # lista di oggetti
paths = find_files("torqueTrackLog")
groups = {
    1: "Volkswagen Polo 2004",  # 1
    2: "Lancia Phedra 2010",  # 2 (Cinghio)
    3: "Fiat 500L 2018 Benzina",  # 11 (noi)
    4: "Fiat Panda 2012 Benzina-GPL",  # 14 (Cosimo Bromo)
    5: "Renault Megane Diesel", # 15 (Dario)
    6: "Subaru Legacy Station Wagon Benzina/Gpl", # (Michele)
    7: "Volkswagen Golf 2012",
    8: "Volkswagen Polo 2014 Benzina Euro 6"
    }

if not paths:
    raise Exception("nessun file con quel nome sul computer")

if __name__ == "__main__":
    resoconto = list()

    for key, value in groups.items():
        esperienze.append(Obd2Analyzer(paths[key - 1], key, value))

        """
        se ho convertito un xlsx elimino il csv
        generato da me
        """
        if "muori_celermente.csv" in os.listdir(os.getcwd()):
            subprocess.call(['rm', 'muori_celermente.csv'])

    esperienze.sort()  # funziona grazie all'Overload degli operatori
    print(*esperienze, sep="\n")

    for i in range(len(esperienze)):
        esperienze[i].plotConsumo()
        resoconto.append([esperienze[i].used_trip_distance, esperienze[i].consumo_medio_ist])

    for i in range(len(esperienze)):
        plt.plot(resoconto[i][0], resoconto[i][1])

    plt.gcf().canvas.set_window_title("grafico globale")
    plt.grid()
    plt.legend([i.vehicle for i in esperienze])
    plt.xlim(-0.2, 6)
    plt.xlabel("Spazio percorso[km]")
    plt.ylabel("Consumo medio istantaneo[km/L]")
    plt.show(block=True)








