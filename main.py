import requests


def clean_subjects(subjects_list):
    cleaned = []
    for tag in subjects_list:
        slowa = tag.split()
        zawiera_cyfre = False
        for znak in tag:
            if znak.isdigit():
                zawiera_cyfre = True
        if len(slowa) <= 4 and zawiera_cyfre == False:
            cleaned.append(tag)
    return cleaned[:15]


def get_book_details(work_key):
    url2 = f"https://openlibrary.org{work_key}.json"
    response2 = requests.get(url2)
    data2 = response2.json()
    return {
        'title': data2.get('title'),
        'subjects': data2.get('subjects'),
        'description': data2.get('description')
    }

def search_books(query, limit=5):
    url = f"https://openlibrary.org/search.json?q={query}"
    response = requests.get(url)
    data = response.json()
    all_docs = data['docs']
    top_docs = all_docs[:limit]
    results = []
    for doc in top_docs:
        work_key = doc.get('key')
        dork = get_book_details(work_key)
        results.append(dork)
    return results





wynik = get_book_details("/works/OL1168083W")
surowe_subjects = wynik['subjects']
wyczyszczone = clean_subjects(surowe_subjects)
search_books("dune", 3),
print(len(surowe_subjects))
print(len(wyczyszczone))
print(wyczyszczone)