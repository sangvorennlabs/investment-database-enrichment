import pickle
import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(layout="wide")

with st.sidebar:
    input_password = st.text_input(label='password', type='password')

if input_password in ['rennlabs123***']:
    json_data_claude = [json.load(open(f'sample_result_claude_agent_2.1/{x}', 'r')) for x in os.listdir('sample_result_claude_agent_2.1')]
    json_data_openai = [json.load(open(f'sample_result_openai_agent/{x}', 'r')) for x in os.listdir('sample_result_openai_agent')]
    json_input = json.load(open('input.json', 'r'))
    
    idx = st.number_input('Sample number', 1, len(json_data_openai)) - 1

    company_name = os.listdir('sample_result_claude_agent_2.1')[idx].split('.')[0]
    company_url = [x for x in json_input if x["Company name"]==company_name][0]["Company website"] if company_name!="Renn Global" else "https://www.rennglobal.com/"

    st.write('# Input')
    st.write(f'## Company name:\n{company_name}')
    st.write(f'## Company website:\n{json_data_openai[idx]["website_url"]}')
    col1, col2 = st.columns([1,1])
    with col1:
        st.write('# Output (claude-instant-2.1)')
        st.json(json_data_claude[idx])
    with col2:
        st.write('# Output (gpt-3.5-turbo-0125)')
        st.json(json_data_openai[idx])
