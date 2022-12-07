import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list= pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

fruit_selected=streamlit.multiselect("Pick some fruits:", list (my_fruit_list.index),['Avocado','Strawberries'])
fruit_to_show=my_fruit_list.loc[fruit_selected]

streamlit.dataframe(fruit_to_show) 

streamlit.header("Fruityvice Fruit Advice!")
#adding interface code 
fruit_choice=streamlit.text_input('What fruit would you like information about?','Kiwi') #input data
streamlit.write('The user entered',fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice) #parametrised call for fruit choice
#streamlit.text(fruityvice_response.json()) no longer needed

##normalise json
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

##output as table
streamlit.dataframe(fruityvice_normalized)

#do not run anything past here while we check
streamlit.stop()
#connection to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

##second user input
fruit_second_choice=streamlit.text_input('What fruit would you like to add?','Kiwi') #input data
streamlit.write('Thanks for adding ',fruit_second_choice)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")




