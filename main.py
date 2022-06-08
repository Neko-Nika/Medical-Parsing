import streamlit as st
import math
import pandas as pd

import parsing
from config import (
    sources,
    output_formats,
    DEFAULT_SAMPLES,
    MIN_SAMPLES,
    MAX_SAMPLES,
    MAX_CLINICS,
    DEFAULT_CLINICS_FROM,
    DEFAULT_CLINICS_TO,
)

if __name__ == "__main__":
    # Sidebar
    st.sidebar.title('Сервис для парсинга данных о врачах')
    st.sidebar.markdown("""---""")

    st.sidebar.subheader('Источник данных')
    source = st.sidebar.radio(
        label='Выберите сайт, с которого будет парситься информация',
        options=sources.keys()
    )

    # specializations parsing
    specializations_list = parsing.parse_specializations()

    # Main screen
    info = {
        'specs': specializations_list, 
        'weekday': [True, True, True, True, True, True, False],
        'clinics_from': DEFAULT_CLINICS_FROM,
        'clinics_to': DEFAULT_CLINICS_TO,
    }

    if st.checkbox('Дополнительная информация'):
        ingore_specializations = st.multiselect(
            label='Выберите какие специализации не нужно добавлять',
            options=[x['spec'] for x in specializations_list]
        )

        st.write('Выберите рабочие дни')
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        col7, _ = st.columns(2)
        with col1:
            monday = st.checkbox('Понедельник', value=True)
        with col2:
            tuesday = st.checkbox('Вторник', value=True)
        with col3:
            wednesday = st.checkbox('Среда', value=True)
        with col4:
            thursday = st.checkbox('Четверг', value=True)
        with col5:
            friday = st.checkbox('Пятница', value=True)
        with col6:
            saturday = st.checkbox('Суббота', value=True)
        with col7:
            sunday = st.checkbox('Воскресенье', value=False)

        from_clinics, to_clinics = st.slider(
            label='Укажите число клиник для каждого врача',
            min_value=1,
            max_value=MAX_CLINICS,
            value=(DEFAULT_CLINICS_FROM, DEFAULT_CLINICS_TO)
        )
        
        # Update info
        info['specs'] = [x for x in specializations_list if x['spec'] not in ingore_specializations]
        info['weekday'] = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        info['clinics_from'] = from_clinics
        info['clinics_to'] = to_clinics

    st.markdown("""---""")
    samples = st.number_input(
        label='Введите желаемое количество записей', 
        value=DEFAULT_SAMPLES,
        min_value=MIN_SAMPLES,
        max_value=MAX_SAMPLES
    )

    output_format = st.selectbox(
        label='Формат файла',
        options=output_formats,
        index=0
    )

    if st.button('Сгенерировать'):
        # Check for validity
        error = None
        if len(info['specs']) < 1:
            error = 'Не выбраны специализации.'
        elif len(set(info['weekday'])) == 1 and list(set(info['weekday']))[0] is False:
            error = 'Не выбраны рабочие дни.'

        if error is None:
            data = parsing.create_doctor_table(info=info, samples=samples, output_format=output_format)
            if output_format == 'csv':
                file = data.to_csv(index=False).encode('windows-1251')
            else:
                writer = pd.ExcelWriter(f'Vrachi.{output_format}', engine='xlsxwriter')
                data.to_excel(writer, encoding='windows-1251', index=False)
                file = open(f'Vrachi.{output_format}', 'rb')
                writer.save()

            with st.expander('Превью'):
                st.write(data)

            st.download_button(
                label='Скачать данные',
                data=file,
                file_name=f'Vrachi.{output_format}',
                mime=f'text/{output_format}'
            )
        else:
            st.error(error)