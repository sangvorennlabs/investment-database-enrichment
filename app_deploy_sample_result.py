import pickle
import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(layout="wide")

with st.sidebar:
    input_password = st.text_input(label='password', type='password')

if input_password in ['rennlabs123***']:
    json_data = [json.load(open(f'sample_result_claude_agent_2.1/{x}', 'r')) for x in os.listdir('sample_result_claude_agent_2.1')]
    idx = st.number_input('Sample number', 1, len(json_data)) - 1
    col1, col2 = st.columns([1,2])
    with col1:
        st.write('# Input')
        st.write(f'## Company name:\n{json_data[idx]["firm_name"]}')
        st.write(f'## Company website:\n{json_data[idx]["website_url"]}')
    with col2:
        st.write('# Output')
        st.json(json_data[idx])