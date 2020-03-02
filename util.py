import urllib
import re, string
import hw2
from urllib import parse, request
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')


def process_string(sent):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    stopwords = hw2.read_stopwords('common_words')
    words = sent.split(' ')
    final = []
    for w in words:
        w = w.lower()
        if w != '' and (w not in stopwords) and (regex.search(w) is None):
            f = re.sub(r'[^\w\s]', '', w)
            final.append(stemmer.stem(f))
    print(final)
    return final


def word_list(link):
    stopwords = hw2.read_stopwords('common_words')
    symptoms = hw2.read_stopwords('symptoms')
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    url = link
    try:
        html = request.urlopen(url).read()
    except:
        print('cannot open page')
        return 0
    soup = BeautifulSoup(html, features="html5lib")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    word = []
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    for line in lines:
        li = line.split(' ')
        for w in li:
            w = w.lower()
            if w != '' and (w not in stopwords) and (regex.search(w) is None and (w != 'cdc')):
                f = re.sub(r'[^\w\s]', '', w)
                final = stemmer.stem(f)
                word.append(final)
    return word


def load_final_vector():
    disease_vec = list()
    with open('disease_vector_list.txt', 'r') as f:
        lines = f.readlines()
        for l in lines:
            vec = list()
            l = l.rstrip('\n')
            l = l[1:]
            l = l[:-1]
            l.replace(' ', '')
            for n in l.split(','):
                vec.append(float(n))
            disease_vec.append(vec)
    return disease_vec


def load_symptoms():
    symptom_list = list()
    with open('sym.csv') as f:
        lines = f.readlines()
        for l in lines:
            temp = list()
            l = l.split(',')
            for ll in l:
                if ll.rstrip() != '':
                    temp.append(stemmer.stem(ll))
            symptom_list.append(temp)
    return symptom_list


def extract_medical_terms():
    stopwords = hw2.read_stopwords('common_words')
    diseases = hw2.read_stopwords('diseases')
    html = request.urlopen('https://en.wikipedia.org/wiki/List_of_medical_symptoms').read()
    soup = BeautifulSoup(html)
    word = []
    for t in soup.find_all('li'):
        for w in t.text.split(' '):
            if w.lower() not in stopwords and ('(' not in w.lower()) and ("/" not in w.lower())\
                    and ("(" not in w.lower()) and (w in diseases):
                f = re.sub(r'[^\w\s]', '', w.lower())
                final = stemmer.stem(f)
                word.append(final)

    with open('medical_terms', 'w', encoding='utf-8') as f:
        for item in word:
            f.write("%s\n" % item)


def load_disease_vector():
    vec = defaultdict()
    with open('disease_vector.csv', 'r') as f:
        lines = f.readlines()
        for l in lines:
            temp = l.split(',', 1)


if __name__ == '__main__':
    print(load_final_vector())


