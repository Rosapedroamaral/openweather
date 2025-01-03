import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_HISTORICAL = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

# Função para obter dados meteorológicos
def get_weather_data(city, country):
    params = {
        'q': f"{city},{country}",
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL_WEATHER, params=params)
    return response.json()

# Função para obter dados históricos
def get_historical_data(lat, lon, date):
    timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    params = {
        'lat': lat,
        'lon': lon,
        'dt': timestamp,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL_HISTORICAL, params=params)
    return response.json()

def show_historical_analysis():
    st.title("Análise Histórica de Dados Climáticos")

    city = st.text_input("Digite o nome da cidade", "Rio de Janeiro")
    country = st.text_input("Digite o código do país (ex: br, us, ca)", "br")
    
    if city and country:
        city = city.strip().title()
        country = country.strip().lower()
        weather_data = get_weather_data(city, country)
        st.write("Dados Meteorológicos:", weather_data)  # Adiciona mensagem de depuração
        
        if weather_data.get("cod") != 200:
            st.error(f"Cidade '{city}' não encontrada no país '{country.upper()}'. Tente outra cidade ou país.")
        else:
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # Seleção de data
            start_date = st.date_input("Selecione a data inicial", datetime.today() - timedelta(days=7))
            end_date = st.date_input("Selecione a data final", datetime.today())
            
            if start_date and end_date:
                date_range = pd.date_range(start_date, end_date)
                historical_data = []

                # Obtenção de dados históricos para o intervalo de datas
                for date in date_range:
                    data = get_historical_data(lat, lon, date.strftime("%Y-%m-%d"))
                    st.write(f"Dados Históricos para {date.strftime('%Y-%m-%d')}: ", data)  # Adiciona mensagem de depuração
                    if 'current' in data:
                        historical_data.append({
                            'Data': date.strftime("%Y-%m-%d"),
                            'Temperatura (°C)': data['current']['temp'],
                            'Umidade (%)': data['current']['humidity']
                        })

                if historical_data:
                    historical_df = pd.DataFrame(historical_data)
                    st.subheader(f"Dados Históricos de {city}")
                    st.line_chart(historical_df.set_index('Data'))

def main():
    st.title('Page 2')
    show_historical_analysis()

if __name__ == "__main__":
    main()
