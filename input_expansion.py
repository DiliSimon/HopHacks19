import numpy as np
import matplotlib.pyplot as plt


def load_disease_vector():
    diseases = list()
    with open("svdresult25.txt", 'r') as f:
        lines = f.readlines()
        for l in lines:
            l = l[1:-2]
            l = l.replace(" ","")
            temp = l.split(',')
            diseases.append(temp)
    return diseases


def load_user_vector():
    diseases = list()
    with open("simon25.txt", 'r') as f:
        lines = f.readlines()
        for l in lines:
            l = l[1:-2]
            l = l.replace(" ","")
            temp = l.split(',')
            diseases.append(temp)
    return diseases


def improve_user_vector(x):
    dv = load_svd_vector()
    np_ve = np.array(dv)
    median = np.median(dv, axis=1)
    twentyfifth = np.percentile(dv, 25, axis=1)
    seventyfifth = np.percentile(dv, 75, axis=1)
    for idx, val in enumerate(x):
        if val == 0:
            x[idx] = twentyfifth[idx]
        if (val > 0.3 and val < 0.4):
            x[idx] = median[idx]
        if (val > 0.4):
            x[idx] = seventyfifth[idx]
    return x


def load_svd_vector():
    final = []
    with open('simon25.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line[1:]
            line = line[:-2]
            line = line.split(', ')
            temp = []
            for l in line:
                temp.append(float(l))
            final.append(temp)
    return final


if __name__ == '__main__':
    improve_user_vector()



