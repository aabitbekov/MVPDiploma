import streamlit as st
import read
import webbrowser


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def buildMain():
    st.header("Проверить основное балансовое соотношение")
    st.write("Проверим основное балансовое соотношение по формуле основного балансового соотношения $∑{y{\sub i}} = ∑{z{\sub j}}$")
    st.write("""Применение межотраслевого баланса для анализа экономического показателя труда.
Различные модификации рассмотренной выше модели межотраслевого баланса производства и распределения продукции в народном хозяйстве позволяют расширить круг показателей, охватываемых моделью
    """)

    with st.expander("Инструкции по использованию"):
        st.info("""
              В этих инструкциях вы найдете информацию о требованиях к входным файлам для расчета, также вы можете скачать шаблон таблицы.
          """)
        st.markdown('''
                  <div class="row-widget stButton" style="margin:20px 0">
                    <a href="https://docs.google.com/document/d/1lU4yq6mLy87De1oz7lhG5V7N39NXnZGQ/edit" kind="primary" style="text-decoration: none" class="css-2r05pe edgvbvh9">Инструкция</a>
                  </div>
                 ''', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx'])

    if uploaded_file:

        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)

        if not read.checkFormatBalans(sheet):
            main_matrix, end_pruducts = read.readBigMainMatrix(sheet)
            itogo_by_row, itogo_by_col = [], []
            for matrix in main_matrix:
                sum_by_row = 0
                for value in matrix:
                    sum_by_row += value
                    itogo_by_row.append(sum_by_row)
            itogo_by_col = [0] * len(itogo_by_row)
            for matrix in main_matrix:
                index = 0
                for value in matrix:
                    itogo_by_col[index] += value
                    index += 1

            val_price = []
            for i in range(len(end_pruducts)):
                value = end_pruducts[i] + itogo_by_row[i]
                val_price.append(value)

            dob_st = []
            val_price_by_col = []
            for i in range(len(val_price)):
                dob_st.append(val_price[i] - itogo_by_col[i])
                val_price_by_col.append(dob_st[i] + itogo_by_col[i])

            st.write("- Сумма 'Добавленная стоимость' = {}".format(sum(dob_st)))
            st.write("- Сумма 'Конечная продукция' = {}".format(sum(end_pruducts)))
            if sum(dob_st) == sum(end_pruducts):
                st.info("**Баланс сохранен**: Сумма 'Добавленная стоимость' = Сумма 'Конечная продукция'")

            st.write("- Сумма Валовая продукция (по горизонтали) = {}".format(sum(val_price)))
            st.write("- Сумма Валовая продукция (по вертикале) = {}".format(sum(val_price_by_col)))
            if sum(val_price) == sum(val_price_by_col):
                st.info(
                    "**Баланс сохранен**: Сумма Валовая продукция (по горизонтали) = Сумма Валовая продукция (по вертикале)")

            st.write("--------")
            st.warning('Проверим основное балансовое соотношение по формуле основного балансового соотношения $∑{y{\sub i}} = ∑{z{\sub j}}$')
            st.write("--------")
            if sum(dob_st) == sum(end_pruducts) and sum(val_price) == sum(val_price_by_col):
                st.success("**Баланс сохранен**")
            else:
                st.warning("Баланс не сохранен")

            count = 0
            for matrix in main_matrix:
                matrix.append(itogo_by_row[count])
                matrix.append(end_pruducts[count])
                matrix.append(val_price[count])
                count += 1
            main_matrix.append(itogo_by_col)
            main_matrix.append(dob_st)
            main_matrix.append(val_price_by_col)

            import xlsxwriter
            from io import BytesIO

            output = BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            row = 0
            for col, data in enumerate(main_matrix):
                worksheet.write_column(row, col, data)
            workbook.close()

            st.download_button(
                label="Скачать таблицу",
                data=output.getvalue(),
                file_name="workbook.xlsx",
                mime="application/vnd.ms-excel"
            )

        else:
            st.error("Этот файл не подходит для расчета. Пожалуйста, проверьте шаблон таблицы в описании.")


