"This is my first streamlit app"

import time
import streamlit as st
import pandas as pd 
import numpy as np

add_selectbox = st.sidebar.selectbox(
    'How would you like to be connected?', 
    ('Email', 'Home phone', 'Mobile phone')
)

add_slider = st.sidebar.slider(
    'select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
left_column.button('Press me!')

with right_column:
    chosen = st.radio(
        'Sorting hat',
        ('A', 'B', 'C', 'D'))
    
    st.write(f"You are in {chosen} house")

st.write("Here's our first attempt at using streamlit")
st.write(pd.DataFrame({
    'first_column': [1, 2, 3, 4],
    'second_colunm': [10, 20, 30, 50]
}))

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

x = st.slider('x')
st.write(x, 'squared is', x * x)

st.text_input('Your Name', key = 'name')
st.session_state.name

if st.checkbox('Show DataFrame'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    chart_data

df = pd.DataFrame({
    'first_column': [1, 2, 3, 4],
    'second_colunm': [10, 20, 30, 50]})

option = st.selectbox(
    'Which number do you like best?',
    df['first_column']
)
'Your selected: ', option

"Starting a long computaion..."
latest_intertion = st.empty()
bar = st.progress(0)

for i in range(10):
    latest_intertion.text(f"Iteraion {i + 1}")
    bar.progress(i+1)
    time.sleep(0.1)

    "...and now we\'re done"