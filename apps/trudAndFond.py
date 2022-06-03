import numpy as np
import streamlit as st
import pandas as pd
import read
import webbrowser

def buildMain():
    st.header("Рассчет коэффициентов прямых и полных затрат труда и фондов и плановую потребность.")
    st.markdown(
        """Рассчитать коэффициенты прямых и полных затрат труда и фондов и плановую потребность в соответствующих ресурсах.""")
    with st.expander("Инструкции по использованию"):
        st.info("""
           В этих инструкциях вы найдете информацию о требованиях к входным файлам для расчета, также вы можете скачать шаблон таблицы.
       """)
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Инструкция"):
                    webbrowser.open_new_tab(
                        "https://docs.google.com/document/d/1GtSvtRwEtLHP98ZprLIr2mA5w6VqKjrZ/edit?usp=sharing&ouid=111050107448852221170&rtpof=true&sd=true")
            with col2:
                if st.button("Шаблон таблицы"):
                    webbrowser.open_new_tab(
                        "https://docs.google.com/spreadsheets/d/1wXDrTJWpt8u1ySvC0c1beAQcRS4g6ROJ/edit?usp=sharing&ouid=111050107448852221170&rtpof=true&sd=true")

    st.markdown("***")

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx'])
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        if read.checkFormat(sheet):
            col_names, itogo_by_row, dob_st, val_price_by_raw, trud, fond = read.readByCol(sheet)
            t, f = [], []
            trudy = list(filter(None, trud))
            fondy = list(filter(None, fond))
            val_price_by_raw = list(filter(None, val_price_by_raw))

            for index in range(len(trudy) - 1):
                t.append(round(trudy[index] / val_price_by_raw[index], 3))
                f.append(round(fondy[index] / val_price_by_raw[index], 3))

            main_matrix = read.readMainMatrix(sheet)
            row_names, itogo_by_col, end_pruducts, val_price = read.readByRow(sheet)
            koef_pryamyx_zatrat = read.koef_prymyx_zatrat(main_matrix, val_price)
            inv_matrix = read.getInverseMatrix(koef_pryamyx_zatrat)
            inv_matrix = np.array(inv_matrix)
            t = np.array(t)

            with st.container():
                left_col, right_col = st.columns(2)
                with left_col:
                    st.subheader("Труды")
                    st.write('''
                                Коэффициенты прямой трудоёмкости $(t_j)$:
                        ''')
                    st.table(pd.DataFrame(t))

                    t = t.dot(inv_matrix)
                    for index in range(len(t)):
                        t[index] = round(t[index], 3)
                    st.write('Таблица полных затрат трудов $(L)$')
                    st.table(pd.DataFrame(t))

                with right_col:
                    st.subheader("Фонд")
                    st.write('''
                                Коэффициенты прямой фондоёмкости $(f_j)$:
                                        ''')
                    st.table(pd.DataFrame(f))

                    st.text("")

                    f = np.array(f)
                    f = f.dot(inv_matrix)
                    for index in range(len(t)):
                        f[index] = round(f[index], 3)
                    st.write('Таблица коэффициентов полных затрат фондов $(Ф)$')
                    st.table(pd.DataFrame(f))
        else:
            st.error("Этот файл не подходит для расчета. Пожалуйста, проверьте шаблон таблицы в описании.")




