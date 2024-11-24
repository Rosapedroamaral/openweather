import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    # Exemplo de dados de temperatura média diária ao longo de um ano
    data = {
        'Data': pd.date_range(start='2023-01-01', periods=365, freq='D'),
        'Temperatura (°C)': [20 + (i % 10) for i in range(365)]  # Dados fictícios
    }
    df = pd.DataFrame(data)
    return df

def main():
    st.title('Page 2')
    st.subheader('Padrões Climáticos Históricos')

    # Carregar dados
    df = load_data()

    # Exibir tabela de dados
    st.write(df)

    # Criar gráfico interativo
    chart = alt.Chart(df).mark_line().encode(
        x='Data',
        y='Temperatura (°C)',
        tooltip=['Data', 'Temperatura (°C)']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart)

    # Informações adicionais
    st.subheader('Informações Adicionais')
    st.write("""
        Este gráfico mostra a temperatura média diária ao longo de um ano.
        Você pode interagir com o gráfico para ver detalhes específicos de cada dia.
    """)

if __name__ == "__main__":
    main()
