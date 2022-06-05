import random
import datetime
import numpy as np

from config import (
    MIN_DAYWORK_TIME,
    MAX_DAYWORK_TIME,
    MAX_CLINICS,
    russian_number_codes
)

def generate_schedule(samples, is_working=True):
    result = []
    if is_working is False:
        return [np.nan for _ in range(samples)]

    for _ in range(samples):
        if random.uniform(0, 1) > .85:
            result.append(np.nan)
            continue

        delta_hours = random.randint(MIN_DAYWORK_TIME, MAX_DAYWORK_TIME)
        delta_minutes = 15 * random.randint(0, 3) if delta_hours < MAX_DAYWORK_TIME else 0

        hours_start = random.randint(8, 10)
        minutes_start = 15 * random.randint(0, 3)
        start = datetime.timedelta(hours=hours_start, minutes=minutes_start)
        end = start + datetime.timedelta(hours=delta_hours, minutes=delta_minutes)
        
        result.append(f'{("0" + str(start))[:-3][-5:]}-{("0" + str(end))[:-3][-5:]}')

    return result

def generate_phone(samples):
    result = []
    for _ in range(samples):
        code = random.choice(russian_number_codes)
        base = "".join([str(random.randint(0, 9)) for x in range(7)])
        result.append(f'+7({code}){base[:3]}-{base[3:5]}-{base[-2:]}')

    return result

def generate_clinics(samples, clinics_from, clinics_to):
    result = []
    for _ in range(samples):
        amount = random.randint(clinics_from, clinics_to)
        clinics = map(str, sorted(random.sample(range(1, MAX_CLINICS + 1), k=amount)))
        result.append(", ".join(clinics))

    return result

def generate_med_license(samples):
    result = []
    for _ in range(samples):
        base = "".join([str(random.randint(0, 9)) for x in range(10)])
        result.append(f'ЛО-{base[:2]}-{base[2:4]}-{base[4:]}')

    return result

def generate_end_term(samples):
    result = []
    for _ in range(samples):
        now = datetime.datetime.now()
        end = now + datetime.timedelta(days=30 * random.randint(1, 12*4))
        result.append(end.strftime('%d.%m.%Y'))
        
    return result
