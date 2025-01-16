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

# Dados fictícios para demonstração (valores diferenciados)
@st.cache_data
def load_data():
    data = {
        'Mês': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] * 3,
        'Setor': ['Produção'] * 12 + ['Logística'] * 12 + ['Administração'] * 12,
        'CO2 (ton)': [1200, 1250, 1300, 1400, 1450, 1500, 1550, 1600, 1700, 1750, 1800, 1900] +  # Produção
                     [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1200] +        # Logística
                     [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420],            # Administração
        'CH4 (ton)': [300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410] +           # Produção
                     [150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 210] +          # Logística
                     [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110],                     # Administração
        'N2O (ton)': [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260] +          # Produção
                     [75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130] +              # Logística
                     [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]                        # Administração
    }
    return pd.DataFrame(data)  # Carregar os dados

df = load_data()

# Sidebar para filtros
st.sidebar.header("🎛️ Filtros")
mes_selecionado = st.sidebar.multiselect("Selecione o mês:", df['Mês'].unique(), default=df['Mês'].unique())
setor_selecionado = st.sidebar.multiselect("Selecione o setor:", df['Setor'].unique(), default=df['Setor'].unique())
tipo_gas = st.sidebar.multiselect("Selecione o tipo de gás:", ['CO2 (ton)', 'CH4 (ton)', 'N2O (ton)'], default=['CO2 (ton)', 'CH4 (ton)', 'N2O (ton)'])

# Filtrar os dados
dados_filtrados = df[(df['Mês'].isin(mes_selecionado)) & (df['Setor'].isin(setor_selecionado))]

# Layout em colunas para os KPIs
st.markdown("## ⚡ Principais Métricas")
col1, col2, col3 = st.columns(3)

with col1:
    total_co2 = dados_filtrados['CO2 (ton)'].sum()
    st.metric("Total de CO2", f"{total_co2} ton", delta=f"{total_co2 - 1000} ton")

with col2:
    total_ch4 = dados_filtrados['CH4 (ton)'].sum()
    st.metric("Total de CH4", f"{total_ch4} ton", delta=f"{total_ch4 - 300} ton")

with col3:
    total_n2o = dados_filtrados['N2O (ton)'].sum()
    st.metric("Total de N2O", f"{total_n2o} ton", delta=f"{total_n2o - 150} ton")

# Gráficos: Visão Geral
st.markdown("## 📊 Visão Geral das Emissões")

# Gráfico de barras: Emissões Totais
emissoes_totais = dados_filtrados.groupby('Setor')[tipo_gas].sum().reset_index()
emissoes_totais_melted = emissoes_totais.melt(id_vars='Setor', var_name='Gás', value_name='Emissões (ton)')

fig_bar_total = px.bar(
    emissoes_totais_melted,
    x='Setor',
    y='Emissões (ton)',
    color='Gás',
    barmode='group',
    title="Emissões Totais por Setor e Tipo de Gás",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_bar_total, use_container_width=True)

# Gráfico de linhas: Evolução Temporal (Separado por Setor)
st.markdown("## 📈 Evolução Temporal das Emissões por Setor")

for setor in setor_selecionado:
    st.markdown(f"### Setor: {setor}")
    dados_setor = dados_filtrados[dados_filtrados['Setor'] == setor]

    fig_line_setor = px.line(
        dados_setor,
        x='Mês',
        y=tipo_gas,
        title=f"Evolução das Emissões no Setor {setor}",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_line_setor, use_container_width=True)

# Gráficos por Setor
st.markdown("## 🔍 Análise por Setor")

for setor in setor_selecionado:
    st.markdown(f"### Setor: {setor}")
    dados_setor = dados_filtrados[dados_filtrados['Setor'] == setor]

    fig_bar_setor = px.bar(
        dados_setor,
        x='Mês',
        y=tipo_gas,
        barmode='group',
        title=f"Emissões por Gás no Setor {setor}",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig_bar_setor, use_container_width=True)

# Download de Dados
st.markdown("## 📥 Download do Relatório")
st.download_button(
    label="Baixar Dados como CSV",
    data=dados_filtrados.to_csv(index=False),
    file_name="emissoes_setores.csv",
    mime="text/csv",
    help="Faça o download dos dados filtrados para análise offline."
)
