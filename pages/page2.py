import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

def load_data(start_date, end_date):
    # Exemplo de dados de temperatura máxima diária ao meio-dia no intervalo fornecido
    date_range = pd.date_range(start=start_date, end=end_date)
    data = {
        'Data': date_range,
        'Temperatura Máxima ao Meio-Dia (°C)': [20 + (i % 10) for i in range(len(date_range))]  # Dados fictícios
    }
    df = pd.DataFrame(data)
    return df

def main():
    st.title('Page 2')
    st.subheader('Padrões Climáticos Históricos')

    # Perguntar ao usuário a data inicial e a data final
    start_date = st.date_input("Selecione a data inicial", datetime(2023, 1, 1))
    end_date = st.date_input("Selecione a data final", datetime(2023, 12, 31))

    if start_date > end_date:
        st.error("A data inicial não pode ser posterior à data final.")
    else:
        # Carregar dados
        df = load_data(start_date, end_date)

        # Exibir tabela de dados
        st.write(df)

        # Criar gráfico interativo
        chart = alt.Chart(df).mark_line().encode(
            x='Data',
            y='Temperatura Máxima ao Meio-Dia (°C)',
            tooltip=['Data', 'Temperatura Máxima ao Meio-Dia (°C)']
        ).properties(
            width=800,
            height=400
        ).interactive()

        st.altair_chart(chart)

        # Informações adicionais
        st.subheader('Informações Adicionais')
        st.write("""
            Este gráfico mostra a temperatura máxima diária ao meio-dia ao longo do intervalo selecionado.
            Você pode interagir com o gráfico para ver detalhes específicos de cada dia.
        """)

if __name__ == "__main__":
    main()
