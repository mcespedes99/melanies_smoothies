# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

# Name in app
name_on_order = st.text_input('Name on Smoothie')

# Create table layout
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Add data to multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe)

# Display
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # Get list in string
    ingredients_string = ' '.join(ingredients_list)

    # st.write(ingredients_string)
    
    # Now build a sql command
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+ name_on_order+"""')"""

    # st.write(my_insert_stmt)
    
    # Submit button
    time_to_insert = st.button('Submit Order')

    # Run command
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon='✅')
    
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)