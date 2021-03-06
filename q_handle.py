import csv
import sys
from urllib import parse, request


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


def main():
    if len(sys.argv) == 1:
        raise Exception('Missing command line argument(user input). Exitting.')
    inp_arr = sys.argv[1] 
    q_eq = lookup() # lookup table
    norm_inp = user_inp(inp_arr)
    res = [x-x for x in range(128)]
    # n = question number
    # q_eq[n] = [equivalence classes corresponding to q n]
    for n in range(29):
        q_eq[n] = q_eq[n].split(',')
        for eq in q_eq[n]: # each eq class corresponding to q n
            if (eq.rstrip() !=''):
                res[int(eq)] += norm_inp[n]
    print(res)

if __name__ == '__main__':
    main()
    
