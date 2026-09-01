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



wynik = get_book_details("/works/OL1168083W")
surowe_subjects = wynik['subjects']
wyczyszczone = clean_subjects(surowe_subjects)
print(len(surowe_subjects))
print(len(wyczyszczone))
print(wyczyszczone)