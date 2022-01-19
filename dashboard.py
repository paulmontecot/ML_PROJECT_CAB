import pandas as pd
import streamlit as st
import Scrapper
import pickle
import sklearn

#with open('/Users/paulmontecotgrall/Downloads/HistBoost.sav') as f:
f = open('/Users/paulmontecotgrall/Downloads/HistBoost.sav', 'rb')
model = pickle.load(f)

print(model)
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

humidity = data["humidity"][:-1]
precip = data["precipitation"][:-1]
wind = data["wind"].split(" ")
day = data["dayhour"].split(" ")
hour = day[1].split(':')

print(humidity)
print(precip)
print(wind)

to_pred = {"timestamp":1.543708e+09,"hour": hour[0], "day": 16,
           "source": origin,"destination": destination, "cab_type":cab_type,"name":cab_pricing,
           "distance":distance,"latitude":42.2148,"longitude":-71.0330,"temperature":data['temp_now'],
           "humidity":humidity,"windSpeed":wind[0], "icon":meteo_description ,"surge_multiplier":rate,
           "long_summary":long_summary,"datetime":'Sunday',"precipIntensity":precip}
to_pred = pd.DataFrame.from_records([to_pred])
print(to_pred)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

categorical_columns = ['source', 'destination', 'cab_type', 'name', 'icon', 'long_summary', 'datetime']
numerical_columns = ['timestamp', 'hour', 'day', 'distance', 'latitude', 'longitude', 'temperature', 'humidity',
                     'windSpeed', 'surge_multiplier', 'precipIntensity']
# numerical_columns = ['timestamp', 'hour', 'day', 'distance', 'latitude', 'longitude', 'temperature', 'humidity', 'windSpeed','surge_multiplier']
# numerical_columns = ['hour', 'day', 'distance', 'latitude', 'longitude', 'temperature', 'humidity', 'windSpeed']
to_pred = pd.get_dummies(to_pred, columns=categorical_columns)
print(to_pred)
#Q1 = to_pred[numerical_columns].quantile(0.25)
#Q3 = to_pred[numerical_columns].quantile(0.75)
#IQR = Q3 - Q1

# features = features[~((features[numerical_columns] < (Q1 - 1.5 * IQR)) |(features[numerical_columns] > (Q3 + 1.5 * IQR))).any(axis=1)]



#for i in numerical_columns:
    # fit on training data column
    #scale = StandardScaler().fit(to_pred[[i]])

    # transform the training data column
    #to_pred[i] = scale.transform(to_pred[[i]])
print(to_pred)
st.write(to_pred)


if st.button('PREDICT'):
    price = model.predict(to_pred)
    st.write('The price will be {}'.format(price))








