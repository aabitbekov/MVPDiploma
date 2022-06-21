import streamlit as st
import requests
from streamlit_lottie import st_lottie


def load_lottieUrl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


animation = load_lottieUrl("https://assets4.lottiefiles.com/packages/lf20_u8jppxsl.json")
about_gif = load_lottieUrl("https://assets10.lottiefiles.com/packages/lf20_wzrthmvn.json")
contact_gif = load_lottieUrl("https://assets5.lottiefiles.com/packages/lf20_uyxm6s2e.json")


def buildMain():

    with st.container():
        # fir diploma
        # st.subheader("Добро пожаловать на веб-сайт")
        left_col, right_col = st.columns(2)

        with left_col:
            # for product
            st.header("Информационная система для составления динамических моделей межотраслевого баланса с применением метода экономической кибернетики")
            # for diploma
            # st.title("Научно-производственный центр «Геодезия и картография")
            # st.write(
            #     "«Геодезия и картография» качественная подготовка специалистов в области геодезии и картографии, научно- исследовательских институтов, производственных организации, национальных и региональных земельных комитетов для получения измерительной пространственной информации о поверхности Земли, ее недрах, объектах поверхности Земли или отдельных ее территорий на планах и картах")
        with right_col:
            st_lottie(animation, height=350, key="animation")

    st.write("---")

    # "about us" block
    with st.container():
        st.header("О нас")
        left_col, right_col = st.columns(2)

        with left_col:
            st_lottie(about_gif, height=300, key="about_gif")

        with right_col:
            st.write("##")
            # for diploma
            # st.write(
            #     "Мы применяем инновационные технологические решения, чтобы улучшить условия обслуживания пользователей, способствуем обеспечению сохранности и востребованности материалов фонда. Вся наша команда ориентирована на информатизацию экономики и общества, предоставление и распространение пространственных данных!Реорганизация в установленном законодательством порядке РГП «Казгеодезия» и «Национальный картографо-геодезический фонд», находящиеся в ведении комитета геодезии и картографии министерства цифрового развития, инноваций и аэрокосмической промышленности РК, путем слияния и преобразования в РГП на ПХВ «Национальный центр геодезии и пространственной информации» комитета геодезии и картографии министерства цифрового развития, инноваций и аэрокосмической промышленности РК.")
            # for produc
            st.write("Web-приложение обеспечивает автоматизацию составления динамических моделей межотраслевого баланса. Созданная  веб-страница обеспечивает выдачу отчетов составленных таблиц прямых и полных затрат и проверку основных макроэкономических показателей состояния равновесия различных отраслей экономики на определенный период.")
            st.write("Разработано специалистами «Astana IT University» в рамках реализации программно-целевого финансирования НТП BR10764919 МСХ РК «Исследование влияния государственной политики в отрасли сельского хозяйства на развитие кооперационных процессов в АПК, устойчивого развития сельских территорий и обеспечения продовольственной безопасности» на 2021-2023 годы")
            st.write("---")

    with st.container():
        left_col, right_col = st.columns(2)

        with left_col:
            st.header("Контакты:")
            st.text("Тел: + 7 (771) 536 96 15")
            st.text("e-mail: oalipbeki@gmail.com")
            st.text("Адрес:  Нур-Султан, пр. Бейбітшілік 73 (пересечение ул. Ә.Молдагуловой), каб. 6212")
            st.text("Время работы:  с понедельника по пятницу с 8:45 по 18:00")

        with right_col:
            st_lottie(contact_gif, height=250, key="contact_gif")


