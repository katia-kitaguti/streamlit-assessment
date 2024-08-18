
# Imports
import streamlit as st
import pandas as pd
import numpy as np
import json 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


st.set_page_config(layout='wide')
# Creating the main page
header_main = st.header("Trading App", divider="gray")

#Retrieving Data

json_list = ['1ae.json', '1mc.json','aee.json','nrz.json','rez.json']

list_with_dfs = []
for j in json_list:
    with open(f"retrieve_data/{j}", 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data["data"])
    list_with_dfs.append(df)

df  = pd.concat(list_with_dfs)

# Retrieving issuer code filters here:

values_of_filter = df['issuer_code'].unique()

col1, col2 = st.columns(2)

with col1:
    filtered_values = st.multiselect('Select issuer code:',values_of_filter, values_of_filter)
with col2: 
    st.write("Click in the check box below if you want to see only Trading Halt")
    check_box = st.checkbox("Only Show Trading Halt", key="disabled")

# Using filters to filter the df
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df['issuer_code'].isin(filtered_values)]

if check_box:
    filtered_df = filtered_df[filtered_df['header'] == "Trading Halt"]

# Creating the table
header_table = st.header("Table with applied filters :clipboard:", divider = "gray")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gb.configure_grid_options(domLayout="normal")
gridOptions = gb.build()

grid_response = AgGrid(
    filtered_df,
    gridOptions=gridOptions,
    #data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=False,
    theme='streamlit', #Add theme color to the table
    enable_enterprise_modules=True,
    height=800,
    width='100%',
    reload_data=True,
    custom_css={"#gridToolBar": {"padding-bottom": "0px !important"}},
    data_return_mode = DataReturnMode.FILTERED_AND_SORTED)
