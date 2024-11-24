import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configurações da API do OpenWeather
API_KEY = st.secrets["API_KEY"]
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/onecall"
BASE_URL_AIR_QUALITY = "https://api.openweathermap.org/data/2.5/air_pollution"

# Níveis recomendados de poluentes (valores fictícios para exemplo)
RECOMMENDED_LEVELS = {
    'pm2_5': 25,  # µg/m³
    'pm10': 50,  # µg/m³
    'no2': 40,  # µg/m³
    'so2': 20,  # µg/m³
    'o3': 100,  # µg/m³
    'co': 450  # ppm
}

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

# Função para obter dados de previsão do tempo
def get_weather_forecast(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'current,minutely,hourly,alerts',
        'units': 'metric',
        'appid': API_KEY
    }
    response = requests.get(BASE_URL_FORECAST, params=params)
    return response.json()

# Função para obter dados de qualidade do ar
def get_air_quality_data(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL_AIR_QUALITY, params=params)
    return response.json()

# Função para criar a dashboard
def create_dashboard():
    st.title('Dashboard de Saúde e Clima')

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
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            air_quality_data = get_air_quality_data(lat, lon)
            weather_forecast_data = get_weather_forecast(lat, lon)
            
            st.write(f"**Cidade**: {weather_data['name']}")
            st.write(f"**Temperatura**: {weather_data['main']['temp']} °C")
            st.write(f"**Umidade**: {weather_data['main']['humidity']}%")
            st.write(f"**Pressão**: {weather_data['main']['pressure']} hPa")
            st.write(f"**Velocidade do Vento**: {weather_data['wind']['speed']} m/s")
            st.write(f"**Descrição**: {weather_data['weather'][0]['description'].capitalize()}")

            if air_quality_data:
                air_quality_index = air_quality_data['list'][0]['main']['aqi']
                st.write(f"**Qualidade do Ar**: {air_quality_index}")
                
                components = air_quality_data['list'][0]['components']
                components_df = pd.DataFrame(components.items(), columns=['Componente', 'Concentração'])

                # Verificar componentes acima dos níveis recomendados
                for component, concentration in components.items():
                    # Considerar ppm para CO e ajustar valores de referência
                    if component == 'co':
                        concentration_ppm = concentration / 1000  # Converter µg/m³ para ppm
                        if concentration_ppm > RECOMMENDED_LEVELS[component]:
                            st.warning(f"Nível de {component.upper()} está acima do recomendado: {concentration_ppm} ppm (Recomendado: {RECOMMENDED_LEVELS[component]} ppm)")
                    elif component in RECOMMENDED_LEVELS and concentration > RECOMMENDED_LEVELS[component]:
                        st.warning(f"Nível de {component.upper()} está acima do recomendado: {concentration} µg/m³ (Recomendado: {RECOMMENDED_LEVELS[component]} µg/m³)")

                # Exibir gráfico de componentes do ar
                st.subheader('Componentes da Qualidade do Ar')
                air_quality_chart = alt.Chart(components_df).mark_bar().encode(
                    x=alt.X('Componente:N'),
                    y=alt.Y('Concentração:Q'),
                    tooltip=['Componente', 'Concentração']
                ).properties(width=600, height=400).interactive()
                st.altair_chart(air_quality_chart)

            if 'daily' in weather_forecast_data:
                # Extrair dados de previsão do tempo
                forecast_dates = []
                forecast_temps = []
                for day in weather_forecast_data['daily']:
                    forecast_dates.append(pd.to_datetime(day['dt'], unit='s'))
                    forecast_temps.append(day['temp']['day'])

                forecast_df = pd.DataFrame({
                    'Data': forecast_dates,
                    'Temperatura (°C)': forecast_temps
                })

                # Exibir gráfico de previsão do tempo
                st.subheader('Previsão do Tempo para os Próximos Dias')
                weather_forecast_chart = alt.Chart(forecast_df).mark_line(point=True).encode(
                    x=alt.X('Data:T', title='Data'),
                    y=alt.Y('Temperatura (°C):Q', title='Temperatura (°C)'),
                    tooltip=['Data', 'Temperatura (°C)']
                ).properties(width=600, height=400).interactive()
                st.altair_chart(weather_forecast_chart)
            else:
                st.warning("Dados de previsão do tempo não disponíveis.")
                # Exibir a resposta completa da API para depuração
                st.json(weather_forecast_data)

if __name__ == "__main__":
    create_dashboard()

    # Adiciona um botão para atualização manual
    if st.button("Atualizar Dados"):
        st.rerun()
