import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Função para obter dados de previsão meteorológica
def get_forecast_data(city, country):
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
    st.title('Dashboard de Previsão do Tempo')

    # Adicionar entrada para cidade e país
    city = st.text_input("Digite o nome da cidade", "Rio de Janeiro")
    country = st.text_input("Digite o código do país (ex: br, us, ca)", "br")
    
    if city and country:
        # Remover espaços extras e capitalizar o nome da cidade
        city = city.strip().title()
        country = country.strip().lower()
        forecast_data = get_forecast_data(city, country)
        
        if forecast_data.get("cod") != "200":
            st.error(f"Cidade '{city}' não encontrada no país '{country.upper()}'. Tente outra cidade ou país.")
        else:
            st.write(f"**Cidade**: {forecast_data['city']['name']}")

            # Exibir dados brutos para depuração
            st.write("Dados Brutos de Previsão:")
            st.write(forecast_data)

            # Processar dados de previsão
            forecast_list = forecast_data['list']
            forecast_df = pd.json_normalize(forecast_list)
            forecast_df['dt'] = pd.to_datetime(forecast_df['dt'], unit='s')
            forecast_df['description'] = forecast_df['weather'].apply(lambda x: x[0]['description'] if isinstance(x, list) and len(x) > 0 else None)
            forecast_df = forecast_df[['dt', 'main.temp', 'main.temp_min', 'main.temp_max', 'description']]

            # Exibir tabela de previsão
            st.subheader('Previsão para os próximos 5 dias')
            st.write(forecast_df)

            # Exibir gráfico de temperatura
            st.subheader('Tendência de Temperatura')
            temp_chart = alt.Chart(forecast_df).mark_line().encode(
                x=alt.X('dt:T', title='Data'),
                y=alt.Y('main.temp:Q', title='Temperatura (°C)'),
                tooltip=['dt:T', 'main.temp:Q', 'description']
            ).properties(width=600, height=400).interactive()
            st.altair_chart(temp_chart)

if __name__ == "__main__":
    create_dashboard()

    # Adiciona um botão para atualização manual
    if st.button("Atualizar Dados"):
        st.rerun()
