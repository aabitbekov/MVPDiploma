import streamlit as st
st.set_page_config(
    page_title="MOБ",
    page_icon="⚙️",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://docs.google.com/document/d/1y2W8h1uf3Ked1m4Ez0UbAwxkS9ygWQ1YqQ2oA3Q7clg/edit?usp=sharing',
        'Report a bug': "https://wa.link/99i079",
        'About': "От Научно-производственный центр «Геодезия и картография» для рассчета МОБ!"
    }
)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

import streamlit_authenticator as stauth
import auth.authreader
from multiapp import MultiApp
from apps import main, trudAndFond, balans, landing, methodology


names = auth.authreader.getNames()
usernames = auth.authreader.getUsername()
passwords = auth.authreader.getPass()

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

#
with st.sidebar:
    st.title("Научно-производственный центр «Геодезия и картография»")
    name, authentication_status, username = authenticator.login('Войти в систему', 'main')
if not st.session_state['authentication_status']:
    landing.buildMain()

if st.session_state['authentication_status']:
    app = MultiApp()
    app.add_app("Главная страница", landing.buildMain)
    app.add_app("Методология", methodology.buildMain)
    app.add_app("Подсчет коэффициентов прямых материальных затрат.", main.buildMain)
    app.add_app("Рассчет коэффициентов прямых и полных затрат труда и фондов и плановую потребность.", trudAndFond.buildMain)
    app.add_app("Основное балансовое соотношение", balans.buildMain)
    app.run()
    with st.sidebar:
        st.write("")
        st.write("")
        st.write("----------")
        with open("excelFiles/manual/manual.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Руководство пользователя",
                           data=PDFbyte,
                           file_name="Руководство пользователя.pdf",
                           mime='application/octet-stream')
        st.write("----------")
        authenticator.logout('Выйти из системы', 'main')
elif st.session_state['authentication_status'] == False:
    with st.sidebar:
        st.error('Неверное имя пользователя/пароль')
elif st.session_state['authentication_status'] == None:
    with st.sidebar:
        st.warning('Пожалуйста, введите имя пользователя и пароль')
