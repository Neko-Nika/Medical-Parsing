import streamlit as st

if __name__ == "__main__":
    # Sidebar
    st.sidebar.title('Сервис для парсинга данных о врачах')
    st.sidebar.markdown("""---""")

    st.sidebar.subheader('Источник данных')
    source = st.sidebar.radio(
        label='Выберите сайт, с которого будет парситься информация',
    )

    samples = st.number_input(
        label='Введите желаемое количество записей', 
        value=10,
        min_value=1,
        max_value=100
    )
