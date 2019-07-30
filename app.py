import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime
import argparse

from datetime import timedelta
from addDate import addition

from addDate import get_rt
from addDate import get_crt
from addDate import get_trt
from addDate import get_np
from addDate import get_date_np


class RockTask:
    """Init Class"""
    def __init__(self):
        self.done_ext_pr = addition("prices")
        self.done_ext_pr = addition("weights")
        self.done_ext_exch = addition("exchanges")

        self.date = get_date_np()  # 0 - price, 1 - ex, 2 - weight
        self.columns = get_np()  # 0 - price, 1 - ex, 2 - weight

    """Methods for task"""

    def calculate_asset_performance(self, start_date, end_date) -> pd.Series:
        start_date = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
        end_date = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
        rt = get_rt(start_date, end_date, self.date[0], self.columns[0], self.date[2], self.columns[2])
        p = [1]
        for i in range(1, len(rt) + 1):
            pi = p[i - 1] * (1 + rt[i - 1])  # from description.pdf
            p.append(pi)
        return pd.Series(p[1:])

    def calculate_currency_performance(self, start_date, end_date) -> pd.Series:
        start_date = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
        end_date = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
        crt = get_crt(start_date, end_date, self.date[1], self.columns[1], self.date[2], self.columns[2])
        cp = [1]
        for i in range(1, len(crt) + 1):
            cpi = cp[i - 1] * (1 + crt[i - 1])  # from description.pdf
            cp.append(cpi[1:])

        return pd.Series(cp)

    def calculate_total_performance(self, start_date, end_date) -> pd.Series:
        start_date = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
        end_date = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
        trt = get_trt(start_date, end_date, self.date[0], self.columns[0], self.date[2],
                      self.columns[2], self.date[1], self.columns[1])
        tp = [1]
        for i in range(1, len(trt) + 1):
            tpi = tp[i - 1] * (1 + trt[i - 1])  # from description.pdf
            tp.append(tpi)
        return pd.Series(tp[1:])


if __name__ == "__main__":
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (15, 5)
    np.seterr(divide='ignore', invalid='ignore')
    a = RockTask()
    print(a.calculate_total_performance('2014-01-21', '2014-02,02'))
