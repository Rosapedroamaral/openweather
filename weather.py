import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_HISTORY = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

# Função para obter dados meteorológicos atuais
def get_current_weather_data(city, country):
    params = {
        'q': f"{city},{country}",
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL_CURRENT, params=params)
    return response.json()

# Função para obter dados históricos da temperatura
def get_historical_weather_data(lat, lon, days):
    historical_data = []
    for day in range(days):
        dt = int((datetime.now() - timedelta(days=day)).timestamp())
        params = {
            'lat': lat,
            'lon': lon,
            'dt': dt,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'pt_br'
        }
        response = requests.get(BASE_URL_HISTORY, params=params)
        data = response.json()
        if 'current' in data:
            historical_data.append(data['current'])
    return historical_data

# Função para criar a dashboard
def create_dashboard():
    st.title('Dashboard de Tempo em Tempo Real')

    # Adicionar entrada para cidade e país
    city = st.text_input("Digite o nome da cidade", "Rio de Janeiro")
    country = st.text_input("Digite o código do país (ex: br, us, ca)", "br")
    
    if city and country:
        # Remover espaços extras e capitalizar o nome da cidade
        city = city.strip().title()
        country = country.strip().lower()
        current_weather_data = get_current_weather_data(city, country)
        
        if current_weather_data.get("cod") != 200:
            st.error(f"Cidade '{city}' não encontrada no país '{country.upper()}'. Tente outra cidade ou país.")
        else:
            st.write(f"**Cidade**: {current_weather_data['name']}")
            st.write(f"**Temperatura**: {current_weather_data['main']['temp']} °C")
            st.write(f"**Umidade**: {current_weather_data['main']['humidity']}%")
            st.write(f"**Pressão**: {current_weather_data['main']['pressure']} hPa")
            st.write(f"**Velocidade do Vento**: {current_weather_data['wind']['speed']} m/s")
            st.write(f"**Descrição**: {current_weather_data['weather'][0]['description'].capitalize()}")

            # Obter dados históricos
            lat = current_weather_data['coord']['lat']
            lon = current_weather_data['coord']['lon']
            historical_data = get_historical_weather_data(lat, lon, 5)
            
            if historical_data:
                # Criar DataFrame com dados históricos
                hist_df = pd.DataFrame(historical_data)
                hist_df['dt'] = pd.to_datetime(hist_df['dt'], unit='s')
                hist_df = hist_df[['dt', 'temp']]
                
                # Exibir gráfico de temperatura histórica
                st.subheader('Temperatura nos Últimos Dias')
                temp_chart = alt.Chart(hist_df).mark_line().encode(
                    x=alt.X('dt:T', title='Data'),
                    y=alt.Y('temp:Q', title='Temperatura (°C)'),
                    tooltip=['dt:T', 'temp:Q']
                ).properties(width=600, height=400).interactive()
                st.altair_chart(temp_chart)

            # Exibir gráfico de temperatura atual
            temp_df = pd.DataFrame({
                'Métrica': ['Temperatura', 'Umidade', 'Pressão', 'Velocidade do Vento'],
                'Valor': [current_weather_data['main']['temp'], current_weather_data['main']['humidity'], current_weather_data['main']['pressure'], current_weather_data['wind']['speed']]
            })

            chart = alt.Chart(temp_df).mark_bar().encode(
                x=alt.X('Métrica:N'),
                y=alt.Y('Valor:Q'),
                color='Métrica:N'
            ).properties(width=600, height=400).interactive()

            st.altair_chart(chart)

if __name__ == "__main__":
    create_dashboard()

    # Adiciona um botão para atualização manual
    if st.button("Atualizar Dados"):
        st.rerun()
