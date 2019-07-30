import sys
import datetime
import argparse
import pandas as pd
import numpy as np

from datetime import timedelta

import logger_creator

logger = logger_creator.get_logger(
    logger_name="App Date", filename="app_date.log", stream=sys.stdout
)


def check(a, b):
    return a.day == b.day and a.month == b.month and a.year == b.year


def get_index(arr, d):
    for i in range(len(arr)):
        if check(arr[i], d):
            return i
    return -1


def get_np():
    # ---------__READ_---_.CSV_-----------

    price_csv = pd.read_csv('prices_ref.csv', sep=',', encoding='latin1', parse_dates=['date'], index_col='date')
    ex_csv = pd.read_csv('exchanges_ref.csv', sep=',', encoding='latin1', parse_dates=[0], index_col=0)
    weig_csv = pd.read_csv('weights_ref.csv', sep=',', encoding='latin1', parse_dates=[0], index_col=0)

    logger.info("Read csv successfully in get_np()")

    price_np = price_csv.to_numpy()
    price_np = np.nan_to_num(price_np)

    ex_csv = ex_csv[['CHF', 'EUR']]
    a = [1] * 1513
    a = pd.Series(a)
    a.index = ex_csv.index
    ex_csv = ex_csv.assign(USD1=pd.Series(a))
    ex_csv['EUR1'] = ex_csv['EUR']
    ex_csv['USD2'] = ex_csv['USD1']

    ex_np = ex_csv.to_numpy()
    ex_np = np.nan_to_num(ex_np)

    weig_np = weig_csv.to_numpy()
    weig_np = np.nan_to_num(weig_np)

    return [price_np, ex_np, weig_np]


def get_date_np():

    # ---------__READ_---_.CSV_-----------

    price_csv = pd.read_csv('prices_ref.csv', sep=',', encoding='latin1', parse_dates=['date'], index_col='date')
    ex_csv = pd.read_csv('exchanges_ref.csv', sep=',', encoding='latin1', parse_dates=[0], index_col=0)
    weig_csv = pd.read_csv('weights_ref.csv', sep=',', encoding='latin1', parse_dates=[0], index_col=0)
    logger.info("Read csv successfully in get_date_np()")
    ex_csv = ex_csv[['CHF', 'EUR']]
    a = [1] * 1513
    a = pd.Series(a)
    a.index = ex_csv.index
    ex_csv = ex_csv.assign(USD1=pd.Series(a))
    ex_csv['EUR1'] = ex_csv['EUR']
    ex_csv['USD2'] = ex_csv['USD1']

    price_index = price_csv.index.values
    ex_index = ex_csv.index.values
    weig_index = weig_csv.index.values
    b = pd.to_datetime(price_index)
    pr_date = np.array([])
    for i in b:
        pr_date = np.append(pr_date, i)

    b = pd.to_datetime(ex_index)
    ex_date = np.array([])
    for i in b:
        ex_date = np.append(ex_date, i)

    b = pd.to_datetime(weig_index)
    we_date = np.array([])
    for i in b:
        we_date = np.append(we_date, i)

    return [pr_date, ex_date, we_date]


def get_rt(st, en, pr_date, price_np, we_date, weig_np):
    pl = timedelta(1)

    if st > en:
        # maybe add logger
        st, en = en, st
    ind = get_index(pr_date, st)
    ind_w = get_index(we_date, st)
    rt = []
    while True:

        if ind == -1:
            print("Error with index: date was not found::: " + st.strftime("%Y-%m-%d"))

        if price_np[ind - 1].any() == 0:
            tmp = price_np[ind]
        else:
            tmp = (price_np[ind] - price_np[ind - 1]) / price_np[ind - 1]
        rt.append(sum(weig_np[ind_w] * tmp))

        if check(st, en):
            break
        st += pl
        ind += 1
        ind_w += 1
    logger.info("Get rt successfully in get_rt()")
    return rt


def get_crt(st, en, pr_date, price_np, we_date, weig_np):
    pl = timedelta(1)

    if st > en:
        # maybe add logger
        st, en = en, st
    ind = get_index(pr_date, st)
    ind_w = get_index(we_date, st)
    rt = []
    while True:

        if ind == -1:
            print("Error with index: date was not found:::")

        if price_np[ind - 1].any() == 0:
            tmp = price_np[ind]
        else:
            tmp = (price_np[ind] - price_np[ind - 1]) / price_np[ind - 1]
        rt.append(sum(weig_np[ind_w] * tmp))

        if check(st, en):
            break
        st += pl
        ind += 1
        ind_w += 1
    logger.info("Get crt successfully in get_crt()")
    return rt


def get_trt(st, en, pr_date, price_np, we_date, weig_np, ex_date, ex_np):

    pl = timedelta(1)

    if st > en:
        # maybe add logger
        st, en = en, st
    ind = get_index(pr_date, st)
    ind_w = get_index(we_date, st)
    ind1 = get_index(ex_date, st)
    rt = []
    while True:

        if ind == -1:
            print("Error with index: date was not found")

        if price_np[ind - 1].any() == 0 or ex_np[ind1 - 1].any() == 0:
            tmp = price_np[ind] * ex_np[ind1]
        else:
            tmp = (price_np[ind] * ex_np[ind1] - price_np[ind - 1] * ex_np[ind1 - 1]) / \
                  (price_np[ind - 1] * ex_np[ind1 - 1])
        rt.append(sum(weig_np[ind_w] * tmp))

        if check(st, en):
            break
        st += pl
        ind += 1
        ind1 += 1
        ind_w += 1
    logger.info("Get trt successfully in get_trt()")
    return rt


def addition(name) -> int:
    pl = timedelta(1)
    file = open(name + ".csv", 'r')
    lines = file.readlines()

    cur_date = datetime.date(int(lines[1][:4]), int(lines[1][5:7]),
                             int(lines[1][8:10]))
    # print(cur_date)
    last_ = lines[1].split(',')
    num = len(lines[0].split(','))
    # print(num)
    file2 = open(name + "_ref.csv", "w")
    file2.write(lines[0])
    # print(lines[0])
    file2.write(lines[1])

    for line in lines[2:]:
        sp_line = line.split(',')
        now_date = datetime.date(int(sp_line[0][:4]), int(sp_line[0][5:7]),
                                 int(sp_line[0][8:10]))
        cur_date += pl
        while not check(cur_date, now_date):
            ans = cur_date.strftime("%Y-%m-%d")
            for it in last_[1:]:
                ans += ','
                ans += it
            file2.write(ans)
            cur_date += pl

        last_ = line.split(',')
        ans = cur_date.strftime("%Y-%m-%d")
        for it in last_[1:]:
            ans += ','
            ans += it

        file2.write(ans)
        cur_date = now_date
    file2.close()
    file.close()
    logger.info("Successfully expanded " + name + ".csv into " + name + "_ref.csv")
    return 1


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description='Adding Missed Dates')
        parser.add_argument(
            '--manual',
            type=int,
            help='manual start of adding date in tables'
        )
        args = parser.parse_args()

    except Exception:
        print(sys.exc_info()[1])
