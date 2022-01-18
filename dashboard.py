import pandas as pd
import streamlit as st
import Scrapper


URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
region = "Boston"#args.region
URL += region
df = pd.read_csv('/Users/paulmontecotgrall/Downloads/rideshare_kaggle.csv')
df = df.dropna()

data = Scrapper.get_weather_data(URL)


#Config of the app
st.set_page_config(
    # Can be "centered" or "wide". In the future also "dashboard", etc.
    layout="wide",
    initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
    # String or None. Strings get appended with "• Streamlit".
    page_title="Features Extraction Interface \U0001F58A",
    page_icon="\U0001F58A Features Extraction Interface",  # String, anything supported by st.image, or None.
# Display a title
)
st.title('Cab Price prediction application')

st.markdown("**Fill the differents items then click on predict**")

#Data Infos
st.sidebar.subheader('What is your favourite VTC service ?')
cab_type = st.sidebar.selectbox("",df['cab_type'].unique())
cab_pricing = st.sidebar.selectbox("",df['product_id'].unique())

st.subheader('Where do you come from ?')
origin = st.selectbox("",df['source'].unique())

st.subheader('Where are you going ?')
destination = st.selectbox("",df['destination'].unique())

st.sidebar.subheader('Price rate')
rate = st.sidebar.selectbox("",df['surge_multiplier'].unique())

st.subheader('Distance')
distance = st.number_input('', min_value=df['distance'].min(), max_value=df['distance'].max(), value=df['distance'].mean(), step=0.5)

st.subheader('Meteo Description')
meteo_description = st.selectbox("",df['icon'].unique())
long_summary = st.selectbox("",df['long_summary'].unique())

st.sidebar.subheader("Meteo")
st.sidebar.write(' Weather for: {}'.format(data["region"]))
st.sidebar.write(" Now: {}".format(data["dayhour"]))
st.sidebar.write(" Temperature now:{}°C".format(data['temp_now']))
st.sidebar.write(" {}".format(data['weather_now']))
st.sidebar.write(" Precipitation:{}".format(data["precipitation"]))
st.sidebar.write(" Humidity:{}".format(data["humidity"]))
st.sidebar.write(" Wind:{}".format(data["wind"]))









