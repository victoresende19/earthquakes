from utils.model import previsao
from utils.map import mapa, regioes, projecoes_mapa
from utils.etl import coleta_dados, manipula_dados, tipo_eventos
import pytz
import datetime
import numpy as np
import streamlit as st

st.set_page_config(layout="wide", page_icon='🌎', page_title='SismoMap')
st.markdown(
    """
    <style>
    .stApp, .css-12ttj6m, .e8zbici2{
        background: linear-gradient( 109.6deg,  rgba(5,84,94,1) 16%, #bbb 91.1% );
    }
    .css-9q76rl, .css-1z8u7d{
        background-color: #033940;
    }
    .st-bp, .st-br, st.css-9q76rl, .css-pav9s7, .css-9rexhf{
        background: #0000
    }
    p{
        font-size: 20px !important;
        color: #fff
    }
    a {
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align: left; font-size:52px; color: white'>SismoMap</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align: left; font-size:16px'>Descubra, pesquise e preveja terremotos de forma fácil, exclusiva e personalizada!</p><br><br>", unsafe_allow_html=True)
mapa_sismos, predict, doc = st.tabs(["Mapa", "Predição magnitude", "Documentação"])

with mapa_sismos:
    st.markdown("<h5 style='text-align: left;  color: white;'><br>Caso deseje, aplique os filtros:</h5>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col2:
        st.write('')
    
    with col1:
        with st.form(key='my_form_map'):
            with st.expander("Filtros"):
                col1, col2 = st.columns(2)

                with col1:
                    startTime = st.date_input("Data inicial (ano/mês/dia):", datetime.datetime.now(pytz.timezone('America/Sao_Paulo')) - datetime.timedelta(weeks=4))
                    visualizacaoPeriodo = st.selectbox('Visualização por ano:', ('Não', 'Sim'))

                magMinima = 3
                magnitudeUsuario = st.slider('Magnitude mínima:', magMinima, 10, 4)

                with col2:
                    endTime = st.date_input("Data final (ano/mês/dia):", datetime.datetime.now(pytz.timezone('America/Sao_Paulo')) )
                    visualizacaoTremor = st.selectbox('Tipo de tremor:', list(tipo_eventos.keys()))

            data = coleta_dados(startTime, endTime, magnitudeUsuario, visualizacaoTremor)
            terremotos = manipula_dados(data)
            submit_button = st.form_submit_button(label='Encontrar terremotos 💥')
    
    with col3:
        st.write('')

    if len(terremotos) == 20000 and startTime.strftime('%m/%d/%Y - %H:%M') != terremotos['Timestamp'].iloc[-1]:
        st.markdown(f"<br><h5 style='text-align: center;'>Devido a quantidade máxima de pesquisa de 20.0000 terremotos ter sido atingida, foram encontrados sismos na data de {startTime.strftime('%d/%m/%Y')} até {terremotos['Timestamp'].iloc[-1]} </h5>", unsafe_allow_html=True)
    else:
        st.markdown(f"<br><h4 style='text-align: center; color: white'>Foram encontrados {len(terremotos)} terremotos na data de {startTime.strftime('%d/%m/%Y')} a {endTime.strftime('%d/%m/%Y')}</h4>", unsafe_allow_html=True)
    
    if len(terremotos):
        st.plotly_chart(mapa(data=terremotos, visualizacaoPeriodo=visualizacaoPeriodo), use_container_width=True)
    else:
        st.warning('Não existem dados para os filtros aplicados')

    # st.markdown(f"<h4 style='text-align: center; font-size:16px'>Quantidade de terremotos: {terremotos.shape[0]}</h4>", unsafe_allow_html=True)
    # st.markdown("<p style='text-align: left; font-size:16px; color:red'><strong>Observação (1):</strong> Apesar do range de dados escolhido, a aplicação considera apenas os 20.000 primeiros dados referente a data de início.</p>", unsafe_allow_html=True)
    # st.markdown("<p style='text-align: left; font-size:16px; color:red'> <strong>Observação (2):</strong> A quantidade de dados pesquisados pode afetar no tempo de execução da visualização.</p>", unsafe_allow_html=True)


with predict:
    # st.markdown("<h1 style='text-align: center; color: white;'>Previsão magnitude de terremotos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: white;'>Como exposto por Geller (1997), terremotos são desastres praticamente impossíveis de se prever dada sua natureza incerta. Entretanto, Mondol (2021) apresenta um estudo sobre variáveis e métodos para previsão da magnitude de um terremoto. Nesse último, o algoritmo de floresta aleatória obteve resultados interessantes quando alimentado por dados sobre profundidade dos terremotos.  </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: white;'>Portanto, ao verificar a correlação e a literatura, decidiu-se que as variáveis de longitude e profundidade do epicentro (em km) são as que possuem melhor resultado na predição de um tremor. Dessa forma, o modelo utilizado para tal chama-se <strong>floresta aleatória</strong>, um método não-linear do qual utiliza um agregado de árvores de decisão para assim prever a magnitude do terremoto. Abaixo estão disponibilizados os filtros citado para fazer a previsão da magnitude do terremoto.</p>", unsafe_allow_html=True)
    st.write('')
    st.markdown("<h5 style='text-align: left; color: white'>Caso deseje, aplique os filtros:</h5>", unsafe_allow_html=True)
    with st.form(key='my_form_predict'):
        col1, col2, col3 = st.columns(3)

        with col1:
            latitude = st.slider('Latitude: ', min_value=-90.0, max_value=180.0, value=90.0)

        with col2:
            longitude = st.slider('Longitude: ', min_value=-180.0, max_value=180.0, value=142.0)

        with col3:
            profundidade = st.slider('Profundidade: ', min_value=5.0, max_value=500.0, value=15.0)
            
        submit_button = st.form_submit_button(label='Aplicar filtros')

    st.markdown("<p style='text-align: left; color: #02292e;'><strong>Observação (1)</strong>: A previsão é realizada com base em uma amostra representativa dos dados.</p>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: justify; color: white;'>Caso o terremoto ocorresse em uma latitude de {latitude}, longitude de {longitude}, e o epicentro estiver a uma profundidade de {profundidade} km, a magnitude estimada desse tremor seria: </h4>", unsafe_allow_html=True)
    previsao = previsao(latitude, longitude, profundidade)
    st.markdown(f"<h3 style='text-align: center; color: black;'>{round(previsao[0], 2)} graus na escala Ritcher </h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: white;'>A métrica utilizada para a avaliação da floresta aleatória foi o R², ou coeficiente de determinação, do qual demonstra quão explicativo o modelo é, variando entre 0 a 1. Como consta na documentação do projeto, o R² referente ao conjunto de dados utilizado como treinamento chegou a 0.72. Além disso, a métrica MAPE foi de 0.11, o que significa dizer que a precisão do modelo é cerca de 89% nas respectivas previsões.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: #02292e;'><br><br><strong>Referências</strong> </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify;'><a href='http://essay.utwente.nl/87313/' style='color: #02292e'>[1] Manaswi Mondol. Analysis and prediction of earthquakes using different machine learning techniques. B.S. thesis, University of Twente, 2021.</a> </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify;'><a href='https://www.scec.org/publication/404' style='color: #02292e'>[2] Robert J Geller, David D Jackson, Yan Y Kagan, and Francesco Mulargia. Earthquakes cannot be predicted. Science, 275(5306):1616–1616, 1997</a> </p>", unsafe_allow_html=True)


with doc:
    # st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/4tnS9bb/imagem-terremoto-lisboa.png", caption='Ilustração da cidade de Lisboa após o terremoto em 1755')

    doc1, doc2, doc3 = st.columns(3)
    with doc1:
        st.markdown("""<p align='justify';'> Fenômenos naturais desencadeados por terremotos ocorrem desde a formação do nosso planeta. Ao longo dos séculos, a humanidade enfrentou as consequências devastadoras desses eventos, que podem resultar em perdas de vidas, alterações significativas nas paisagens e muitos outros impactos. No entanto, foi somente após o terremoto que arrasou Lisboa em 1755, considerado um dos terremotos mais intensos já registrados na Europa, que a análise científica dos terremotos verdadeiramente teve início. De acordo com sismólogos modernos, esse tremor atingiu uma magnitude de 9 na escala Richter, desencadeando um tsunami e ceifando a vida de aproximadamente 100 mil pessoas. Uma das consequências marcantes desse cataclismo foi o despertar do interesse pela sismologia, uma ciência que, até aquele momento, permanecia relativamente pouco explorada. </p>""", unsafe_allow_html=True)
        
    with doc2:
        st.markdown("""<p align='justify';'> A sismologia visa o estudo dos sismos (ou terremotos) e, genericamente, dos diversos movimentos que ocorrem na superfície do globo terrestre. Esta ciência busca conhecer e determinar em que circunstâncias ocorrem os sismos naturais assim como suas causas, de modo a prevê-los em tempo e espaço. Portanto, por meio dessa ciência, é possível analisar dados gerados de diversos observatórios sismológicos e sensores sismógrafos a fim de entender os tremores terrestres, as causas e impactos diretos na sociedade, havendo até a possibilidade de prevê-los em alguns casos dependendo dos dados gerados. Assim, o SismoMap empenha-se em contribuir para a democratização da visualização de tremores e estimativa das magnitudes dos sismos por meio de modelos estatísticos avançados e vigorosos métodos computacionais..</p>""", unsafe_allow_html=True)

    with doc3:
        st.markdown("""<p align='justify';'>A referência mundial em relação ao monitoramento global de tremores terrestre acontece por meio do Serviço Geológico dos Estados Unidos (USGS). Dessa forma, a plataforma consulta uma API pública para a coleta dos dados, do qual pode ser acessada por diversas formas. Portanto, o SismoMap faz a consulta dos dados de acordo com os filtros aplicados. Vale ressaltar que a API citada possui um limite de 20.000 dados por requisição, caso os filtros excedam esse limite, são coletados apenas os primeiros 20.000 sismos referente as datas escolhidas. Para a melhor experiência do usuário e coleta dos dados referentes aos terremotos, foi fixado o limite de terremotos com magnitude mínima igual a 3 graus na escala Ritcher, não sendo possível visualizar sismos menores.</p>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div><br><br><br> 
        <a href = "https://github.com/victoresende19/earthquakes" style='color: white;'>Documentação&nbspoficial&nbspe&nbspcódigo-fonte </a> 
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div>
    <a href = "https://github.com/victoresende19" style='color: white;'> &copy2023 &nbsp-&nbspVictor Augusto Souza Resende </a>
</div>
""", unsafe_allow_html=True)