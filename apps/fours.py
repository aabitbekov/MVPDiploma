import numpy as np
import pandas
import streamlit as st
import pandas as pd

import read
def buildMain():
    st.markdown("""Проследить эффект матричного мультипликатора при дополнительном увеличении конечного продукта по какой-либо отрасли на X %.""")
    otrasl = st.text_input('Введите номер отрасли например: 1')
    procent = st.text_input('Сколько процентов увеличении, Введите процент например: 7')
    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx','csv'])
    if uploaded_file and otrasl and procent:
        st.write('Oтрасль {} на {} процентов в увеличении'.format(otrasl, procent))
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        row_names, itogo_by_col, end_pruducts, val_price = read.readByRow(sheet)
        st.write(round(end_pruducts[int(otrasl) - 1] * float(procent) / 100, 3))
        mat1 = round(end_pruducts[int(otrasl) - 1] * float(procent) / 100, 3)
        main_matrix = read.readMainMatrix(sheet)
        st.write(main_matrix)

        inv_matrix = read.getInverseMatrix(main_matrix)
        st.table(pandas.DataFrame(inv_matrix))

        res = np.dot(mat1, inv_matrix)

        # print resulted matrix
        st.table(pd.DataFrame(res))






def app():
    buildMain()