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
        if navigation == "Contact":
            st.markdown(f"""<div style="height: 200px;"><img src="{original_json[idx]['avatar_url']}" alt="No avatar" height="200"></div>""", unsafe_allow_html=True)
        st.write('## Original Json')
        original_json_dict = {key: original_json[idx][key] for key in ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country', 'linkedin_url', 'facebook_url', 'twitter_url', 'investor_type', 'check_size_max', 'check_size_min', 'investment_stages', 'investment_strategies', 'strategic_sectors', 'geographic_preferences', 'work_history']}
        st.json(original_json_dict)
    with col2:
        if navigation == "Contact":
            st.markdown(f"""<div style="height: 200px;"><img src="{apollo_enrich_json[idx]['avatar_url']}" alt="No avatar" height="200"></div>""", unsafe_allow_html=True)
        st.write('## Appolo-enriched Json')
        apollo_enrich_json_dict = {key: apollo_enrich_json[idx][key] for key in ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country', 'linkedin_url', 'facebook_url', 'twitter_url', 'investor_type', 'check_size_max', 'check_size_min', 'investment_stages', 'investment_strategies', 'strategic_sectors', 'geographic_preferences', 'work_history']}
        st.json(apollo_enrich_json_dict)
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
