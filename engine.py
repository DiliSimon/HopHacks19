import hw2
import util
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from queue import Queue
from bs4 import BeautifulSoup
from string import ascii_lowercase
from urllib import parse, request
from urllib.parse import urlparse
from collections import defaultdict
import json
from datetime import date, datetime


medical_terms = hw2.read_stopwords('medical_terms')
disease_list = hw2.read_stopwords('disease_list')
print(disease_list)
symptom_list = util.load_symptoms()


def renew_data_pubmed():
    disease_to_article_links = defaultdict()
    base = 'https://www.ncbi.nlm.nih.gov/pubmed/'
    for idx, d in enumerate(disease_list):
        print(d)
        link = base + '?term=' + d
        links = get_all_article_links(link)
        disease_to_article_links[d] = links
    return dict(disease_to_article_links)
    # store_csv('disease_pages.csv', disease_pages)


def get_all_article_links_bs(url):
    links = list()
    try:
        html = request.urlopen(url).read()
    except:
        print('cannot open page')
        return []
    soup = BeautifulSoup(html)
    mydivs = soup.findAll("div", {"class": "rslt"})
    for div in mydivs:
        a = div.findChild("p").findChild("a")
        link = a.get_attribute["href"]

        try:
            html_2 = request.urlopen(link).read()
        except:
            print('cannot open page')
            return []
        sp = BeautifulSoup(html_2)
        links.append(sp.find("div", {"class":"icons portlet"}).find("a")["href"])
    return links


# return list of all full text links to the given disease's url
def get_all_article_links(url):
    links = list()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get(url)

    i = 0
    while i < 1:
        i += 1
        xpath = "//div[@class='rslt']/p[@class='title']/a"
        try:
            articles_list = driver.find_elements_by_xpath(xpath)
        except NoSuchElementException as e:
            print(e)
        for a in articles_list:
            p = "//div[contains(@class, 'icons') and contains(@class, 'portlet')]//a"
            '''
            p_test = "//div[contains(@class, 'icons') and contains(@class, 'portlet')]//a/href()"
            page = request.urlopen(a)
            htmlparser = etree.HTMLParser()
            tree = etree.parse(page, htmlparser)
            l = tree.xpath(p)
            links.append(l)
            '''
            driver_2 = webdriver.Chrome('./chromedriver', options=chrome_options)
            try:
                a_link = a.get_attribute('href')
            except StaleElementReferenceException as e:
                print(e)
                continue

            #print(a_link)
            driver_2.get(a_link)
            try:
                links.append(driver_2.find_element_by_xpath(p).get_attribute('href'))
            except NoSuchElementException as e:
                print('Error for: ' + a_link)
                print(e)
                print("\n")
        '''
        try:
            driver.find_element_by_xpath("//a[contains(text(), 'Next >')]").click()
        except NoSuchElementException as e:
            print(e)
            break
        '''
    return links


def renew_data():
    base = 'https://www.cdc.gov/diseasesconditions/az/'
    disease_pages_alpha = []
    disease_pages = []
    for a in ascii_lowercase:
        link = base + a + '.html'
        disease_pages_alpha.append(link)
        res = request.urlopen(link)
        html = res.read()
        soup = BeautifulSoup(html, 'html.parser')
        target = soup.find("div", {"class": "az-content"})
        for link in target.findChildren("a"):
            disease = [link.text, link.get('href')]
            disease_pages.append(disease)
    return disease_pages
    # store_csv('disease_pages.csv', disease_pages)


# create vector according to the first three layer of descriptions
# return the vector representation of a disease given its link
def create_vector(root):
    word_list = util.word_list(root)
    if word_list == 0:
        return 0
    word_list = [x for x in word_list if x != '']
    return compute_term_frequency(word_list)


def create_vector_sum(urls):
    vec = [0]*len(symptom_list)
    i = 0
    for u in urls:
        i += 1
        dic = create_vector(u)
        if dic == 0:
            i -= 1
            continue
        for idx, k in enumerate(dic):
                vec[idx] += dic[idx]
    for idx, v in enumerate(vec):
        vec[idx] = v
    return vec


def create_csv():
    disease_to_article_links = renew_data_pubmed()
    disease_to_vec = defaultdict()

    # vec = create_vector_sum(disease_to_article_links[d])
    # disease_to_vec[d] = vec
    for idx, d in enumerate(disease_to_article_links):
        for l in disease_to_article_links[d]:
            vec = create_vector(l)
            if vec == 0:
                continue
            vec_dict = json.dumps(vec)
            with open('disease_vector.csv', 'a+') as f:
                f.write(d + ',' + vec_dict + '\n')
                f.close()
            '''
            for d in disease_to_vec:
                id += 1
                name = d
                vec = disease_to_vec[d]
                print(name)
                print(vec)
                vec_dict = json.dumps(vec)
            '''
    print('Completed')


def create_database():
    conn = sqlite3.connect('diseases.db')
    c = conn.cursor()
    try:
        c.execute('''DROP TABLE Diseases''')
    except:
        print('CANNOT DROP TABLE')
    c.execute('''CREATE TABLE Diseases(id INTEGER PRIMARY KEY, name TEXT, vec TEXT)''')
    today = date.today()
    disease_to_article_links = renew_data_pubmed()
    disease_to_vec = defaultdict()

    for d in disease_to_article_links:
        vec = create_vector_sum(disease_to_article_links[d])
        disease_to_vec[d] = vec
    print(disease_to_vec)
    id = 0
    for d in disease_to_vec:
        id += 1
        name = d
        vec = disease_to_vec[d]
        print(name)
        print(vec)
        vec_dict = json.dumps(vec)
        try:
            c.execute('''INSERT INTO Diseases(id, name, vec)VALUES (?,?,?)''', (id, name, vec_dict))
        except Exception as e:
            print(e)
            print(name)
            conn.rollback()
    conn.commit()
    conn.close()


def engine(query: str):
    words = util.process_string(query)
    vec = compute_term_frequency(words)
    conn = sqlite3.connect('diseases.db')
    c = conn.cursor()
    c.execute('''SELECT name, vec FROM Diseases''')
    target = defaultdict()
    for row in c:
        name = row[0]
        d_vec = json.loads(row[1])
        sim = hw2.cosine_sim(d_vec, vec)
        target[sim] = name
    idx = 0
    for i in sorted(target.keys(), reverse=True):
        if idx > 10:
            break
        idx += 1
        print(target[i])
        print(i)


# return a list representation of the input word list
# attribute each word to equivalence class
def compute_term_frequency(words):
    vec = [0]*len(symptom_list)
    for w in words:
        for idx, l in enumerate(symptom_list):
            if w in symptom_list[idx]:
                vec[idx] += 1
    return vec


def store_csv(name, data):
    with open(name, 'w') as resultFile:
        for row in data:
            resultFile.write(row[0] + ',' + row[1] + '\n')
        resultFile.close()


def sql_fetch(con):
    cursorObj = con.cursor()

    cursorObj.execute('SELECT name, vec FROM Diseases')

    rows = cursorObj.fetchall()

    for row in rows:
        print(row)


def main():
    create_csv()
    #util.load_symptoms()
    #create_csv()
    #con = sqlite3.connect('diseases.db')
    #sql_fetch(con)
    # engine('Heart')


if __name__ == '__main__':
    main()
