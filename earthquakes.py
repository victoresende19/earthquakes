###############################################################################################################################################################################################################
#                                                                                               Bibliotecas
###############################################################################################################################################################################################################
import datetime
import time
from turtle import width
import streamlit as st

import pandas as pd
import urllib.request
import json
import plotly.express as px
import plotly.graph_objects as go

###############################################################################################################################################################################################################
#                                                                                                           Funções
###############################################################################################################################################################################################################
def Tema():
    #CURRENT_THEME = "blue"
    IS_DARK_THEME = True
    THEMES = [
        "light",
        "dark",
        "green",
        "blue",
    ]
    return IS_DARK_THEME, THEMES

#Funcao barra progresso
def Progresso():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center;'>Carregando...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

# Funcao metricas
def Metricas(df):
    col1, col2, col3 = st.columns(3)
    col1.write("")
    col2.metric("Magnitude Média", df.Magnitude.mean())
    col3.write("")

# Funcao plotar mapa 
def Mapa(regiao, df):
    if df.shape[0] !=0:
        mapa = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                            projection=projecoes, color_continuous_scale=['#04290d', 'yellow', 'red'],
                            animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope=regiao, width=900, height=600)
        # Fazendo com que as fronteiras aparecam
        mapa.update_geos(showcountries=True)

        if regiao == 'world':
            # Ajustando rotacao do globo
            mapa.layout.geo.projection = {'rotation': {'lon': 200}, 'type': projecoes}

    else:
        mapa = st.warning('Não existem dados para os filtros aplicados')
        mapa = go.Figure()

    return mapa

###############################################################################################################################################################################################################
#                                                                                       Inicio da página Streamlit - Input dos dados
###############################################################################################################################################################################################################
Tema()
st.set_page_config(layout="wide", initial_sidebar_state='expanded')
st.sidebar.markdown("<h1 style='text-align: center;'>Filtros de pesquisa</h1>",
            unsafe_allow_html=True)
projeto = st.sidebar.selectbox('Projeto', ('Documentação', 'Mapas'))

if projeto == 'Documentação':
    #Dividindo a pagina em tres colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<p align='justify';'>
                Os fenômenos naturais se referem a toda ação da natureza que não ocorre a partir de intervenção humana. Consequentemente, com o passar dos anos a humanidade têm trabalhado e estudado os motivos que geram tais fenômenos, principalmente por meio da coleta e análise de dados gerados por sensores que monitoram possíveis regiões afetadas.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                Sismologia é o estudo dos sismos (ou terremotos) e, genericamente, dos diversos movimentos que ocorrem na superfície do globo terrestre. Esta ciência busca conhecer e determinar em que circunstâncias ocorrem os sismos naturais assim como suas causas, de modo a prevê-los em tempo e espaço. Portanto, por meio dessa ciência, é possível analisar dados gerados de diversos observatórios sismológicos e sensores sismógrafos a fim de entender os tremores terrestres, as causas e impactos diretos na sociedade, havendo até a possibilidade de prevê-los em alguns casos dependendo dos dados gerados.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.image("https://images.theconversation.com/files/79512/original/image-20150427-18167-1q17be7.png?ixlib=rb-1.1.0&q=45&auto=format&w=754&fit=clip", 
                caption = 'Ilustração onde as placas tectônicas deslizam umas sob as outras.')
        #st.image("http://1.bp.blogspot.com/-L7wY8A1k-A0/VNeuLj8LZ_I/AAAAAAAAAgE/TlJZTJyzPyI/s1600/hipocentro%2Be%2Bepicentro.gif", width = 400)

    #Utilizando apenas a coluna do meio pois é centralizada
    with col2:
        st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>",
            unsafe_allow_html=True)
        st.image("https://spedigital.editorapositivo.com.br/IMP/72/CLA191/img/SPE_EF2_CIE_72_M002-mundo_placas_tectonicas.png",
                    caption = 'Ilustração das placas tectônicas no planeta.')
        st.markdown("""<p align='justify';'>
                Com o passar dos anos e o avanço da tecnologia, houve a criação e implementação de sensores em locais com risco de desastres naturais para a verificação de riscos e coleta dos dados. Dessa forma, uma vasta quantidade de dados é gerada diariamente, principalmente quando há situações de tremores, seja em razão de terremotos, erupções, ou até mesmo de ações humanas como acontece em alguns tipos de explosões. Portanto, a criação de um observatório sobre tremores e a predição da magnitude de determinada vibração terrestre, dado a localidade (Por meio da latitude e longitude), torna-se interessante para o monitoramento de tais fenômenos.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                A referência mundial em relação ao monitoramento global de tremores terrestre acontece por meio do Serviço Geológico dos Estados Unidos (USGS). Dessa forma, em seu site é disponibilizado uma API pública para a consulta dos dados, do qual pode ser acessada por diversas formas.</p>""",
                unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<p align='justify';'>
                Esse projeto utiliza ferramentas de mineração, coleta, visualização dos dados, criação de modelos preditivos e implementação. Os dados utilizados nos mapas a seguir são oriundos de uma API disponibilizada pelo Serviço Geológico dos Estados Unidos (USGS). A etapa de coleta dos dados foi realizado por meio da linguagem de programação Python, da qual se arquitetou o tratamento dos dados para a extração das variáveis pertinentes. Da mesma forma, a etapa de visualização dos dados e implementação se desenvolveram por meio da linguagem Python.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                Esse estudo utiliza dados da API pública citada em formato JSON, coletando dados de tremores que tiveram magnitude maior ou igual a 2. Vale ressaltar que a API possui um limite de apenas 20.000 registros por requisição. Consequentemente, será necessário fazer mais de uma consulta para coletar todos os dados do período citado na introdução.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify';'></p>""", unsafe_allow_html=True)
        st.image("https://ndma.gov.in/kids/images/img-4.png", width = 500, caption = 'Ilustração pós sismo.')
    

if projeto == 'Mapas':
    startTime = st.sidebar.date_input(
        "Data inicial (ano/mês/dia):", datetime.date(2021, 1, 1), min_value = datetime.date(1960, 1, 1))

    endTime = st.sidebar.date_input(
        "Data final (ano/mês/dia):", datetime.date(2022, 6, 10), min_value = datetime.date(1960, 1, 1))

    magMinima = 4
    magnitude_desejada = st.sidebar.slider('Magnitude mínima:', magMinima, 10, 5)

    paginaContinentes = st.sidebar.selectbox('Selecione a região de pesquisa', [
                                            'world', 'africa', 'north america', 'south america', 'asia', 'europe'])

    visualizacaoTremor = st.sidebar.selectbox(
        'Tipo de tremor:', ('Terremoto', 'Explosão', 'Explosão Nuclear', 'Explosão de rochas', 'Explosão de pedreira'))

    visualizacaoPeriodo = st.sidebar.selectbox('Visualização por ano:', ('Não', 'Sim'))

    projecoes = st.sidebar.selectbox(
        'Tipo de projeção:',
        ('natural earth', 'mercator', 'equirectangular', 'orthographic', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
        'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'))  

    resultado = st.sidebar.button('Aplicar')

###############################################################################################################################################################################################################
#                                                                                       Manipulação dos dados
###############################################################################################################################################################################################################
    # Acessando a API de maneira dinâmica utilizando os inputs do usuário
    @st.cache(show_spinner = False)
    def Dados(startTime, endTime, magnitude_desejada):
        url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startTime}&endtime={endTime}&minmagnitude={magnitude_desejada}&limit=20000'
        response = urllib.request.urlopen(url).read()
        data = json.loads(response.decode('utf-8'))
        return data
    
    data = Dados(startTime, endTime, magnitude_desejada)
    Progresso().empty()
###############################################################################################################################################################################################################
    # Extraindo variáveis do JSON
    magnitude = []

    for mag in data['features']:
        magnitude.append(mag['properties']['mag'])

    tipoTerremoto = []

    for tipo in data['features']:
        tipoTerremoto.append(tipo['properties']['type'])

    alerta = []

    for alert in data['features']:
        alerta.append(alert['properties']['alert'])

    latitude = []

    for lat in data['features']:
        latitude.append(lat['geometry']['coordinates'][1])

    longitude = []

    for lon in data['features']:
        longitude.append(lon['geometry']['coordinates'][0])

    timestamp = []

    for time in data['features']:
        timestamp.append(time['properties']['time'])

    # Criando data frame com as variáveis em lista
    dicionario_geral = {'Magnitude': magnitude, 'Timestamp': timestamp,
                        'Tipo': tipoTerremoto, 'Alerta': alerta,
                        'Latitude': latitude, 'Longitude': longitude}       
    df = pd.DataFrame.from_dict(dicionario_geral)

    # Ajustando variáveis de data/tempo
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='ms')
    df['Year'] = pd.to_datetime(df.Timestamp).dt.year
    df = df.sort_values(by=['Year'], ascending=True)

    # Renomeando observações

    # Variável Tipo
    mapping_tipo = {"Tipo": {'earthquake': 'Terremoto', 'explosion': 'Explosão', 'nuclear explosion':
                            'Explosão Nuclear', 'rock burst': 'Explosão de rochas', 'quarry blast': 'Explosão de pedreira'}}
    df = df.replace(mapping_tipo)

    df = df[df.Tipo == visualizacaoTremor]

###############################################################################################################################################################################################################
#                                                                                      Demonstração dos gráficos após os inputs
###############################################################################################################################################################################################################
    dataInicio = startTime.strftime("%d/%m/%Y")
    dataFim = endTime.strftime("%d/%m/%Y")

    #Título da pagina
    st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>",
                unsafe_allow_html=True)

    #Título gráfico
    #st.markdown(f"<h2 style='text-align: center;'>Visualização interativa dos {df.shape[0]} primeiros tremores</h2>",
    #            unsafe_allow_html=True)

    #Data utilizada
    st.markdown(f"<h4 style='text-align: center; font-size:16px'>{dataInicio} a {dataFim}</h4>",
                    unsafe_allow_html=True)
    
    #Metricas
    #Metricas(df)
    
    #Mapa
    st.plotly_chart(Mapa(paginaContinentes, df), use_container_width=True)

    #Observacoes
    st.markdown(f"<p style='text-align: center; font-size:16px'> <strong>Obs:</strong> A quantidade de dados pesquisados pode afetar no tempo de execução da visualização.</p>",
                    unsafe_allow_html=True)

    #Volume dos dados
    st.markdown(f"<h4 style='text-align: center; font-size:16px'>Volume de dados pesquisados ({df.shape[0]})</h4>",
                    unsafe_allow_html=True)