import os
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd


class Obd2Analyzer(object):
    def __init__(self, csvfile, num_gruppo, vehicle):
        self.csvfile = csvfile
        self.used_trip_distance = list()
        self.consumo_medio_ist = self.evaluateConsumoMedioIst()
        self.num_gruppo = num_gruppo
        self.vehicle = vehicle

    def __lt__(self, other) -> bool:
        return self.consumo_medio_ist[-1] > other.consumo_medio_ist[-1]

    def __eq__(self, other) -> bool:
        return self.consumo_medio_ist[-1] == other.consumo_medio_ist[-1]

    def __str__(self):
        return "gruppo: " + str(self.num_gruppo) + "\t\t" \
               + "veicolo utilizzato: " + self.vehicle + "\t\t" \
               + "consumo medio istantaneo: " + str(self.consumo_medio_ist[-1]) \
               + "  km/L"

    @staticmethod
    def getData(csvfile):
        kpl = list()
        trip_d = list()

        if ".xlsx" in csvfile:  # conservione eventuale excel in csv
            csvfile = xlsxlToCsv(csvfile)

        with open(csvfile, "r") as f:  # check esistenza file controllato prima
            reader = csv.reader(f)
            intestaz = next(reader)
            r1 = indexOf(intestaz, "Trip Distance(km)")
            r2 = indexOf(intestaz, "Kilometers Per Litre(Instant)(kpl)")

            try:
                for riga in reader:
                    trip_d.append(riga[r1])
                    kpl.append(riga[r2])

                trip_d, kpl = list(zip(*[(s, kpl[i]) for i, s in enumerate(trip_d) if is_float(kpl[i], s)]))
                trip_d, kpl = list(np.float_(trip_d)), list(np.float_(kpl))
            except ValueError:
                raise ValueError
            finally:
                f.close()

            return linearInterp(kpl), trip_d

    def evaluateConsumoMedioIst(self) -> list:
        consumi_ist, trip_distance = self.getData(self.csvfile)
        ripartizione = list()
        consumo_medio_ist = list()
        sommatoria = 0

        for i in range(0, len(consumi_ist) - 2):
            litr = (trip_distance[i + 1] - trip_distance[i]) / consumi_ist[i]
            sommatoria += litr
            ripartizione.append(sommatoria)

            if ripartizione[i] != 0:
                self.used_trip_distance.append(trip_distance[i])
                consumo_medio_ist.append(trip_distance[i] / ripartizione[i])

        return consumo_medio_ist

    def getConsumoMedioIst(self):
        return self.consumo_medio_ist[-1]

    def plotConsumo(self):
        plt.gcf().canvas.set_window_title(
            "grafico consumo gruppo {} ({})".format(str(self.num_gruppo), self.vehicle)
        )
        plt.plot(self.used_trip_distance, self.consumo_medio_ist)
        plt.xlabel("Spazio percorso[km]")
        plt.ylabel("Consumo medio istantaneo[km/L]")
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


def linearInterp(my_list):
    pulisciUpper(my_list)
    pulisciLower(my_list)

    y_iniz = np.array(my_list)
    x = np.arange(len(y_iniz))
    idx = np.nonzero(y_iniz)
    interp = interp1d(x[idx], y_iniz[idx])
    y_fixed = interp(x)

    return y_fixed


def xlsxlToCsv(excel_file):
    data_xls = pd.read_excel(excel_file, index_col=None)
    data_xls.to_csv('muori_celermente.csv',
                    encoding='utf-8', index=False)
    return os.getcwd() + '/muori_celermente.csv'


def indexOf(my_list, element):
    return my_list.index(element)


def is_float(*arg):
    try:
        for i in arg:
            float(i)
        return True
    except ValueError:
        return False


