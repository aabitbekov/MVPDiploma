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
        st.subheader("Добро пожаловать на веб-сайт")
        left_col, right_col = st.columns(2)

        with left_col:
            st.title("Научно-производственный центр «Геодезия и картография»")
            st.write(
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")

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
            st.write(
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")

    st.write("---")

    with st.container():
        left_col, right_col = st.columns(2)

        with left_col:
            st.header("Контакты:")
            st.text("Тел: 87081053795, 87272208008")
            st.text("e-mail: npc_gc@mail.ru")

        with right_col:
            st_lottie(contact_gif, height=250, key="contact_gif")


