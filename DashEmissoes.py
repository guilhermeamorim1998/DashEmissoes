import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt



# Funções para calcular emissões
def calcular_emissoes_fertilizante(quantidade_n):
    return (((quantidade_n * 0.016) + (quantidade_n * 0.11 * 0.014) + (quantidade_n * 0.24 * 0.011)) * 44 / 28) * 298


def calcular_emissoes_calcario(quantidade_calcario, tipo_calcario):
    fatores_emissao = {"Calcítico": 0.12, "Dolomítico": 0.13}
    return (quantidade_calcario * fatores_emissao[tipo_calcario]) * (44 / 12) if tipo_calcario in fatores_emissao else 0


def calcular_emissoes_palha_cafe(quantidade_n_palha_cafe):
    return (((quantidade_n_palha_cafe * 0.006) + (quantidade_n_palha_cafe * 0.21 * 0.014) + (
            quantidade_n_palha_cafe * 0.24 * 0.011)) * 44 / 28) * 298


def calcular_emissoes_cama_frango(quantidade_n_cama_frango):
    return (((quantidade_n_cama_frango * 0.006) + (quantidade_n_cama_frango * 0.21 * 0.014) + (
            quantidade_n_cama_frango * 0.24 * 0.011)) * 44 / 28) * 298


def calcular_emissoes_esterco(quantidade_n_esterco):
    return (((quantidade_n_esterco * 0.006) + (quantidade_n_esterco * 0.21 * 0.014) + (
            quantidade_n_esterco * 0.24 * 0.011)) * 44 / 28) * 298

def calcular_emissoes_diesel(litros_diesel):
    tj_diesel = (litros_diesel * 35.8) / 1_000_000
    emissoes_co2 = tj_diesel * 74100
    emissoes_ch4 = tj_diesel * 4.15 * 25
    emissoes_n2o = tj_diesel * 28.6 * 298
    emissoes_totais_co2eq = emissoes_co2 + emissoes_ch4 + emissoes_n2o
    return emissoes_totais_co2eq, emissoes_co2, emissoes_ch4, emissoes_n2o

def calcular_emissoes_irrigacao_diesel(litros_diesel_irrigacao):
    tj_diesel_irrigacao = (litros_diesel_irrigacao * 35.8) / 1_000_000
    emissoes_co2 = tj_diesel_irrigacao * 74100
    emissoes_ch4 = tj_diesel_irrigacao * 4.15 * 25
    emissoes_n2o = tj_diesel_irrigacao * 28.6 * 298
    emissoes_totais_co2eq = emissoes_co2 + emissoes_ch4 + emissoes_n2o
    return emissoes_totais_co2eq

def calcular_emissoes_irrigacao_eletrica(mwh_eletrica):
    emissoes_co2eq_por_mwh = 0.0003785  # valor médio de emissões para geração de eletricidade (em kg CO₂eq/MWh)
    return mwh_eletrica * emissoes_co2eq_por_mwh


# Configuração do tema customizado no Streamlit (via CSS)
st.markdown(
    """<style>.css-18e3th9 {background-color: #f5f5f5;}.stButton>button {background-color: #0066cc;color: black;border-radius: 10px;font-size: 16px;padding: 8px 16px;border: none;transition: 0.3s;}.stButton>button:hover {background-color: #00509e;color: #ffffff;cursor: pointer;}</style>""",
    unsafe_allow_html=True)

# Título e Imagem de Capa
st.title("🌱 Calculadora de Emissões de Carbono dos Cafés Amazônicos")
st.markdown("### Torne sua produção de café mais sustentável!")
image = Image.open("image/Cafe_Robusta_Amazonico.jpeg")
st.image(image, caption='Café Robusta Amazônico', use_container_width=True)

# Layout em colunas para inputs
st.header("Dados de Entrada")

col1, col2 = st.columns(2)
with col1:
    operacao = st.radio("Tipo de Condução", ("Produção", "Plantio"))

with col2:
    irrigacao = st.radio("💧 Área Irrigada?", ("Sim", "Não"))

# Lista de fertilizantes e suas concentrações de N
fertilizantes = {
    "Sulfato de amônio": 24,
    "Ureia": 44,
    "MAP": 11,
    "20-0-20": 20
}

# Inputs adicionais para fertilizantes 1 e 2
st.subheader("Fertilizantes Sintéticos")
col3, col4 = st.columns(2)

with col3:
    fertilizante1 = st.selectbox("🚜 Fertilizante Opção A", list(fertilizantes.keys()))
    quantidade_fertilizante1 = st.number_input("Quantidade de fertilizante Opção A (kg ha⁻¹ ano⁻¹)", min_value=0.0,
                                               format="%.2f")

with col4:
    fertilizante2 = st.selectbox("🚜 Fertilizante Opção B", list(fertilizantes.keys()))
    quantidade_fertilizante2 = st.number_input("Quantidade de fertilizante Opção B (kg ha⁻¹ ano⁻¹)", min_value=0.0,
                                               format="%.2f")

# Inputs adicionais para outras emissões
st.subheader("Fertilizantes Orgânicos")
quantidade_palha_cafe = st.number_input("Quantidade de palha de café (kg ha⁻¹ ano⁻¹)", min_value=0.0, format="%.2f")
quantidade_cama_frango = st.number_input("Quantidade de cama de frango (kg ha⁻¹ ano⁻¹)", min_value=0.0, format="%.2f")
quantidade_esterco = st.number_input("Quantidade de Esterco Bovino (kg ha⁻¹ ano⁻¹)", min_value=0.0, format="%.2f")
# Inputs para calcário
st.subheader("Calcário")
quantidade_calcario1 = st.number_input("Quantidade de calcário Opção A (kg ha⁻¹ ano⁻¹)", min_value=0.0, format="%.2f")
tipo_calcario1 = st.selectbox("Tipo de calcário Opção A", ["Calcítico", "Dolomítico"])
quantidade_calcario2 = st.number_input("Quantidade de calcário Opção B (kg ha⁻¹ ano⁻¹)", min_value=0.0, format="%.2f")
tipo_calcario2 = st.selectbox("Tipo de calcário Opção B", ["Calcítico", "Dolomítico"])

# Inputs para diesel
st.subheader("Consumo de Diesel")

# Valores de referência de diesel
valores_referencia_diesel = {
    "Aração": 10.0,
    "Gradagem": 8.0,
    "Calagem": 7.0,
    "Gessagem": 6.0,
    "Aplicação de Fertilizantes": 9.0,
    "Aplicação de Defensivos": 12.0,
    "Aplicação de Herbicidas": 12.0,
    "Aplicação de Adubo Foliar": 12.0,
    "No uso da Trincha": 12.0,
    "No uso da Roçadeira": 12.0,
    "Na Colheita Mecanizada": 12.0,
    "Na Colheita Semimecanizada": 12.0,
}


# Função para criar inputs de diesel
def input_diesel(nome):
    usar_referencia = st.checkbox(f"Usar valor de referência para {nome}?")
    if usar_referencia:
        return valores_referencia_diesel[nome]
    else:
        return st.number_input(f"🚜 Consumo de diesel na {nome} (l ha⁻¹)", min_value=0.0, format="%.2f")


# Inputs para diesel
diesel_aracao = input_diesel("Aração")
diesel_gradagem = input_diesel("Gradagem")
diesel_calagem = input_diesel("Calagem")
diesel_gessagem = input_diesel("Gessagem")
diesel_fertilizantes = input_diesel("Aplicação de Fertilizantes")
diesel_defensivos = input_diesel("Aplicação de Defensivos")
diesel_herbicida = input_diesel("Aplicação de Herbicidas")
diesel_adubo_foliar = input_diesel("Aplicação de Adubo Foliar")
diesel_trincha = input_diesel("No uso da Trincha")
diesel_rocadeira = input_diesel("No uso da Roçadeira")
diesel_colheita_mecanizada = input_diesel("Na Colheita Mecanizada")
diesel_colheita_semimecaniada = input_diesel("Na Colheita Semimecanizada")


# Inputs adicionais para a irrigação
st.subheader("Irrigação")

# Valores de referência de diesel e elétrica para irrigação
valores_referencia_irrigacao = {
    "Diesel": 9.0,
    "Elétrica": 12.0,
}

if irrigacao == "Sim":
    col_irrigacao1, col_irrigacao2 = st.columns(2)

    # Escolher tipo de geração
    with col_irrigacao1:
        tipo_geracao = st.selectbox("Tipo de geração de energia para irrigação", ["Diesel", "Elétrica"])

    # Opção para usar valores de referência
    usar_referencia = st.checkbox(f"Usar valor de referência para {tipo_geracao}?")

    if usar_referencia:
        emissoes_irrigacao = valores_referencia_irrigacao[tipo_geracao]
    else:
        if tipo_geracao == "Diesel":
            # Entrada de litros de diesel usados por hectare
            litros_diesel_irrigacao = st.number_input("Consumo de diesel para irrigação (l ha⁻¹ ano⁻¹)", min_value=0.0,
                                                      format="%.2f")

            # Cálculo das emissões usando a função definida
            emissoes_totais_co2eq, emissoes_co2, emissoes_ch4, emissoes_n2o = calcular_emissoes_diesel(
                litros_diesel_irrigacao)
            emissoes_irrigacao = emissoes_totais_co2eq  # Emissões totais em CO₂eq para exibir ou armazenar

        elif tipo_geracao == "Elétrica":
            # Inputs adicionais para o cálculo personalizado (apenas para Elétrica)
            horas_por_dia = st.number_input("Horas de operação da irrigação por dia", min_value=0.0, format="%.2f")
            meses_por_ano = st.number_input("Meses de operação por ano", min_value=0, max_value=12, format="%d")
            dias_por_ano = meses_por_ano * 30  # Aproximação de dias/ano

            # Cálculo das horas úteis por ano
            dias_uteis_por_ano = dias_por_ano  # Aqui pode-se ajustar conforme necessidade
            horas_uteis_por_ano = dias_uteis_por_ano * horas_por_dia

            # Fator de emissão e cálculo das emissões totais para geração elétrica
            fator_emissao_mwh = 0.0385  # Emissões em TCO₂/MWh
            emissoes_irrigacao = (
                        (0.000735499 * horas_uteis_por_ano) * fator_emissao_mwh * 1000)  # Emissões em kg CO₂eq

else:
    emissoes_irrigacao = 0
# Botão para calcular as emissões
if st.button("Calcular Emissões"):

    # Cálculo das emissões para cada operação
    emissoes_aracao = calcular_emissoes_diesel(diesel_aracao)
    emissoes_gradagem = calcular_emissoes_diesel(diesel_gradagem)
    emissoes_calagem = calcular_emissoes_diesel(diesel_calagem)
    emissoes_gessagem = calcular_emissoes_diesel(diesel_gessagem)
    emissoes_fertilizantes = calcular_emissoes_diesel(diesel_fertilizantes)
    emissoes_defensivos = calcular_emissoes_diesel(diesel_defensivos)
    emissoes_herbicida = calcular_emissoes_diesel(diesel_herbicida)
    emissoes_adubo_foliar = calcular_emissoes_diesel(diesel_adubo_foliar)
    emissoes_trincha = calcular_emissoes_diesel(diesel_trincha)
    emissoes_rocadeira = calcular_emissoes_diesel(diesel_rocadeira)
    emissoes_colheita_mecanizada = calcular_emissoes_diesel(diesel_colheita_mecanizada)
    emissoes_colheita_semi_mecanizada = calcular_emissoes_diesel(diesel_colheita_semimecaniada)
    emissoes_totais_diesel =  (emissoes_aracao[0] + emissoes_gradagem[0] +
                                              emissoes_calagem[0] + emissoes_gessagem[0] +
                                              emissoes_fertilizantes[0] + emissoes_defensivos[0] + emissoes_herbicida[0] + emissoes_adubo_foliar[0]+ emissoes_colheita_mecanizada[0] + emissoes_trincha[0] + emissoes_rocadeira[0]+ emissoes_colheita_semi_mecanizada[0])


    # Cálculo das emissões dos fertilizantes e resíduos
    concentracao_n1 = fertilizantes[fertilizante1]
    quantidade_n_fertilizante1 = (concentracao_n1 / 100) * quantidade_fertilizante1
    concentracao_n = fertilizantes[fertilizante2]
    quantidade_n_fertilizante2 = (concentracao_n / 100) * quantidade_fertilizante2
    emissao_fertilizante1 = calcular_emissoes_fertilizante(quantidade_n_fertilizante1)
    emissao_fertilizante2 = calcular_emissoes_fertilizante(quantidade_n_fertilizante2)
    quantidade_n_palha_cafe = quantidade_palha_cafe * (16.8 / 1000)  # Convertendo quilos para quilos de N
    quantidade_n_cama_frango = quantidade_cama_frango * (28.6 / 1000)  # Convertendo quilos para quilos de N
    quantidade_n_esterco = quantidade_esterco * (13.6 / 1000)  # Convertendo quilos para quilos de N
    emissao_palha_cafe = calcular_emissoes_palha_cafe(quantidade_n_palha_cafe)
    emissao_cama_frango = calcular_emissoes_cama_frango(quantidade_n_cama_frango)
    emissao_calcario1 = calcular_emissoes_calcario(quantidade_calcario1, tipo_calcario1)
    emissao_calcario2 = calcular_emissoes_calcario(quantidade_calcario2, tipo_calcario2)
    emissoes_totais_fertilizantes = (emissao_fertilizante1+ emissao_fertilizante2)
    emissoes_totais_calcario = (emissao_calcario1 + emissao_calcario2)

    # Calcular total de emissões sem diesel e sem irrigação
    emissoes_totais_sem_diesel_e_irrigacao = (emissao_fertilizante1 + emissao_fertilizante2 + emissao_calcario1 + emissao_calcario2+
                                              emissao_palha_cafe +
                                              emissao_cama_frango + emissoes_aracao[0] + emissoes_gradagem[0] +
                                              emissoes_calagem[0] + emissoes_gessagem[0] +
                                              emissoes_fertilizantes[0] + emissoes_defensivos[0] + emissoes_herbicida[0] + emissoes_adubo_foliar[0]+ emissoes_colheita_mecanizada[0] + emissoes_trincha[0] + emissoes_rocadeira[0]+ emissoes_colheita_semi_mecanizada[0] + emissoes_irrigacao)


    # Exibir resultados das emissões
    st.subheader("Resultados das Emissões 🌍")
    st.write(f"Emissões Fertilizante Sintético A: {emissao_fertilizante1:.2f} kg CO₂eq")
    st.write(f"Emissões Fertilizante Sintético B: {emissao_fertilizante2:.2f} kg CO₂eq")
    st.write(f"Emissões Palha de Café: {emissao_palha_cafe:.2f} kg CO₂eq")
    st.write(f"Emissões Cama de Frango: {emissao_cama_frango:.2f} kg CO₂eq")
    st.write(f"Emissões Calcário A: {emissao_calcario1:.2f} kg CO₂eq")
    st.write(f"Emissões Calcário B: {emissao_calcario2:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Aração: {emissoes_aracao[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Gradagem: {emissoes_gradagem[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Calagem: {emissoes_calagem[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Gessagem: {emissoes_gessagem[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Fertilizantes: {emissoes_fertilizantes[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Aplicação de Defensivos: {emissoes_defensivos[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Aplicação de Herbicidas : {emissoes_herbicida[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Aplicação de Adubo Foliar : {emissoes_adubo_foliar[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel no Uso da Trincha : {emissoes_trincha[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel no Uso da Roçadeira : {emissoes_rocadeira[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Colheita Mecanizada : {emissoes_colheita_mecanizada[0]:.2f} kg CO₂eq")
    st.write(f"Emissões Do Consumo do Diesel na Colheita Semi Mecanizada : {emissoes_colheita_semi_mecanizada[0]:.2f} kg CO₂eq")
    st.write(f"Emissões da irrigação: {emissoes_irrigacao:.2f} kg CO₂eq")
    st.write(f"Emissões Totais: {emissoes_totais_sem_diesel_e_irrigacao:.2f} kg CO₂eq")

    # Somando as emissões totais
    emissoes_totais_grafico = [
        emissoes_totais_fertilizantes,
        emissoes_totais_calcario,
        emissao_palha_cafe,
        emissao_cama_frango,
        emissoes_totais_diesel,
        emissoes_irrigacao,
    ]

    # Categorias correspondentes para o gráfico
    categorias = [
        "Fertilizante Sintético",
        "Calcário",
        "Palha de Café",
        "Cama de Frango",
        "Diesel",
        "Irrigação"
    ]

    # Gerando o gráfico de pizza aprimorado
    fig, ax = plt.subplots(figsize=(12, 10))  # Aumentando ainda mais o tamanho do gráfico
    wedges, texts, autotexts = ax.pie(
        emissoes_totais_grafico,
        labels=categorias,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors,
        textprops={'color': "black", 'fontsize': 14},  # Fonte dos rótulos ajustada
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},  # Borda branca mais espessa
    )

    # Ajustando estilo dos textos do gráfico
    for text in texts:
        text.set_fontsize(14)  # Aumentando o tamanho dos rótulos

    for autotext in autotexts:
        autotext.set_color('white')  # Cor branca nas porcentagens
        autotext.set_fontweight('bold')  # Negrito nas porcentagens
        autotext.set_fontsize(14)  # Aumentando o tamanho das porcentagens

    # Adicionando um título central ao gráfico
    ax.set_title("Distribuição das Emissões de Carbono", fontsize=18, weight='bold', pad=30)

    # Garantir que o gráfico seja circular
    ax.axis('equal')

    # Adicionando uma legenda proporcional
    ax.legend(
        wedges,
        categorias,
        title="Categorias",
        loc="center left",
        bbox_to_anchor=(1.2, 0.5),  # Posicionando a legenda fora do gráfico
        fontsize=14,  # Aumentando tamanho das fontes na legenda
        title_fontsize=16  # Título da legenda maior
    )

    # Ajustando o layout para evitar cortes ou sobreposições
    plt.subplots_adjust(left=0.1, right=0.85)  # Ajuste de margens para legenda e gráfico

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)
