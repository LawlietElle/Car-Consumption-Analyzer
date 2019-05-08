import os
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd


class Obd2Analyzer:
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.used_trip_distance = list()
        self.consumo_medio_ist = self.evaluateConsumoMedioIst()

    def __lt__(self, other) -> bool:
        return self.consumo_medio_ist[-1] < other.consumo_medio_ist[-1]

    def __str__(self):
        return str(self.consumo_medio_ist[-1])

    def getData(self, csvfile):
        consumi_ist = list()
        trip_distance = list()

        # conservione eventuale excel in csv
        if ".xlsx" in csvfile:
            csvfile = xlsxltoCsv(csvfile)

        with open(csvfile, "r") as f:  # check esistenza file controllato prima
            reader = csv.reader(f)
            intestaz = next(reader)

            col_tripdistance = estrai_indici(intestaz, "Trip Distance(km)")
            col_consumi = estrai_indici(intestaz, "Kilometers Per Litre(Instant)(kpl)")

            for riga in reader:
                try:
                    if riga[col_tripdistance] != "-":
                        consumi_ist.append(float(riga[col_consumi]))
                        trip_distance.append(float(riga[col_tripdistance]))
                except ValueError:   # handling di più intestazioni
                    continue
        f.close()

        consumi_ist = self.linearInterp(consumi_ist)
        return consumi_ist, trip_distance

    def linearInterp(self, my_list):
        pulisciUpper(my_list)
        pulisciLower(my_list)

        y_iniz = np.array(my_list)
        x = np.arange(len(y_iniz))
        idx = np.nonzero(y_iniz)
        interp = interp1d(x[idx], y_iniz[idx])
        y_fixed = interp(x)

        return y_fixed

    def evaluateConsumoMedioIst(self) -> list:
        consumi_ist, trip_distance = self.getData(self.csvfile)
        ripartizione = list()
        litri_ist = list()
        consumo_medio_ist = list()
        sommatoria = 0

        for i in range(0, len(consumi_ist) - 2):
            litr = (trip_distance[i + 1] - trip_distance[i]) / consumi_ist[i]
            sommatoria += litr
            litri_ist.append(litr)
            ripartizione.append(sommatoria)

            if ripartizione[i] != 0:
                self.used_trip_distance.append(trip_distance[i])
                consumo_medio_ist.append(trip_distance[i] / ripartizione[i])

        return consumo_medio_ist

    def getConsumoMedioIst(self):
        return self.consumo_medio_ist[-1]

    def plotConsumo(self):
        plt.plot(self.used_trip_distance, self.consumo_medio_ist)
        plt.xlabel("Spazio percorso[km]")
        plt.ylabel("Consumo medio istantaneo[L/km]")
        plt.grid()
        plt.show()


# funzioni fuori dalla classe

def pulisciUpper(my_list):
    if my_list[0] == 0.0:
        my_list.remove(0)
        pulisciUpper(my_list)


def pulisciLower(my_list):
    if my_list[len(my_list) - 1] == 0.0:
        del my_list[-1]
        pulisciLower(my_list)


def xlsxltoCsv(excel_file):
    data_xls = pd.read_excel(excel_file, index_col=None)
    data_xls.to_csv('csvfile.csv', encoding='utf-8', index=False)
    return os.getcwd() + "/csvfile.csv"


def estrai_indici(my_list, element):
    return my_list.index(element)

