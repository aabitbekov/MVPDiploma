import sqlite3
from datetime import datetime, date
from sqlite3 import Connection
import streamlit as st

URI_SQLITE_DB = "/Users/abitbekov/PycharmProject/DiplomaAdminPanel/db.sqlite3"
PRIAMYEZATRATY = 'koefzatrat'
TRUDANDFOND = 'trudfond'
BALANS = 'balans'

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)


def getConn():
    conn = get_connection(URI_SQLITE_DB)
    return conn


# insert into mainapp_document (id, description, document, uploaded_at, func)
# values ();

def createDoc(inputdocument, infunc):

    if infunc == 1:
        infunc = PRIAMYEZATRATY
    if infunc == 2:
        infunc = TRUDANDFOND
    if infunc == 3:
        infunc = BALANS
    inputdescription = 'some'
    insert = "insert into mainapp_document(description, document, uploaded_at, func) values ('{}', '{}', '{}', '{}')".format(inputdescription, inputdocument, date.today(), infunc)
    conn = getConn()
    conn.execute(insert)
    conn.commit()



