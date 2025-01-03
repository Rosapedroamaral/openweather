import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

# Função para obter previsão do tempo
def get_forecast_data(city, country):
    params = {
        'q': f"{city},{country}",
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL_FORECAST, params=params)
    return response.json()

# Função para exibir a análise de previsão
def display_forecast_analysis(city, country):
    st.title("Análise de Tendências de Previsão")

    forecast_data = get_forecast_data(city, country)
    if forecast_data.get("cod") != "200":
        st.error("Erro ao obter dados de previsão do tempo.")
    else:
        forecast_list = []
        for day in forecast_data['list']:
            forecast_list.append({
                'Data': day['dt_txt'],
                'Temperatura (°C)': day['main']['temp'],
                'Descrição': day['weather'][0]['description'].capitalize()
            })

        forecast_df = pd.DataFrame(forecast_list)
        forecast_df['Data'] = pd.to_datetime(forecast_df['Data'])

        # Ordenar os dados pela coluna 'Data' para garantir a sequência correta
        forecast_df.sort_values(by='Data', inplace=True)

        # Verificar se os dados estão na ordem correta
        st.write("Dados Ordenados:")
        st.write(forecast_df)

        st.line_chart(forecast_df.set_index('Data'))

def main():
    st.title('Page 2')

    city = st.text_input("Digite o nome da cidade", "Rio de Janeiro")
    country = st.text_input("Digite o código do país (ex: br, us, ca)", "br")

    if city and country:
        display_forecast_analysis(city, country)

if __name__ == "__main__":
    main()
