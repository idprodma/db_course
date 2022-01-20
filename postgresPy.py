import psycopg2
import random
import datetime
import json
from bs4 import BeautifulSoup as bs
import requests
import re

def create_connection():
    with open("credentials.json", "r") as credentials_file:
        credentials = json.load(credentials_file)
    
    conn = psycopg2.connect(dbname='cynologist_club', user=credentials['user'],
                            password=credentials['password'], host='localhost')
    return conn

tel_numbers = []
def generate_telnum():
    telnum = '8'
    while len(telnum) < 11:
        telnum = telnum + str(random.randint(0,9))
    if telnum not in tel_numbers:
        tel_numbers.append(telnum)
        return telnum
    else:
        return generate_telnum()

def generate_name(sex):
    if sex == 0:
        return random.choice(all_male_names)
    else:
        return random.choice(all_female_names)

def generate_surname(sex):
    if sex == 0:
        return random.choice(all_surnames)
    else:
        return random.choice(all_surnames) + 'а'

def generate_full_name():
    sex = random.randint(0, 1)
    name = generate_name(sex)
    surname = generate_surname(sex)
    return name + ' ' + surname

def generate_street():
    return random.choice(all_streets)

def generate_house_num():
    return random.randint(1, 100)

def generate_address():
    return generate_street() + ', ' + str(generate_house_num())

def get_streets():
    streets = []
    url = 'https://ru.wikipedia.org/wiki/Список_улиц_Москвы'
    soup = bs(requests.get(url).text, 'html.parser')
    litera_divs = soup.find_all('div', {'class': 'columns'})
    for div in litera_divs:
        street_uls = div.find_all('ul')
        for street_ul in street_uls:
            street_lis = street_ul.find_all('li')
            for street_li in street_lis:
                street = street_li.find('a', href=True)
                if street is not None:
                    street_str = street_li.find('a', href=True).get_text()
                else:
                    street_str = street_li.get_text()
                streets.append(street_str)
    return streets

def get_male_names():
    url = 'https://ru.wikipedia.org/wiki/Категория:Русские_мужские_имена'
    soup = bs(requests.get(url).text, 'html.parser')
    litera_groups = soup.find('div', {'class': 'mw-category'}).find_all('div', {'class': 'mw-category-group'})
    male_names = []
    for litera_group in litera_groups:
        litera_names = litera_group.find_all('a')
        for name in litera_names:
            male_names.append(name.get('title')
                                  .replace(' (имя)', '')
                                  .replace(' (значения)', ''))
    return male_names

def get_female_names():
    url = 'https://ru.wikipedia.org/wiki/Категория:Русские_женские_имена'
    soup = bs(requests.get(url).text, 'html.parser')
    litera_groups = soup.find('div', {'class': 'mw-category'}).find_all('div', {'class': 'mw-category-group'})
    female_names = []
    for litera_group in litera_groups:
        litera_names = litera_group.find_all('a')
        for name in litera_names:
            female_names.append(name.get('title')
                                    .replace(' (имя)', '')
                                    .replace(' (значения)', '')
                                    .replace(' (женское имя)', ''))
    return female_names

def get_surnames():
    url = 'https://ru.wikipedia.org/wiki/Список_общерусских_фамилий'
    soup = bs(requests.get(url).text, 'html.parser')
    surnames = []
    surname_lis = soup.find('div', {'class': 'columns'}).find_all('li')
    for surname_li in surname_lis:
        surnames.append(surname_li.find('a').get_text())
    return surnames

def get_breed_groups():
    url = 'http://rkf.org.ru/plemennaja-dejatelnost/'
    soup = bs(requests.get(url).text, 'html.parser')
    breed_groups_div = soup.find('div', {'class': 'flex-line'}).find('div')
    group_links = breed_groups_div.find_all('a')
    breed_groups = []
    for link in group_links:
        tmp_url = link.get('href')
        tmp_url = tmp_url.replace('/standarty-porod', '')
        tmp_url = tmp_url.replace('/plemennaja-dejatelnost', '')
        get_breed_group_info(tmp_url, breed_groups)
    breed_groups.append({'group_name': 'Таксы', 'breed_names': ['Такса']})
    return breed_groups

def get_breed_group_info(url: str, breed_groups):
    url = 'http://rkf.org.ru/plemennaja-dejatelnost' + url
    soup = bs(requests.get(url).text, 'html.parser')
    group_name = re.search('— (.+?)$', soup.find('h2').get_text()).group(1)
    breed_names_parse = soup.find_all('div', {'class': 'fusion-toggle-heading'})
    breed_names = []
    for breed in breed_names_parse:
        breed_names.append(re.search('^(.+?)\s?(№|\().*', breed.get_text()).group(1))
    breed_groups.append({'group_name': group_name, 'breed_names': breed_names})

def get_dog_male_names():
    dog_male_names = []
    url = 'https://magizoo.ru/nicknames/klichki-dlya-sobak-malchiki/'
    soup = bs(requests.get(url).text, 'html.parser')
    name_divs = soup.find_all('div', {'class': 'namesBlock__names__item'})
    for name_div in name_divs:
        name = re.search('(\S+)\s?', name_div.get_text()).group(1)
        dog_male_names.append(name)
    return dog_male_names

def get_dog_female_names():
    dog_female_names = []
    url = 'https://magizoo.ru/nicknames/klichki-dlya-sobak-devochek/'
    soup = bs(requests.get(url).text, 'html.parser')
    name_divs = soup.find_all('div', {'class': 'namesBlock__names__item'})
    for name_div in name_divs:
        name = re.search('([\w\/]+)\.?|\s?', name_div.get_text()).group(1)
        dog_female_names.append(name)
    return dog_female_names

def generate_dog_name(sex):
    if sex == 0:
        return random.choice(all_dog_male_names)
    else:
        return random.choice(all_dog_female_names)

def generate_date(birthdate = None):
    start_date = datetime.date(2005, 1, 1)
    today = datetime.datetime.today().date()
    time_between_dates = today - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    if birthdate is None or (birthdate is not None and birthdate < random_date):
        return random_date
    elif (birthdate is not None and birthdate >= random_date):
        return generate_date(birthdate)

def fill_dog_breeds_table():
    conn = create_connection()
    cursor = conn.cursor()
    dog_breeds = get_breed_groups()
    cnt = 1
    query = 'insert into dog_breeds (breed_group, breed_name, breed_id) values (\'%s\', \'%s\', %s);'
    for group in dog_breeds:
        for breed_name in group['breed_names']:
            cursor.execute(query % (group['group_name'], breed_name, cnt))
            cnt += 1
    conn.commit()
    cursor.close()
    conn.close()

def fill_owners_table():
    conn = create_connection()
    cursor = conn.cursor()
    query_has_telnum = 'insert into owners (id, full_name, address, telnum) values (%s, \'%s\', \'%s\', \'%s\');'
    query_no_telnum = 'insert into owners (id, full_name, address) values (%s, \'%s\', \'%s\');'
    for cnt in range(1, 51):
        full_name = generate_full_name()
        address = generate_address()
        has_telnum = random.randint(0, 100)
        if has_telnum > 40:
            telnum = generate_telnum()
            cursor.execute(query_has_telnum % (cnt, full_name, address, telnum))
        else:
            cursor.execute(query_no_telnum % (cnt, full_name, address))
    conn.commit()
    cursor.close()
    conn.close()

def fill_dogs_and_prizes_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('select count(*) from dog_breeds;')
    all_breeds_count = cursor.fetchone()[0]
    query_deathdate = ('insert into dogs (id, name, owner_id, birthdate, sex, breed, deathdate) ' +
                       'values(%s, \'%s\', %s, \'%s\', \'%s\', %s, \'%s\');')
    query_no_deathdate = ('insert into dogs (id, name, owner_id, birthdate, sex, breed) ' +
                         'values(%s, \'%s\', %s, \'%s\', \'%s\', %s);')
    query_prize = 'insert into prizes values(%s, \'%s\', \'%s\');'
    for cnt in range(1, 61):
        sex = random.choice(['м', 'ж'])
        if sex == 'м':
            name = generate_dog_name(0)
        else:
            name = generate_dog_name(1)
        owner_id = random.randint(1, 50)
        birthdate = generate_date()
        breed = random.randint(1, all_breeds_count)
        if random.randint(0, 1) == 0:
            deathdate = generate_date(birthdate)
            cursor.execute(query_deathdate
                           % (cnt, name, owner_id, birthdate, sex, breed, deathdate))
        else:
            cursor.execute(query_no_deathdate
                           % (cnt, name, owner_id, birthdate, sex, breed))
            prizedate = generate_date(birthdate)
            cursor.execute(query_prize % (cnt, random.choice(prizes), prizedate))
    conn.commit()
    cursor.close()
    conn.close()

def clear_tables():
    conn = create_connection()
    cursor = conn.cursor()
    for table in ['prizes', 'dogs', 'owners', 'dog_breeds']:
        cursor.execute('delete from %s;' % table)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unused_owners():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('delete from owners where id not in (select owner_id from dogs);')
    conn.commit()
    cursor.close()
    conn.close()

all_male_names = get_male_names()
all_female_names = get_female_names()
all_streets = get_streets()
all_surnames = get_surnames()
all_dog_male_names = get_dog_male_names()
all_dog_female_names = get_dog_female_names()
prizes = ['ЧК', 'КЧК', 'ЮКЧК', 'СС', 'ЛПП']

if __name__ == '__main__':
    clear_tables()
    fill_dog_breeds_table()
    fill_owners_table()
    fill_dogs_and_prizes_tables()
    delete_unused_owners()
    pass
