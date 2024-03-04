import random
import requests

#main functions
API_KEY = ''

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
    if len(response.json()['passages']) == 0:
        return "404"
    passages = response.json()['passages'][0]
    prev_verse = response.json()['passage_meta'][0]['prev_verse']
    next_verse = response.json()['passage_meta'][0]['next_verse']
    
    lst = passages.split("\n")
    new = []
    for i in lst:
        if len(i) != 0:
            new.append(i.strip())
    
    ref = new[0]
    verse = new[1:]

    return (ref, verse, prev_verse, next_verse)

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
    if len(initial.json()['results']) == 0:
        return "404"
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
    lst = []
    for line in f:
        line = line.strip()
        if line not in lst:
            lst.append(line)

    f.close()
    return lst
