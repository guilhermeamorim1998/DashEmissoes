import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do layout da página
st.set_page_config(
    page_title="Dashboard de Emissões Industriais",
    page_icon="🌍",
    layout="wide",
)

# Estilo customizado
st.markdown(
    """
    <style>
        .css-18e3th9 {padding: 1rem 2rem;}
        .css-1d391kg {padding: 1rem 2rem;}
        .main {background-color: #f4f4f4;}
        h1, h2, h3, h4 {font-family: 'Arial';}
        .stButton>button {background-color: #ffcc00; color: black; font-size: 18px;}
        .stButton>button:hover {background-color: #f0ad00;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal
st.title("🌍 Dashboard de Emissões Industriais")

# Inputs para os dados de emissões
st.sidebar.header("🔧 Insira os Dados de Emissões")
meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mes_selecionado = st.sidebar.multiselect("Selecione os meses:", meses, default=meses)

# Criar um DataFrame vazio com os meses selecionados
emissoes_data = {'Mês': mes_selecionado}

# Adicionar campos de entrada para os gases
emissoes_data['CO2 (ton)'] = [st.sidebar.number_input(f'Emissões de CO2 para {mes}', min_value=0, step=1) for mes in mes_selecionado]
emissoes_data['CH4 (ton)'] = [st.sidebar.number_input(f'Emissões de CH4 para {mes}', min_value=0, step=1) for mes in mes_selecionado]
emissoes_data['N2O (ton)'] = [st.sidebar.number_input(f'Emissões de N2O para {mes}', min_value=0, step=1) for mes in mes_selecionado]

# Converter o dicionário em DataFrame
df = pd.DataFrame(emissoes_data)

# Sidebar para filtros
st.sidebar.header("🎛️ Filtros")
tipo_gas = st.sidebar.multiselect("Selecione o tipo de gás:", ['CO2 (ton)', 'CH4 (ton)', 'N2O (ton)'], default=['CO2 (ton)', 'CH4 (ton)', 'N2O (ton)'])

# Layout em colunas para os KPIs
st.markdown("## ⚡ Principais Métricas")
col1, col2, col3 = st.columns(3)

with col1:
    total_co2 = df['CO2 (ton)'].sum()
    st.metric("Total de CO2", f"{total_co2} ton")

with col2:
    total_ch4 = df['CH4 (ton)'].sum()
    st.metric("Total de CH4", f"{total_ch4} ton")

with col3:
    total_n2o = df['N2O (ton)'].sum()
    st.metric("Total de N2O", f"{total_n2o} ton")

# Gráficos
st.markdown("## 📊 Visualização das Emissões")

# Gráfico 1: Emissões Totais
emissoes_totais = df[tipo_gas].sum()
df_emissoes_totais = emissoes_totais.reset_index()
df_emissoes_totais.columns = ['Gás', 'Emissões (ton)']

fig_bar = px.bar(
    df_emissoes_totais,
    x='Gás',
    y='Emissões (ton)',
    title="Emissões Totais por Tipo de Gás",
    color='Gás',
    text='Emissões (ton)',
    template="plotly_white",
    color_discrete_sequence=px.colors.sequential.YlOrBr
)
fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico 2: Evolução Temporal
fig_line = px.line(
    df,
    x='Mês',
    y=tipo_gas,
    title="Evolução Temporal das Emissões",
    markers=True,
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_line, use_container_width=True)

# Gráfico 3: Proporção por Tipo de Gás
fig_pie = px.pie(
    values=emissoes_totais,
    names=tipo_gas,
    title="Proporção de Emissões por Tipo de Gás",
    color_discrete_sequence=px.colors.sequential.Sunset
)
st.plotly_chart(fig_pie, use_container_width=True)

# Download de Dados
st.markdown("## 📥 Download do Relatório")
st.download_button(
    label="Baixar Dados como CSV",
    data=df.to_csv(index=False),
    file_name="emissoes_industria.csv",
    mime="text/csv",
    help="Faça o download dos dados filtrados para análise offline."
)
