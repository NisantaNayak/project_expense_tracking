import json
from operator import index

import streamlit as st
import  requests
import pandas as pd
import matplotlib.pyplot as plt
API_URL = "http://127.0.0.1:8000/"

def analytics_by_month_tab():
    response = requests.get(f"{API_URL}/analytics_by_month")
    data = response.json()
    df = pd.DataFrame.from_dict(data, orient='index').reset_index()
    df.columns = ['Month_Year', 'Total']
    st.title("Expense Breakdown by Month")
    st.bar_chart(data=df.set_index(["Month_Year"]), width=0, height=0, use_container_width=True)
    st.table(df)
