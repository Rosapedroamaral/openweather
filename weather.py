import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_AQI = "https://api.openweathermap.org/data/2.5/air_pollution"

# Função para obter dados meteorológicos
def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL_WEATHER, params=params)
    return response.json()

# Função para obter dados de qualidade do ar
def get_aqi_data(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL_AQI, params=params)
    return response.json()

# Função para criar a dashboard
def create_dashboard():
    st.title('Dashboard de Saúde e Clima')

    # Adicionar entrada para cidade
    city = st.text_input("Digite o nome da cidade", "Rio de Janeiro")
    
    if city:
        # Obter dados meteorológicos
        weather_data = get_weather_data(city)
        
        if weather_data.get("cod") != 200:
            st.error(f"Cidade '{city}' não encontrada. Tente outra cidade.")
        else:
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # Obter dados de qualidade do ar
            aqi_data = get_aqi_data(lat, lon)
            
            # Exibir dados meteorológicos
            st.write(f"**Cidade**: {weather_data['name']}")
            st.write(f"**Temperatura**: {weather_data['main']['temp']} °C")
            st.write(f"**Umidade**: {weather_data['main']['humidity']}%")
            st.write(f"**Pressão**: {weather_data['main']['pressure']} hPa")
            st.write(f"**Velocidade do Vento**: {weather_data['wind']['speed']} m/s")
            st.write(f"**Descrição**: {weather_data['weather'][0]['description'].capitalize()}")

            # Processar e exibir dados de qualidade do ar
            aqi_index = aqi_data['list'][0]['main']['aqi']
            pm2_5 = aqi_data['list'][0]['components']['pm2_5']
            pm10 = aqi_data['list'][0]['components']['pm10']
            no2 = aqi_data['list'][0]['components']['no2']
            o3 = aqi_data['list'][0]['components']['o3']
            so2 = aqi_data['list'][0]['components']['so2']
            co = aqi_data['list'][0]['components']['co']

            st.subheader('Qualidade do Ar')
            st.write(f"**Índice de Qualidade do Ar (AQI)**: {aqi_index}")
            st.write(f"**PM2.5**: {pm2_5} µg/m³")
            st.write(f"**PM10**: {pm10} µg/m³")
            st.write(f"**NO₂**: {no2} µg/m³")
            st.write(f"**O₃**: {o3} µg/m³")
            st.write(f"**SO₂**: {so2} µg/m³")
            st.write(f"**CO**: {co} µg/m³")

            # Exibir gráficos de qualidade do ar
            aqi_df = pd.DataFrame({
                'Poluente': ['PM2.5', 'PM10', 'NO₂', 'O₃', 'SO₂', 'CO'],
                'Valor (µg/m³)': [pm2_5, pm10, no2, o3, so2, co]
            })

            aqi_chart = alt.Chart(aqi_df).mark_bar().encode(
                x=alt.X('Poluente:N'),
                y=alt.Y('Valor (µg/m³):Q'),
                color='Poluente:N'
            ).properties(width=600, height=400).interactive()

            st.altair_chart(aqi_chart)

if __name__ == "__main__":
    create_dashboard()

    # Adiciona um botão para atualização manual
    if st.button("Atualizar Dados"):
        st.rerun()
