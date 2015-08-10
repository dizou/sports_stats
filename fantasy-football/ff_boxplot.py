#!/usr/bin/python

from matplotlib.pyplot import *
import numpy as np
import csv


def is_float(val):
    try:
        float(val)
        return True
    except:
        return False


def turn_into_scatter(non_scatter_data):
    x = []
    y = []
    for index, r in enumerate(non_scatter_data):
        for pt in r:
            x.append(pt)
            y.append(index + 1)
    return x, y

with open('/home/di/Downloads/idp-2014.csv') as idp_csv_file:
    reader = csv.reader(idp_csv_file)
    rows = [row for row in reader][1:]

ordered_player_list = [row[0] for row in rows][::-1]

data = [[float(pts) for pts in row[1:17] if is_float(pts)] for row in rows][::-1]
no_zero_data = [[float(pts) for pts in row[1:17] if is_float(pts) and float(pts) > 0] for row in rows][::-1]

data_dict = {
    'idp-2014-zero.png': data,
    'idp-2014-no-zero.png': no_zero_data
}

for k in data_dict:
    data = data_dict[k]
    means = [np.mean(x) for x in data]
    scatter_data_x, scatter_data_y = turn_into_scatter(data)

    figure()
    boxplot(data, vert=False, labels=ordered_player_list)
    scatter(means, list(range(1,26)))
    #scatter(scatter_data_x, scatter_data_y, marker='.')
    xlim([0,20])
    tight_layout()
    savefig(k)