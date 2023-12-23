import os, configparser
import pandas as pd
from snowflake.snowpark import Session
import streamlit as st

def getFullPath(filename):
    crtdir = os.path.dirname(__file__)
    pardir = os.path.abspath(os.path.join(crtdir, os.pardir))
    return f"{pardir}/{filename}"

# customize with your own Snowflake connection parameters
@st.cache_resource(show_spinner="Connecting to Snowflake...")
def getSession():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
    section = "connections.demo_conn"
    pars = {
        "account": parser.get(section, "accountname"),
        "user": parser.get(section, "username"),
        "password": os.environ['SNOWSQL_PWD']
    }
    return Session.builder.configs(pars).create()

@st.cache_data(show_spinner="Running a Snowflake query...")
def getDataFrame(query):
    conn = getSession()
    rows = conn.sql(query).collect()
    return pd.DataFrame(rows).convert_dtypes()
