import sys
import datetime
import argparse

from datetime import timedelta


def check(a, b):
    return a.day == b.day and a.month == b.month and a.year == b.year


def addition(file, name):
    pl = timedelta(1)
    lines = file.readlines()

    cur_date = datetime.date(int(lines[1][:4]), int(lines[1][5:7]),
                             int(lines[1][8:10]))
    print(cur_date)
    last_ = lines[1].split(',')
    num = len(lines[0].split(','))
    print(num)
    file2 = open(name + "_ref.csv", "w")
    file2.write(lines[0])
    print(lines[0])
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


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description='Adding Missed Dates')
        parser.add_argument('name', type=str, help='Name of the Table Without .csv')

        args = parser.parse_args()
        _file = open(args.name + ".csv", 'r')
        # content = _file.readline()

        addition(_file, args.name)

    except Exception:
        print(sys.exc_info()[1])
