import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


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


def litresToKpl(litr) -> list:
    kpl = list()
    kpl.append(100/float(i) for i in litr if i > 0)
    return kpl


def shift_and_allign(my_list) -> list:
    iniz = my_list[0]
    my_list[:] = [x - iniz for x in my_list]

    return my_list
