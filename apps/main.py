import numpy as np
import streamlit as st
import pandas as pd
import webbrowser
import read


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def buildMain():
    st.header("Подсчет коэффициентов прямых материальных затрат.")
    st.markdown("""
    Основным элементом матричной модели является технологический коэффициент, который отражает технологические связи и материальные потребности между производящими и потребляющими отраслями. </br>
    **Коэффициент прямых материальных затрат $(a_{ij})$** показывает, сколько единиц продукции $і$-отрасли непосредственно затрачивается в качестве средств производства на выпуск единицы продукции $j$-отрасли. </br>
    Прямыми материальными затратами называются затраты, обусловленные на последнем этапе производства.""",
                unsafe_allow_html=True)

    st.markdown("***")

    with st.expander("Инструкции по использованию"):
        st.info("""
           В этих инструкциях вы найдете информацию о требованиях к входным файлам для расчета, также вы можете скачать шаблон таблицы.
       """)
        st.markdown('''
             <div class="row-widget stButton" style="margin:20px 0">
               <a href="https://docs.google.com/document/d/1lU4yq6mLy87De1oz7lhG5V7N39NXnZGQ/edit" kind="primary" style="text-decoration: none" class="css-2r05pe edgvbvh9">Инструкция</a>
               <a href="https://docs.google.com/spreadsheets/d/175sgDy6sk2jIboSKH02y1ZxwS6j8GtHc/edit" kind="primary" style="text-decoration: none" class="css-2r05pe edgvbvh9">Шаблон таблицы</a>
             </div>
            ''', unsafe_allow_html=True)
        st.markdown("***")
    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx', 'csv'])
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        if read.checkFormat(sheet):
            main_matrix = read.readMainMatrix(sheet)
            row_names, itogo_by_col, end_pruducts, val_price = read.readByRow(sheet)
            koef_pryamyx_zatrat = read.koef_prymyx_zatrat(main_matrix, val_price)

            st.markdown("***")

            st.write("""Коэффициенты прямых затрат: $a_{ij} = x_{ij} / x_j$ """)
            st.table(pd.DataFrame(koef_pryamyx_zatrat))

            st.write("---")

            st.write("Обратная матрица: $(E-A)-1$")
            inv_matrix = read.getInverseMatrix(koef_pryamyx_zatrat)
            st.table(pd.DataFrame(inv_matrix))
            st.write("---")

            with st.container():
                left_col, right_col = st.columns(2)
                with left_col:
                    st.write('Валовая продукция $x_i$:')
                    filtered_list = list(filter(None, end_pruducts))
                    del filtered_list[-1]
                    matrixX = np.dot(inv_matrix, filtered_list)
                    st.table(pd.DataFrame(matrixX))

                with right_col:
                    st.write("Величина условно чистой продукции $Z_i$")
                    sum = np.sum(main_matrix, axis=0)
                    res = []
                    for i in range(len(matrixX)):
                        var = round(matrixX[i] - sum[i], 2)
                        res.append(var)
                    st.table(pd.DataFrame(res))
                import xlsxwriter
                from io import BytesIO

                output = BytesIO()

                # Write files to in-memory strings using BytesIO
                # See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
                workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                worksheet = workbook.add_worksheet()

                # db.createDoc(inputdocument='streamlitapp/excelFiles/{}'.format(uploaded_file.name), infunc=1)
                row = 0
                for col, data in enumerate(koef_pryamyx_zatrat):
                    worksheet.write_column(row, col, data)
                workbook.close()
                st.download_button(
                    label="Скачать таблицу",
                    data=output.getvalue(),
                    file_name="Прямые Затраты.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            st.error("Этот файл не подходит для расчета. Пожалуйста, проверьте шаблон таблицы в описании.")

