import pickle
import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(layout="wide")

with st.sidebar:
    input_password = st.text_input(label='password', type='password')
    if input_password in ['rennlabs123***']:
        navigation = st.radio("Navigation", ["Contact", "Firm"])

if input_password in ['rennlabs123***']:
    original_json = json.load(open('sample_apollo/contact/2024-04-05T17_13_31.679141-contact-original.json')) if navigation=="Contact" else json.load(open('sample_apollo/firm/2024-04-05T17_13_31.679141-firm-original.json'))
    apollo_enrich_json = json.load(open('sample_apollo/contact/2024-04-05T17_13_31.679141-contact-enriched.json')) if navigation=="Contact" else json.load(open('sample_apollo/firm/2024-04-05T17_13_31.679141-firm-enriched.json'))
    st.write('# Contact comparision') if navigation=="Contact" else st.write('# Firm comparision')
    idx = st.number_input('Sample number', 1, len(original_json)) - 1
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        st.write('## Original Json')
        st.json(original_json[idx])
    with col2:
        st.write('## Appolo-enriched Json')
        st.json(apollo_enrich_json[idx])
    with col3:
        enriched_field = [key1 for ((key1, value1), (key1, value2)) in zip(original_json[idx].items(), apollo_enrich_json[idx].items()) if value1==None and value2]
        different_field = {key1:[value1,value2] for ((key1, value1), (key1, value2)) in zip(original_json[idx].items(), apollo_enrich_json[idx].items()) if value1!=value2 and value1 and value2}
        st.write('## Compare fields')
        st.write('### Enriched fields')
        a = [st.write(f"- {x}") for x in enriched_field]
        st.write('### Different fields')
        a = [st.write(f"- {k}:\n\n{v}") for k, v in different_field.items()]
        
        data = {
            'Original':[v[0] for k,v in different_field.items()],
            'Appolo-enriched':[v[1] for k,v in different_field.items()],
        }
        df = pd.DataFrame(data, index=different_field.keys())                
