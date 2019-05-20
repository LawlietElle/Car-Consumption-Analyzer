from ObdII import *
import csv
import numpy as np


class Obd2Analyzer2(Obd2Analyzer):
    def __init__(self, csvfile, num_gruppo, vehicle):
        Obd2Analyzer.__init__(self, csvfile, num_gruppo, vehicle)

    # Override
    @staticmethod
    def getData(csvfile):
        """
        :param csvfile:
        :return: linear interpolation of kpl obtained as litres per 100km / 100 ^(-1),
                trip distance(km)
        """
        trip_d = list()
        litr = list()

        with open(csvfile, "r") as f:  # check esistenza file controllato prima
            reader = csv.reader(f)
            intestaz = next(reader)
            r1 = indexOf(intestaz, "Trip Distance(km)")
            r2 = indexOf(intestaz, "Litres Per 100 Kilometer(Instant)(l/100km)")

            for riga in reader:
                trip_d.append(riga[r1])
                litr.append(riga[r2])

            trip_d, litr = list(zip(*[(s, litr[i]) for i, s in enumerate(trip_d) if is_float(litr[i], s)]))
            trip_d, kpl = [float(i) for i in trip_d], [100/float(i) for i in litr]

            f.close()
            return linearInterp(kpl), trip_d

