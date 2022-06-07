DEFAULT_SAMPLES = 10
MIN_SAMPLES = 1
MAX_SAMPLES = 100
MAX_CLINICS = 20
DEFAULT_CLINICS_FROM = 3
DEFAULT_CLINICS_TO = 5
DOCTORS_PER_PAGE = 15
MIN_DAYWORK_TIME = 5
MAX_DAYWORK_TIME = 8

sources = {
    'МОСГОРМЕД': 'https://mosgormed.ru/#vrachi',
    #'СТОП-ЛИСТ.ИНФО': 'http://stop-list.info/baza/poisk_vracha_po_vsej_rossii_baza_dannykh_vrachej_s_foto/2020-02-12-1569'
}

output_formats = ['xls', 'xlsx', 'csv']
columns = [
    'id[pk]',
    'Имя', 'Фамилия', 'Отчество', 'Должность',
    'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс',
    'Номер телефона', 'Email', 'Клиники',
    'Номер медицинской лицензии', 'Срок действия', 'Стаж'
]
russian_number_codes = [
    '910', '915', '916', '917', '919', '920', '985', '986', '995', '996', '999'
]
email_source = 'https://lavrynenko.com/spisok-poddelnyx-email-adresov-generator/'