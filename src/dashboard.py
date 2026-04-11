import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# conexão (CORRIGIDO)
engine = create_engine('postgresql://postgres:False157@localhost:5432/iot_db')

# função para carregar dados (CORRIGIDA)
def load_data(view_name):
    try:
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql(query, engine)

        # garantir que não tenha erro de encoding
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str)

        return df

    except Exception as e:
        st.error(f"Erro ao carregar {view_name}: {e}")
        return pd.DataFrame()

# título
st.title("📊 Dashboard de Temperaturas IoT")

# gráfico 1
st.header("📈 Média de Temperatura por Dispositivo")
df1 = load_data('avg_temp_por_dispositivo')

if not df1.empty:
    fig1 = px.bar(df1, x='device_id', y='avg_temp')
    st.plotly_chart(fig1)
else:
    st.warning("Sem dados para exibir")

# gráfico 2
st.header("⏱ Leituras por Hora")
df2 = load_data('leituras_por_hora')

if not df2.empty:
    fig2 = px.line(df2, x='hora', y='contagem')
    st.plotly_chart(fig2)
else:
    st.warning("Sem dados para exibir")

# gráfico 3
st.header("📅 Máximo e Mínimo por Dia")
df3 = load_data('temp_max_min_por_dia')

if not df3.empty:
    fig3 = px.line(df3, x='data', y=['temp_max', 'temp_min'])
    st.plotly_chart(fig3)
else:
    st.warning("Sem dados para exibir")