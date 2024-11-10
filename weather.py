import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Função para obter dados meteorológicos
def get_weather_data(city, country):
    params = {
        'q': f"{city},{country}",
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

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
        weather_data = get_weather_data(city, country)
        
        if weather_data.get("cod") != 200:
            st.error(f"Cidade '{city}' não encontrada no país '{country.upper()}'. Tente outra cidade ou país.")
        else:
            st.write(f"**Cidade**: {weather_data['name']}")
            st.write(f"**Temperatura**: {weather_data['main']['temp']} °C")
            st.write(f"**Umidade**: {weather_data['main']['humidity']}%")
            st.write(f"**Pressão**: {weather_data['main']['pressure']} hPa")
            st.write(f"**Velocidade do Vento**: {weather_data['wind']['speed']} m/s")
            st.write(f"**Descrição**: {weather_data['weather'][0]['description'].capitalize()}")

            # Exibir gráfico de temperatura
            temp_df = pd.DataFrame({
                'Métrica': ['Temperatura', 'Umidade', 'Pressão', 'Velocidade do Vento'],
                'Valor': [weather_data['main']['temp'], weather_data['main']['humidity'], weather_data['main']['pressure'], weather_data['wind']['speed']]
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
