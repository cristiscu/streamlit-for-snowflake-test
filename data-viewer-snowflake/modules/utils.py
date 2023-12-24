import os, configparser
from sys import platform
import pandas as pd
from snowflake.snowpark import Session
import streamlit as st

def isLocal():
    return platform == "win32";

def getFullPath(filename):
    crtdir = os.path.dirname(__file__)
    pardir = os.path.abspath(os.path.join(crtdir, os.pardir))
    return f"{pardir}/{filename}"

# customize with your own Snowflake connection parameters
def getLocalSession():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
    section = "connections.demo_conn"
    return getSession(parser.get(section, "accountname"),
        parser.get(section, "username"),
        os.environ['SNOWSQL_PWD'])

@st.cache_resource(show_spinner="Connecting to Snowflake...", max_entries=10)
def getSession(account, user, password):
    try:
        return Session.builder.configs({
            "account": account,
            "user": user,
            "password": password
        }).create()
    except:
        return None

@st.cache_data(show_spinner="Running a Snowflake query...")
def getDataFrame(session, query):
    rows = session.sql(query).collect()
    return pd.DataFrame(rows).convert_dtypes()
