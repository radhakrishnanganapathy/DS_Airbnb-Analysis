import pandas as pd 
import streamlit as st 
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
import pymongo


st.header("DS_AIRBND-ANALYSIS")
icon =  Image.open('icon.png')
# st.set_page_config(page_title= "Airbnb Data Visualization | By Radhakrishnan Ganapathy",
#                    page_icon= icon,
#                    layout= "wide",
#                    initial_sidebar_state= "expanded",
#                    menu_items={'About': """# This dashboard app is created by *Radhakrishnan*!
#                                         Data has been gathered from mongodb atlas"""}
#                   )

with st.sidebar:
     selected = option_menu("Menu",["Home","Overview","Explore"],
                            )
     
client = pymongo.MongoClient("mongodb://localhost:27017") 
db = client.airbnb
col = db.listingreviews

result = col.find()
df = pd.DataFrame(result)
# st.write(df)

if selected == "Home":
     # st.image("icon.png")
     col1,col2 = st.columns(2,gap='small')
     col1.markdown("## :blue[Domain] : Travel Industry , Property Management and Tourism ")
     col1.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
     col1.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
     col2.markdown("#   ")
     col2.markdown("#   ")
     # col2.image("icon.jpg")

if selected == 'Overview':
     tab1, tab2 = st.tabs(["$\huge RAW DATA $","$\huge INSIGHTS $"])

     with tab1:
          col1, col2 =st.columns(2)
          if col1.button("Click to view raw data"):
               col1.write(col.find_one())
               # col1.write(df)
          if col2.button("click to view data frame"):
               data = col.find_one()
               # data_df = pd.DataFrame(data)
               col2.write(df)

     #insight
     with tab2:
          neighbourhood_group = st.sidebar.multiselect('Select a neighbourhood_group',sorted(df.neighbourhood_group.unique()),sorted(df.neighbourhood_group.unique()))
          room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
          price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
          query = f'neighbourhood_group in {neighbourhood_group} & room_type in {room} & price >= {price[0]} & price <= {price[1]}'

          col1,col2=st.columns(2,gap='medium')

          with col1:
               df1 = df.query(query).groupby(['host_name']).size().reset_index(name="Listing").sort_values(by="Listing",ascending=False)[:10]
               fig = px.bar(df1,
                            title='Top 10 Host name',
                            x='Listing',
                            y='host_name',
                            orientation='h',
                            color='host_name',
                            color_continuous_scale=px.colors.sequential.Agsunset)
               st.plotly_chart(fig,use_container_width=True)

          with col2:
               # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
               df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
               fig = px.pie(df1,
                              title='Total Listings in each Room_types',
                              names='room_type',
                              values='counts',
                              color_discrete_sequence=px.colors.sequential.Rainbow
                         )
               fig.update_traces(textposition='outside', textinfo='value+label')
               st.plotly_chart(fig,use_container_width=True)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
#     country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
#     prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    neighbourhood_group = st.sidebar.multiselect('Select a neighbourhood_group',sorted(df.neighbourhood_group.unique()),sorted(df.neighbourhood_group.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f' room_type in {room} &  price >= {price[0]} & price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    