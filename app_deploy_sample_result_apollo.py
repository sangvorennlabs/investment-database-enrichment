import pickle
import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(layout="wide")

original_json_contact = json.load(open('sample_apollo/contact/contacts-original.json'))
original_json_firm = json.load(open('sample_apollo/firm/firms-original.json'))
apollo_enrich_json_contact = json.load(open('sample_apollo/contact/contacts-apollo-enriched.json'))
apollo_enrich_json_firm = json.load(open('sample_apollo/firm/firms-apollo-enriched.json'))
ai_enrich_json = json.load(open('sample_apollo/firm/firms-ai-enriched.json'))

ai_enrich_json_gpt_35 = json.load(open('sample_apollo/gpt3.5 vs gpt4/firms-ai-enriched-gpt3.5-40-records.json'))
ai_enrich_json_gpt_4 = json.load(open('sample_apollo/gpt3.5 vs gpt4/firms-ai-enriched-gpt4-40-records.json'))
ai_enrich_json_gemini_pro_15_latest = json.load(open('sample_apollo/gpt3.5 vs gpt4/firms-ai-enriched-gemini-1.5-pro-latest-40-records.json'))
with st.sidebar:
    input_password = st.text_input(label='password', type='password')
    if input_password in ['rennlabs123***']:
        navigation = st.radio("Navigation", ["Contact", "Firm enriched with Apollo", "Firm enriched with AI", "Comparision GPT-3.5 VS GPT-4", "Comparision Gemini-1.5-pro-latest VS GPT-4"])

if input_password in ['rennlabs123***']:
    if navigation == "Comparision Gemini-1.5-pro-latest VS GPT-4":
        st.write("Gemini-1.5-pro-latest VS GPT-4 on data enrichment")
        idx = st.number_input('Sample number', 1, len(ai_enrich_json_gemini_pro_15_latest)) - 1
        col1, col2 = st.columns([1,1])
        keys_to_display = ['name', 'website_url', 'firm_type', 'strategic_sectors', 'investment_stages', 'investment_strategies', 'geographic_preferences', 'investor_type', 'investment_approach', 'asset_under_management_value', 'check_size_typical', 'notable_investments', 'investment_highlights', ]
        with col1:
            st.write('## Gemini-1.5-pro-latest with new prompting')
            st.json({key:ai_enrich_json_gemini_pro_15_latest[idx].get(key) for key in keys_to_display})
        with col2:
            st.write('## GPT 4 with new prompting')
            st.json({key:ai_enrich_json_gpt_4[idx].get(key) for key in keys_to_display})
    elif navigation == "Comparision GPT-3.5 VS GPT-4":
        st.write("GPT-3.5 VS GPT-4 on data enrichment")
        idx = st.number_input('Sample number', 1, len(ai_enrich_json_gpt_35)) - 1
        col1, col2 = st.columns([1,1])
        keys_to_display = ['name', 'website_url', 'firm_type', 'strategic_sectors', 'investment_stages', 'investment_strategies', 'geographic_preferences', 'investor_type', 'investment_approach', 'asset_under_management_value', 'check_size_typical', 'notable_investments', 'investment_highlights', ]
        with col1:
            st.write('## GPT 3.5 with old prompting')
            st.json({key:ai_enrich_json_gpt_35[idx].get(key) for key in keys_to_display})
        with col2:
            st.write('## GPT 4 with new prompting')
            st.json({key:ai_enrich_json_gpt_4[idx].get(key) for key in keys_to_display})
    else:
        # original_json = json.load(open('sample_apollo/contact/contact-original.json')) if navigation=="Contact" else json.load(open('sample_apollo/firm/firm-original.json'))
        # apollo_enrich_json = json.load(open('sample_apollo/contact/contact-apollo-enriched.json')) if navigation=="Contact" else json.load(open('sample_apollo/firm/firm-apollo-enriched.json'))
        # ai_enrich_json = json.load(open('sample_apollo/firm/firm-ai-enriched.json'))
        st.write('# Contact comparision') if navigation=="Contact" else st.write('# Firm comparision')
        idx = st.number_input('Sample number', 1, len(original_json_contact)) - 1
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            if navigation == "Contact":
                st.markdown(f"""<div style="height: 200px;"><img src="{original_json_contact[idx]['avatar_url']}" alt="No avatar" height="200"></div>""", unsafe_allow_html=True)
                original_json_dict = {key: original_json_contact[idx].get(key) for key in ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country', 'linkedin_url', 'facebook_url', 'twitter_url', 'investor_type', 'check_size_max', 'check_size_min', 'investment_stages', 'investment_strategies', 'strategic_sectors', 'geographic_preferences', 'work_history']}
            elif navigation == "Firm enriched with Apollo":
                original_json_dict = original_json_firm[idx]
            elif navigation == "Firm enriched with AI":
                original_json_dict = original_json_firm[idx] 
            st.write('## Original Json')
            st.json(original_json_dict)
        with col2:
            if navigation == "Contact":
                st.markdown(f"""<div style="height: 200px;"><img src="{apollo_enrich_json_contact[idx]['avatar_url']}" alt="No avatar" height="200"></div>""", unsafe_allow_html=True)
                apollo_enrich_json_dict = {key: apollo_enrich_json_contact[idx].get(key) for key in ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country', 'linkedin_url', 'facebook_url', 'twitter_url', 'investor_type', 'check_size_max', 'check_size_min', 'investment_stages', 'investment_strategies', 'strategic_sectors', 'geographic_preferences', 'work_history', 'enriched_fields', 'fields_need_validation']}
            elif navigation == "Firm enriched with Apollo":
                apollo_enrich_json_dict = apollo_enrich_json_firm[idx]
            elif navigation == "Firm enriched with AI":
                apollo_enrich_json_dict = ai_enrich_json[idx]
            st.write('## Appolo-enriched Json')
            st.json(apollo_enrich_json_dict)
        with col3:
            # enriched_field = [key1 for ((key1, value1), (key1, value2)) in zip(original_json_dict.items(), apollo_enrich_json_dict.items()) if value1==None and value2]
            enriched_field = apollo_enrich_json_dict['enriched_fields'] if navigation != "Firm enriched with AI" else apollo_enrich_json_dict['ai_enriched_fields']
            different_field = {key1:[value1,value2] for ((key1, value1), (key1, value2)) in zip(original_json_dict.items(), apollo_enrich_json_dict.items()) if value1!=value2 and value1 and value2}
            fields_need_validation = apollo_enrich_json_dict.get('fields_need_validation')
            print(fields_need_validation)
            
            st.write('## Compare fields')
            st.write('### Enriched fields')
            a = [st.write(f"- {x}") for x in enriched_field] if enriched_field else []
            # st.write('### Different fields')
            # a = [st.write(f"- {k}:\n\n{v}") for k, v in different_field.items()]
            st.write('### Fields need validation')
            a = [st.write(f"- {x}") for x in fields_need_validation] if fields_need_validation else []
            
            data = {
                'Original':[v[0] for k,v in different_field.items()],
                'Appolo-enriched':[v[1] for k,v in different_field.items()],
            }
            df = pd.DataFrame(data, index=different_field.keys())                