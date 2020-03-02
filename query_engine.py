import engine
import math
import csv
import sys
import util
import defaultlist
from urllib import parse, request
import hw2


def load_diseases():
    disease_list = list()
    with open('disease_list_final.txt') as f:
        lines = f.readlines()
        for l in lines:
            disease_list.append(l)
    return disease_list


disease_list = load_diseases()
disease_vector = util.load_final_vector()
print(disease_vector[0])


def lookup():
    '''q_to_eq[index of question] = equivalence class indices'''
    q_to_eq = []
    with open('quest.csv') as f:
        read = csv.reader(f, delimiter=',')
        for row in read:
            q_to_eq.append(row[0])
    f.close()
    return q_to_eq


def user_inp(inp):
    '''Converts the string command line argument into normalized weights'''
    inp_list = inp[1:-1].split(',') # Note all elements are STRINGs
    assert (len(inp_list)==29)
    norm_inp = []
    score4 = [0, 0.33333, 0.66666, 1] # scoring scale for 4 options
    score2 = [0, 1] # scoring scale for 2 options
    for n in range(25): # 25 questions with 4 options
        norm_inp.append(score4[int(inp_list[n])])
    for n in range(4):
        norm_inp.append(score2[int(inp_list[25 + n])])
    return norm_inp


def cosine_sim(x, y):
    '''
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    '''
    sum = 0

    for idx, num_x in enumerate(x):
        num_y = y[idx]
        sum+=num_x*num_y
    sqrt_sum_x = 0
    sqrt_sum_y = 0
    for num_x in x:
        sqrt_sum_x += num_x**2
    norm_x = math.sqrt(num_x)
    for num_y in y:
        sqrt_sum_y += num_y**2
    norm_y = math.sqrt(num_y)
    sim = sum/(norm_x*norm_y + 1)
    return sim


def main():
    if len(sys.argv) == 1:
        raise Exception('Missing command line argument(user input). Exitting.')
    inp_arr = sys.argv[1]
    q_eq = lookup() # lookup table
    norm_inp = user_inp(inp_arr)
    res = [x-x for x in range(127)]
    # n = question number
    # q_eq[n] = [equivalence classes corresponding to q n]
    for n in range(29):
        q_eq[n] = q_eq[n].split(',')
        for eq in q_eq[n]: # each eq class corresponding to q n
            if (eq.rstrip() !=''):
                res[int(eq)] += norm_inp[n]
    similarity = list()
    for idx, v in enumerate(disease_vector):
        similarity.append(cosine_sim(v, res))
    val, idx = max((val, idx) for (idx, val) in enumerate(similarity))
    disease_name = disease_list[idx]
    print(disease_name)


if __name__ == '__main__':
    main()
