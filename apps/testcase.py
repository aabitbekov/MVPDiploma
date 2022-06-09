import pandas as pd
import streamlit as st
from streamlit import StreamlitAPIException

import read


def buildMain():
    st.write("Description page")

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx','csv'])
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        main_matrix, end_pruducts = read.readBigMainMatrix(sheet)
        error = False
        try:
            st.table(pd.DataFrame(main_matrix))
        except StreamlitAPIException:
            error = True
            st.error("Type error")
        if not error:
            itogo_by_row , itogo_by_col = [], []
            for matrix in main_matrix:
                sum_by_row = 0
                for value in matrix:
                    sum_by_row += value
                itogo_by_row.append(sum_by_row)
            # print(len(itogo_by_row))
            itogo_by_col = [0] * len(itogo_by_row)
            for matrix in main_matrix:
                index = 0
                for value in matrix:
                    itogo_by_col[index] += value
                    index += 1
            st.write("Itogo by raw")
            st.table(pd.DataFrame(itogo_by_row))
            st.write("Itogo by col")
            st.table(pd.DataFrame(itogo_by_col))
            st.write("end Product")
            st.table(pd.DataFrame(end_pruducts))

            val_price = []
            for i in range(len(end_pruducts)):
                value = end_pruducts[i] + itogo_by_row[i]
                val_price.append(value)
            # st.write("Val Price")
            # st.table(pd.DataFrame(val_price))

            dob_st = []
            val_price_by_col =[]
            for i in range(len(val_price)):
                dob_st.append(val_price[i] - itogo_by_col[i])
                val_price_by_col.append(dob_st[i] + itogo_by_col[i])

            st.write("Dob St")
            st.table(pd.DataFrame(dob_st))
            st.write("Val Price By Col")
            st.table(pd.DataFrame(val_price_by_col))

            st.write("Сумма Доб Ст {} и сумма {}".format(sum(dob_st), sum(end_pruducts)))
            st.write("Сумма вал ст строки {} и сумма вал ст калонок {}".format(sum(val_price), sum(val_price_by_col)))
            if sum(dob_st) == sum(end_pruducts) and sum(val_price) == sum(val_price_by_col):
                st.write("Balans have! URA")
            else:
                st.write("Balans have't! no URA")