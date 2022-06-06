from numpy import full
from pyparsing import col
import streamlit as st
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import random
import math

from config import sources, columns, email_source, DOCTORS_PER_PAGE
import generate

@st.cache
def parse_specializations():
    request = requests.get(sources['МОСГОРМЕД'])
    html = BS(request.content, 'html.parser')
    result = []

    items = html.select('.speciality-home-list > .speciality-home-one')
    if len(items) > 0:
        for element in items:
            num_entries = element.select('.speciality-number-home-wrap > span')[0].get_text(strip=True)
            if num_entries == "0":
                continue
            data = element.select('.dotted > a')[0]
            result.append(
                {
                    'spec': data.get_text(strip=True),
                    'href': data['href'],
                    'count': int(num_entries)
                }
            )
    
    return result

def parse_doctors(items, samples):
    data = {'Имя': [], 'Фамилия': [], 'Отчество': [], 'Должность': [], 'Стаж': []}
    while len(data['Имя']) != samples:
        item = items[random.randint(0, len(items) - 1)]

        if item['count'] > DOCTORS_PER_PAGE:
            page = random.randint(1, math.ceil(item['count'] // DOCTORS_PER_PAGE))
        else:
            page = 1
        
        request = requests.get(item['href'] + f'page/{page}')
        html = BS(request.content, 'html.parser')
        element = html.select('div.th-poststwo.th-postslist.taxonomy-speciality > article')
        if len(element) == 0:
            continue
        num_elements = len(element) - 1 if len(element) > 1 else 1
        element = element[random.randint(0, num_elements)]

        fullname = element.select('.zagdoc')[0].get_text(strip=True).split()
        experience = int(element.select('.expicience')[0].get_text(strip=True).split()[1])

        if (
            len(fullname) != 3 or
            fullname[1] in data['Имя'] and 
            fullname[0] in data['Фамилия'] and 
            fullname[2] in data['Отчество'] and 
            experience in data['Стаж']
        ):
            continue
        
        data['Имя'].append(fullname[1])
        data['Фамилия'].append(fullname[0])
        data['Отчество'].append(fullname[2])
        data['Должность'].append(item['spec'])
        data['Стаж'].append(experience)
    
    return data

def parse_emails(samples):
    request = requests.get(email_source)
    html = BS(request.content, 'html.parser')
    result = []

    element = html.select('.entry-content > p')[2]
    for email in element.select('a'):
        result.append(email.get_text(strip=True))

    random.shuffle(result)
    result = list(set(result))
    
    return result[:samples]

def create_doctor_table(info, samples, output_format):
    with st.spinner('Считываем данные докторов...'):
        data = parse_doctors(info['specs'], samples=samples)
    
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    day = 0
    with st.spinner('Генерируем расписание...'):
        for i in info['weekday']:
            data[days[day]] = generate.generate_schedule(samples=samples, is_working=i)
            day += 1

    with st.spinner('Генерируем номера телефонов...'):
        data['Номер телефона'] = generate.generate_phone(samples=samples)

    with st.spinner('Считываем адреса электронных почт...'):
        data['Email'] = parse_emails(samples)

    with st.spinner('Генерируем номера клиник...'):
        data['Клиники'] = generate.generate_clinics(samples, info['clinics_from'], info['clinics_to'])

    with st.spinner('Генерируем номера мед-лицензий...'):
        data['Номер медицинской лицензии'] = generate.generate_med_license(samples)

    with st.spinner('Генерируем сроки действия мед-лицензий...'):
        data['Срок действия'] = generate.generate_end_term(samples)

    data['id[pk]'] = list(range(1, samples + 1))

    table = pd.DataFrame(data, columns=columns)

    return table
