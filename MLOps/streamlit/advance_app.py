import time
import streamlit as st
import pandas as pd 
import numpy as np
import duckdb

duckdb_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haWNoaWtodW9uZzE5OThAZ21haWwuY29tIiwic2Vzc2lvbiI6Im1haWNoaWtodW9uZzE5OTguZ21haWwuY29tIiwicGF0IjoiZ3BKSDA2WHNsalBPWlo1dlRlU09KWlhzQ25Vd1ZnTVFiNWxtOWZXSDVLbyIsInVzZXJJZCI6IjJiOTgzYTE2LWNkZjMtNDg4NC04NWQ2LWU3OGNmMmFjMzIwOSIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc1Mzg5MjY4MCwiZXhwIjoxNzg1NDI4NjgwfQ.9RXTzfq1HCnCWPWcqwSkYh9PAUd52-UPTrn2c2aFyHM"

con = duckdb.connect(f"md:sample_data?motherduck_token={duckdb_token}")

# Title of the app
st.title("🔍 DuckDB Explorer")

add_selectbox = st.sidebar.selectbox(
    'How would you like to be connected?', 
    ('Email', 'Home phone', 'Mobile phone')
)

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=['x', 'y'])

st.header('Chose a datapoint color')
color = st.color_picker('Color', '#FF0000')
st.divider()
st.scatter_chart(st.session_state.df, x = 'x', y = 'y', color=color)

# Run a query
query = "SELECT * FROM sample_data.nyc.taxi LIMIT 10"
result_df = con.execute(query).fetchdf()

# Show results
st.title("MotherDuck Query Results")
st.dataframe(result_df)