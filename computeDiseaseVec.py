from defaultlist import defaultlist

dlist = []
with open('disease_list') as f:
    for l in f:
        dlist.append(l.strip('\n'))

dNum = defaultlist(int)
with open('disease_vector.csv') as f:
    for l in f:
        dname = l.split('[')[0][:-1]
        indexOfDisease = dlist.index(dname)
        dNum[indexOfDisease] += 1

dveclist = defaultlist(list)
with open('disease_vector.csv') as f:
    for l in f:
        dname = l.split('[')[0][:-1]
        indexOfDisease = dlist.index(dname)
        dveclist[indexOfDisease] = defaultlist(int)
        scorelist = l.split('[')[1].split(',')
        for ind in range(len(scorelist)):
            if ind == len(scorelist)-1:
                scorelist[ind]=scorelist[ind][:-2]
            if not int(scorelist[ind]) == 0:
                dveclist[indexOfDisease][ind] += 1/dNum[indexOfDisease]

print(dveclist)

for ind in range(len(dveclist)):
    if dveclist[ind] == []:
        print(ind)
