import re
import random
import requests
import datetime


API_KEY = '1a07eb6942168a4236f35a488a4da3ca6dfcc72a'

verses = ["Psalm 42:11", "Psalm 147:3", "Psalm 30:11"]

def get_esv_text(passage):
    API_URL = 'https://api.esv.org/v3/passage/text/'
    params = {
        'q': passage,
        'indent-poetry': False,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': True,
    }

    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)
    passages = response.json()['passages'][0]
    lst = passages.split("\n")

    new = []
    for i in lst:
        if len(i) != 0:
            new.append(i.strip())
    
    ref = new[0]
    verse = new[1:]
    
    return (ref, verse)

def get_random(query):
    API_URL = 'https://api.esv.org/v3/passage/search/'
    params = {
        'q': query,
        'indent-poetry': False,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': True,
    }
    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    initial = requests.get(API_URL, params=params, headers=headers)
    #get random page
    pages = initial.json()['total_pages']
    params['page'] = random.randint(1, pages)


    response = requests.get(API_URL, params=params, headers=headers)
    #get random element that will point to verse
    random_verse = random.randint(0, len(response.json()['results'])-1)

    verse_ref = response.json()['results'][random_verse]['reference']
    verse_cont = response.json()['results'][random_verse]['content']
    
    return (verse_ref, verse_cont)

def txttolist(file):
    f = open(file, "r")
    for line in f:
        line = line.strip()
        print(line)

d = datetime.date.today()
print(d.strftime("%a, %d %b"))
