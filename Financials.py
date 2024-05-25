import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import io
import requests
from io import BytesIO
import urllib.request
from soccerplots.radar_chart import Radar
import matplotlib.colors as mcolors
from scipy.stats import pearsonr

# Setup our colours
color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
'#008941', '#006FA6', '#A30059','#FFDBE5', '#7A4900',
'#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF',
'#997D87', '#5A0007', '#809693', '#FEFFE6', '#1B4400',
'#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A',
'#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9',
'#B903AA', '#D16100', '#DDEFFF', '#000035', '#7B4F4B',
'#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
'#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744',
'#C0B9B2', '#C2FF99', '#001E09', '#00489C', '#6F0062',
'#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1',
'#788D66', '#885578', '#FAD09F', '#FF8A9A', '#D157A0',
'#BEC459', '#456648', '#0086ED', '#886F4C', '#34362D',
'#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9',
'#FF913F', '#938A81', '#575329', '#00FECF', '#B05B6F',
'#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
'#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C',
'#772600', '#D790FF', '#9B9700', '#549E79', '#FFF69F',
'#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465',
'#922329', '#5B4534', '#FDE8DC', '#404E55', '#0089A3',
'#CB7E98', '#A4E804', '#324E72', '#6A3A4C'
]


club_image_paths = {'América': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/America.png',
              'Athletico': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Athletico.png',
              'Atlético': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Atletico.png',
              'Bahia': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Bahia.png',
              'Botafogo': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Botafogo.png',
              'Corinthians': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Corinthians.png',
              'Coritiba': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Coritiba.png',
              'Cruzeiro': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cruzeiro.png',
              'Cuiabá': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cuiaba.png',
              'Flamengo': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Flamengo.png',
              'Fluminense': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fluminense.png',
              'Fortaleza': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fortaleza.png',
              'Goiás': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Goias.png',
              'Grêmio': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Gremio.png',
              'Internacional': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Internacional.png',
              'Palmeiras': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Palmeiras.png',
              #'Red Bull': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/RedBull.png',
              'Santos': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Santos.png',
              'São Paulo': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/SaoPaulo.png',
              'Vasco': 'https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Vasco.png'}


# Loading base file
df = pd.read_csv("resultado.csv")
df1 = pd.read_csv("índices.csv")
df2 = pd.read_csv("caixa.csv")
df3 = pd.read_csv("Painel_Cte.csv")
df4 = pd.read_csv("Transparência.csv")
df5 = pd.read_csv("Transparência (2).csv")
df6 = pd.read_csv("Painel_Cte (2).csv")

clubs = pd.read_csv("clubes.csv")
alt_clubs = pd.read_csv("alt_clubes.csv")

# Defining clubes
clubes = ["América", "Athletico", "Atlético", "Bahia", "Botafogo", 
          "Corinthians", "Coritiba", "Cruzeiro", "Cuiabá", "Flamengo", 
          "Fluminense", "Fortaleza", "Grêmio", "Goiás", "Internacional", 
          "Palmeiras", "Santos", "São Paulo", "Vasco"]

# Defining labels_resultado
label = ["Direitos de transmissão", "Publicidade e patrocínio", "Arrecadação de jogos", 
         "Sócio-torcedor", "Premiações", "Licenciamento da marca", "RECEITA RECORRENTE", 
         "Negociação de atletas", "Outras receitas", "RECEITA OPERACIONAL LÍQUIDA", 
         "Pessoal e encargos sociais", "Direitos de imagem", "Despesas com jogos", 
         "Despesas gerais e administrativas", "Depreciação e amortização", "Outras despesas", 
         "DESPESAS", "RESULTADO OPERACIONAL", "Resultado financeiro", "RESULTADO", "Venda de Direitos - Liga Forte",
         "Outras Despesas Operacionais"]

# Defining labels_caixa
label_caixa = ["Direitos de transmissão", "Publicidade e patrocínio", "Arrecadação de jogos", 
         "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas", 
         "GERAÇÃO DE CAIXA TOTAL", "SAÍDAS DE CAIXA OPERACIONAIS", "Pessoal e encargos sociais", 
         "Direitos de imagem", "Despesas com jogos", "Despesas gerais e administrativas", 
         "Outras despesas", "Ajuste na Geração de Caixa Operacional", "GERAÇÃO DE CAIXA OPERACIONAL", 
         "CAIXA DESTINADO A INVESTIMENTOS", "Compra de Jogadores", "Compra de Imobilizado", "Outras", 
         "CAIXA DESTINADO A FINANCIAMENTOS", "AUMENTO/DIMINUIÇÃO DE CAIXA"]

# Defining temas contábeis
temas_cont = ["Receita c/ Direitos de Transmissão", "Receita c/ Transmissão + Premiações", "Receita c/ Publicidade e patrocínio", 
         "Receita de Match-Day", "Receita c/ Sócio-torcedor", "Premiações", 
         "Receita c/ Licenciamento da marca", "Receita Recorrente", "Receita c/ Negociação de Atletas", 
         "Receita Operacional Líquida", "Resultado", "Dívida", "Despesas gerais e administrativas"]

# Defining temas esportivos
temas_esport = ["Folha do futebol", "Aquisições de atletas", "Gastos com a Base", 
                 "Base de Torcedores", "Pontuação Série A", "Bilheteria Série A (R$ milhões)", 
                 "Bilheteria média (R$ mil/jogo)", "Público Médio (pagantes)", "Sócios-Torcedores", 
                 "Valor do Elenco (€ milhões)"]

# Defining temas gerenciais
temas_ger = ["Folha do futebol / Receita Operacional Líquida", "Folha futebol + Compra jogadores / Rec Oper Líquida",
             "Público Médio / Sócios-Torcedores", "Receita Operacional Líquida / Base de Torcedores", 
             "Receita Operacional Líquida / Sócios Torcedores", 
             "Receita com Venda de Direitos Econômicos / Gastos com a Base", 
             "Receita com Venda de Direitos Econômicos / Pontuação Série A", 
             "Receita com Premiação / Folha do Futebol", "Folha do futebol / Pontuação Série A", 
             "Receita Operacional Líquida / Pontuação Série A", "Receita c/ Pay-per-View", 
             "Dívida / Receita Operacional Líquida",
             "Despesas Administrativas / Folha do Futebol" 
             ]

# Defining temas
temas_y = ["Pontuação Série A", "Performance Série A", 
           "Receita c/ Match-Day", "Receita c/ Sócio-torcedor", "Premiações", 
           "Bilheteria média Série A (R$ mil/jogo)", "Público Médio (pagantes)", 
           "Sócios-Torcedores", "Resultado", "Bilheteria Série A (R$ milhões)"            
           ]

# Defining temas
temas_x = ["Receita c/ Direitos de transmissão", "Folha do futebol", "Base de Torcedores", 
           "Dívida", "Aquisições de atletas", "Gastos com a Base", "Receita c/ Negociação de atletas", 
           "Receita Operacional Líquida", "Valor do Elenco (€ milhões)", "PIB do Estado (R bilhões)", 
           "Receita c/ Publicidade e patrocínio", "Receita c/ Match-Day", "Receita c/ Transmissão + Premiações"
           ]

st.markdown("<h4 style='text-align: center;  color: black;'>Almanaque Financeiro da Série A<br>2023 </b></h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;  color: black;'>app by @JAmerico1898 </b></h6>", unsafe_allow_html=True)
st.markdown("---")


with st.sidebar:

    mobile_styles = """
    <style>
    @media (max-width: 640px) {
        .css-1d391kg { /* Adjust the class according to your actual rendered HTML */
            padding: 0 !important;
            font-size: 12px !important;
        }
    }
    </style>
    """
    st.markdown(mobile_styles, unsafe_allow_html=True)


    choose = option_menu("Análises:", ["Análise Individual - 2023", "Análise Individual - Histórica", 
                                                    "Análise Comparativa Univariada", "Análise Comparativa Bivariada", "Compare 2 clubes!",
                                                    "Índice de Transparência", "Metodologia da Análise"],
                                icons=['graph-up-arrow', 'zoom-in', 'binoculars', 'magic', 'magic', 'brightness-high', 'book'],
                                menu_icon="universal-access", default_index=0,
                                styles={
                                "container": {"padding": "4!important", "background-color": "#fafafa"},
                                "icon": {"color": "orange", "font-size": "18px"},
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#02ab21"},    
                                }
                                )    

###############################################################################################################################

if choose == "Compare 2 clubes!":
    fontsize = 24
    clube1 = st.selectbox("Escolha o primeiro Clube", options=clubes, index=None, placeholder="Escolha o primeiro Clube!")
    clube2 = st.selectbox("Escolha o segundo Clube", options=clubes, index=None, placeholder="Escolha o segundo Clube!")

    if clube1 and clube2:

        if (df1.at[4, clube1] == 0) or (df1.at[4, clube2] == 0):

            #Plotting Headline
            headline = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube1} x {clube2}</div>"
            st.markdown("<h4 style='text-align: center;'>Comparativo dos Principais Indicadores</h4>", unsafe_allow_html=True)
            st.markdown(headline, unsafe_allow_html=True)

            dfb = df1.iloc[np.r_[0:6, 7, 9, 22, 26], np.r_[0:21]]
            dfb_transposed = dfb.T
            # Set the first row as the new header
            dfb_transposed.columns = dfb_transposed.iloc[0]
            # Drop the first row
            dfb_transposed = dfb_transposed.iloc[1:]
            # Rename the first column to 'clubs'
            dfb_transposed.index.name = 'Clubes'
            dfb = dfb_transposed
            # Renaming Columns
            dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                    "Receita c/ Match-Day": "Match-Day",
                                    "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                    "Receita c/ Negociação de atletas": "Venda de jogadores",
                                    "Receita c/ Transmissão + Premiações": "TV + Premiações",
                                    "Receita c/ Licenciamento da marca": "Licenciamento",
                                    "Receita Operacional Líquida": "Rec Oper Líquida" 
                                    })
            
            # Preparing the Graph
            params = list(dfb.columns)
            params = params[0:]
            #Preparing Data
            ranges = []
            a_values = []
            b_values = []

            for x in params:
                a = min(dfb[params][x])
                a = a
                b = max(dfb[params][x])
                b = b
                ranges.append((a, b))

            for x in range(len(dfb.index)):
                if dfb.index[x] == clube1:
                    a_values = dfb.iloc[x].values.tolist()
                if dfb.index[x] == clube2:
                    b_values = dfb.iloc[x].values.tolist()
                                        
            a_values = a_values[0:]
            b_values = b_values[0:]

            # Rounding values to no decimal places
            a_values = [round(value) for value in a_values]
            b_values = [round(value) for value in b_values]

            values = [a_values, b_values]

            #Plotting Data
            title = dict(
                title_name = clube1,
                title_color = '#B6282F',
                subtitle_name = "(R$ milhões)",
                subtitle_color = '#B6282F',
                title_name_2 = clube2,
                title_color_2 = '#344D94',
                subtitle_name_2 = "(R$ milhões)",
                subtitle_color_2 = '#344D94',
                title_fontsize = 18,
            ) 

            ## instantiate object
            radar = Radar()

            ## instantiate object -- changing fontsize
            radar=Radar(fontfamily='Cursive', range_fontsize=14)
            radar=Radar(fontfamily='Cursive', label_fontsize=14)

            fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
            st.pyplot(fig)





        elif (df1.at[4, clube1] != 0) or (df1.at[4, clube2] != 0):

            dfb = df1.iloc[np.r_[47, 1:6, 7, 9, 22, 26], np.r_[0:21]]
            dfb_transposed = dfb.T
            # Set the first row as the new header
            dfb_transposed.columns = dfb_transposed.iloc[0]
            # Drop the first row
            dfb_transposed = dfb_transposed.iloc[1:]
            # Rename the first column to 'clubs'
            dfb_transposed.index.name = 'Clubes'
            dfb = dfb_transposed
            # Renaming Columns
            dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                    "Receita c/ Match-Day": "Match-Day",
                                    "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                    "Receita c/ Negociação de atletas": "Venda de jogadores",
                                    "Receita c/ Direitos de transmissão": "Direitos de TV",
                                    "Receita c/ Licenciamento da marca": "Licenciamento",
                                    "Receita Operacional Líquida": "Rec Oper Líquida" 
                                    })
            
            # Preparing the Graph
            params = list(dfb.columns)
            params = params[0:]
            #Preparing Data
            ranges = []
            a_values = []
            b_values = []

            for x in params:
                a = min(dfb[params][x])
                a = a
                b = max(dfb[params][x])
                b = b
                ranges.append((a, b))

            for x in range(len(dfb.index)):
                if dfb.index[x] == clube1:
                    a_values = dfb.iloc[x].values.tolist()
                if dfb.index[x] == clube2:
                    b_values = dfb.iloc[x].values.tolist()
                                        
            a_values = a_values[0:]
            b_values = b_values[0:]

            # Rounding values to no decimal places
            a_values = [round(value) for value in a_values]
            b_values = [round(value) for value in b_values]

            values = [a_values, b_values]

            #Plotting Data
            title = dict(
                title_name = clube1,
                title_color = '#B6282F',
                subtitle_name = "(R$ milhões)",
                subtitle_color = '#B6282F',
                title_name_2 = clube2,
                title_color_2 = '#344D94',
                subtitle_name_2 = "(R$ milhões)",
                subtitle_color_2 = '#344D94',
                title_fontsize = 18,
            ) 

            ## instantiate object
            radar = Radar()

            ## instantiate object -- changing fontsize
            radar=Radar(fontfamily='Cursive', range_fontsize=14)
            radar=Radar(fontfamily='Cursive', label_fontsize=14)

            fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
            st.pyplot(fig)















if choose == "Análise Individual - 2023":
    clube = st.selectbox("Escolha o Clube", options=clubes, index=None, placeholder="Escolha o Clube!")
    fontsize = 24
    if clube == "Palmeiras":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 8,  9,  9, 16, 16, 16, 16, 16, 16, 17, 17] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19], np.r_[16]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[16]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15,   0.15, 0.15, 0.15, 0.15, 0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60,  0.85, 0.95, 0.95]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.13, 0.20, 0.40, 0.00, -0.05, 0.20, 0.35, 0.50, 0.80, 0.65, 0.20, -0.20, -0.20, 0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'lime', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.295, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.08, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=1.02, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.15, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=1.04, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.36, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.27, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.16, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.835, y=0.10, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.80, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.87, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.01, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.97, y=0.96, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Palmeiras.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14, 15, 15, 15, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13,  8, 16, 20, 21, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 21, 17, 18, 19], np.r_[16]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[16]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.78]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.65]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.92, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.83, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.39, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.28, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Palmeiras.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]
        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = "Receitas e Despesas",
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Flamengo":
        markdown_1 = f"<div style='text-align:center;  color: red   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 16, 16, 16, 16, 16, 16, 18, 17] #19 sources
        target = [6, 6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 19, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 16, 10, 11, 12, 13, 14, 15, 18, 17], np.r_[10]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[10]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.70, 0.90, 0.95]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.11, 0.20, 0.40, 0.00, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.05, -0.20, -0.07, -0.22]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'limegreen', 'limegreen']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'lime', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'lime', 'lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.285, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.82, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.76, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.845, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.65, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.715, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.96, y=1.33, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.05, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.96, y=0.94, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Flamengo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 8, 15,  15, 21, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 20, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 23, 21, 17, 18, 19], np.r_[10]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[10]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.78]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.65]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=0.92, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.83, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.37, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.26, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Flamengo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = "Receitas e Despesas",
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Corinthians":
        markdown_1 = f"<div style='text-align:center;  color: grey   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3,  4, 5,  6, 7,  9,  9, 16, 16, 16, 16, 16, 16, 17, 17] #19 sources
        target = [            6, 6, 6, 6,  6, 6,  9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3,  4, 5,  6, 7, 17, 16, 10, 11, 12, 13, 14, 15, 18, 19], np.r_[6]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[6]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.30,  0.37,  0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.60, 0.70, 0.80, 0.80]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.10, 0.40,  0.05, 0.05, 0.20, 0.35, 0.50, 0.65, 0.25, -0.17, -0.10, -0.22, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'lime', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'lime', 'lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.26, y=0.62, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.29, y=0.54, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.00, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.95, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.78, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.25, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.55, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.595, y=1.29, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.72, y=1.20, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.77, y=1.11, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.76, y=1.35, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.81, y=1.30, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Corinthians.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8,  8, 15, 15, 21, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 20, 17, 18] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 23, 21, 17, 18], np.r_[6]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[6]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15,  0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.60,   0.70,  0.78, 0.78, 0.80, 0.90, 0.78]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, -0.05, 0.20, 0.45, 0.60, 0.75, 0.90,  1.15,  -0.20,  0.00,  0.20, 0.05, -0.15, -0.10, 0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=1.12, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=1.02, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.53, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.60, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.59, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=0.34, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=0.16, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.07, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=0.02, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.63, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.53, y=1.12, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=1.02, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.74, y=1.11, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=1.01, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.82, y=0.80, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.81, y=1.35, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.88, y=1.25, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.83, y=1.10, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.90, y=0.99, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Corinthians.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = "Receitas e Despesas",
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Athletico":
        markdown_1 = f"<div style='text-align:center;  color: red   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16,  9, 23, 17, 18] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 17, 17, 19, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 10, 11, 12, 13, 14, 15, 25, 23, 17, 18], np.r_[3]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[3]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.70, 0.90,    0.95, 0.55]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.10, 0.35,   0.55, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.20, -0.15, 0.00, -0.15, -0.27]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'limegreen', 'limegreen', 'grey', 'grey', 'grey', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'lime', 'darkgrey', 'lime', 'lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.43, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.49, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.285, y=0.50, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.42, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.23, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.08, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.00, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.95, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.65, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.715, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.86, y=0.97, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.92, y=0.87, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.96, y=1.29, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Athletico.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 8,  15, 15, 16, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 14, 16, 21, 17, 18, 19, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 23,  8,  9, 10,  11, 12, 13, 14, 16, 21, 17, 18, 19, 22], np.r_[3]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[3]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.60,  0.78, 0.92, 0.92, 0.92, 0.78, 0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.10, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.10, -0.10, 0.05, 0.20, 0.35, 0.50, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'indianred', 'Lime',
                          'indianred', 'indianred', 'indianred', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.29, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.22, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.12, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=0.92, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.83, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.30, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.60, y=1.20, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.84, y=0.51, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Athletico.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Internacional":
        markdown_1 = f"<div style='text-align:center;  color: red   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 9,  9, 16, 16, 16, 16, 16, 16,  9, 23, 24, 17, 17] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 8, 16, 10, 11, 12, 13, 14, 15, 17, 17, 17, 19, 18] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 10, 11, 12, 13, 14, 15, 25, 23, 24, 17, 18], np.r_[15]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[15]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.54, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.65, 0.75,   0.85,  0.55, 0.60]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35,   0.65, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.27, -0.15, -0.25, -0.10, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen', 'grey', 'grey', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'lime', 'darkgrey', 'darkgrey', 'lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.43, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.49, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.56, y=0.35, xanchor='left', showarrow=False, text='<b>Ajutes em<br>despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=11), x=0.595, y=0.25, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.20, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.05, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.60, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.54, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.65, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.82, y=1.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=0.98, xanchor='left', showarrow=False, text='<b>Outras Receitas<br>Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=10), x=0.595, y=0.89, showarrow=False, text=f'<b>{dfa.iat[24,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Internacional.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14,  15, 15, 15, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 8, 16, 20, 21, 17, 18, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 16, 20, 21, 17, 18, 22], np.r_[15]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[15]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.60,  0.78, 0.92, 0.92, 0.78, 0.78, 0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.00, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.00, -0.10, 0.05, 0.20, 0.30, 0.50, -0.15]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'indianred', 'indianred',
                          'Lime', 'indianred', 'indianred', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=0.90, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.81, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=0.58, xanchor='left', showarrow=False, text='<b>AUMENTO<br>DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.84, y=0.51, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Internacional.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Botafogo":
        markdown_1 = f"<div style='text-align:center;  color: grey   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 17, 23, 17, 17, 18] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 24, 19, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 23, 24, 17, 19], np.r_[5]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[5]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.65, 0.75,   0.85,  0.55, 0.60]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35,   0.65, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.32, -0.15, -0.25, -0.10, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon','maroon',
                          'maroon', 'maroon', 'grey', 'maroon', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'darkgrey', 'darkgrey', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.43, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.49, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.35, xanchor='left', showarrow=False, text='<b>Ajutes em<br>ROL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.25, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.20, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.05, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.50, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.45, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.65, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.80, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=1.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=0.98, xanchor='left', showarrow=False, text='<b>Outras Receitas<br>Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=10), x=0.595, y=0.89, showarrow=False, text=f'<b>{dfa.iat[24,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Botafogo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  8,  7,  8,  8,   8,  8,  8, 14, 15, 20, 20, 16, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 8,  16, 16, 21, 17, 18, 19, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 21,  7,  9, 10,  11, 12, 13, 14, 15, 20, 21, 17, 18, 19, 22], np.r_[5]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[5]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.60,  0.78, 0.92, 0.92, 0.88, 0.68,  0.88, 0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.00, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.05, -0.05, 0.05, 0.20, 0.30, 0.15,  0.60, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'limegreen', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'indianred', 'Lime',
                          'Lime', 'indianred', 'indianred', 'indianred', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.52, y=0.90, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.58, y=0.81, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.85, y=0.28, xanchor='left', showarrow=False, text='<b>AUMENTO<br>DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.90, y=0.18, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.85, y=0.58, xanchor='left', showarrow=False, text='<b>Mútuo c/ Partes<br>Relacionadas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.89, y=0.48, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Botafogo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Fortaleza":
        markdown_1 = f"<div style='text-align:center;  color: blue   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 17, 23, 17, 17] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 23, 18, 19], np.r_[12]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[12]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.55, 0.75,   0.85,  0.40, 0.60]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88,  0.03, 0.35,   0.65, 0.12, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.27, -0.20, -0.25, -0.10, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen', 'grey', 'grey', 'grey', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'darkgrey', 'indianred', 'lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.28, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.34, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.29, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.18, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.22, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.13, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.29, y=0.37, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.32, y=0.27, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.19, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.05, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.82, y=1.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.97, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.93, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fortaleza.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14,  15, 15, 15, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13, 8,   16, 20, 21, 17, 19, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 23,  8,  9, 10,  11, 12, 13, 14,  16, 20, 21, 17, 19, 22], np.r_[12]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[12]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.43, 0.55, 0.55, 0.55, 0.55, 0.55,  0.35,  0.60,  0.78, 0.92, 0.92, 0.78,  0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.05, 0.38, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.05, -0.10, 0.05, 0.20, 0.30, -0.15]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'indianred', 'indianred',
                          'Lime', 'indianred', 'indianred', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.86, y=0.80, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.91, y=0.71, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.75, y=0.60, xanchor='left', showarrow=False, text='<b>AUMENTO<br>DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.80, y=0.53, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fortaleza.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Fluminense":
        markdown_1 = f"<div style='text-align:center;  color: red   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 17, 23, 17, 17] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 19, 18] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 23, 17, 18], np.r_[11]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[11]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.55, 0.75,   0.85,  0.45, 0.60]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35,  0.65, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.27, -0.15, -0.25, -0.10, -0.27, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen', 'grey', 'grey', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'darkgrey', 'lime', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.33, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.39, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.35, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.25, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.20, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.06, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.56, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.52, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.82, y=1.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fluminense.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6,  7,  8,  8,   8,  8,  8,  8, 15, 15, 15, 20, 16, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7,  8,  9, 10,  11, 12, 13, 14, 8,  16, 21, 21, 17, 18, 19, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6,  7,  9, 10,  11, 12, 13, 14, 23, 16, 21, 20, 17, 18, 19, 22], np.r_[11]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[11]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.15, 0.30, 0.43, 0.55, 0.55, 0.55, 0.55,  0.55,  0.55,  0.60,  0.78, 0.87, 0.87,  0.87, 0.75,  0.80, 0.45 ]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.05, 0.42,  0.45, 0.60, 0.75, 0.90,  1.05,  1.20, -0.05, -0.10, -0.15, -0.05, 0.10, 0.60, 0.45, -0.15]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'limegreen', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'Lime',
                          'Lime', 'indianred', 'white', 'indianred', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.07, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.12, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.23, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.28, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.87, y=1.25, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.14, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.87, y=1.00, xanchor='left', showarrow=False, text='<b>Investimento<br>na Base</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=0.90, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=0.24, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.795, y=0.19, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=0.58, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.89, y=0.51, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Fluminense.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Vasco":
        markdown_1 = f"<div style='text-align:center;  color: black   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 9,  9, 16, 16, 16, 16, 16, 16, 16, 17, 18] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 8, 16, 10, 11, 12, 13, 14, 15, 17, 19, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 17, 17, 18], np.r_[19]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[19]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.54, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.65, 0.75,   0.86]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35,   0.65, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.27, -0.15, -0.25, -0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.56, y=0.35, xanchor='left', showarrow=False, text='<b>Ajutes em<br>despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=11), x=0.595, y=0.25, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.22, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.07, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.00, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.94, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.65, y=1.24, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=1.34, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=1.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Vasco.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6, 7,  8,  8,   8,  8,  8, 8,  22, 15, 15, 20, 16, 20] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 8,  9, 10,  11, 12, 13, 14, 15,  8, 16, 16, 17, 21] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 8,  9, 10,  11, 12, 13, 14, 22, 24, 19, 23, 17, 21], np.r_[19]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[19]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.55, 0.60,  0.78, 0.89, 0.70, 0.78, 0.45, 0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.00, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  1.00, -0.00, -0.10, 0.05, 0.20, 0.30, -0.10, -0.15]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'limegreen', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'darkgrey', 'indianred', 'indianred',
                          'indianred', 'indianred', 'Lime', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.35, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.20, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.25, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.09, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.14, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.04, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores<br>e Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.90, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.55, y=0.87, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.60, y=0.78, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.81, y=0.77, xanchor='left', showarrow=False, text='<b>AUMENTO<br>DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.86, y=0.64, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Vasco.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "América":
        markdown_1 = f"<div style='text-align:center;  color: green   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 16, 17, 18] #19 sources
        target = [            6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 17, 19, 19] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 17, 17, 18], np.r_[1]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[1]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.70, 0.70, 0.70, 0.70,  0.60,  0.70, 0.85, 0.95,  0.75,  0.86]
        y = [-0.22, -0.00, 0.22, -0.05, 0.35,   0.65, 0.15, 0.18, 0.50, 0.65, 0.85, 0.35, -0.20, -0.10, -0.20, -0.25, -0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.30, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.21, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.72, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.59, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.33, y=0.20, xanchor='left', showarrow=False, text='<b>Ajutes em<br>despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=11), x=0.365, y=0.12, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.22, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.07, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1.00, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.94, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.53, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.45, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação e<br>Amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.65, y=1.37, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.70, y=1.27, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=1.06, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.97, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.35, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.29, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/América.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 6, 7,  8,  8,  8,  8, 15, 22, 15, 15, 15] #21 sources
        target =              [7, 7, 7, 7, 8,  9, 12, 13, 14,  8, 15, 16, 20, 21] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 6, 7,  9, 12, 13, 14, 23, 22, 16, 20, 21], np.r_[1]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[1]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15,   0.15, 0.29, 0.52, 0.65, 0.65, 0.65, 0.65,  0.46,   0.70,  0.70,  0.70,  0.37, 0.70, 0.70]
        y = [-0.22, -0.00, 0.22, 0.44, 0.15, 0.45, 0.45, 0.60,  0.75, 0.90, -0.00,   0.20, -0.00, -0.10, -0.17, 0.20, 0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'darkgrey', 'indianred',
                          'indianred', 'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.31, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.37, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.52, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.16, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.05, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.46, y=0.87, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.52, y=0.77, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.22, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.46, y=1.12, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.68, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.72, y=0.50, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.68, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.74, y=0.34, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.68, y=0.21, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.74, y=0.16, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.66, y=0.02, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.74, y=-0.05, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=0.87, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.78, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.05, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.95, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.20, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.795, y=1.10, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/América.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

    elif clube == "Goiás":
        markdown_1 = f"<div style='text-align:center;  color: green   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source = [            0, 1, 2, 3, 4, 5, 6, 7, 9,  9, 16, 16, 16, 16, 16, 16, 17, 23, 17, 17] #19 sources
        target = [            6, 6, 6, 6, 6, 6, 9, 9, 8, 16, 10, 11, 12, 13, 14, 15, 16, 17, 19, 18] #19 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 23, 17, 18], np.r_[14]].astype(int) #19 values
        dfa = df.iloc[:, np.r_[14]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.54, 0.45, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.60, 0.55, 0.75,   0.85,  0.45, 0.60]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35,   0.65, 0.10, 0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.27, -0.13, -0.28, -0.13, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',
                          'limegreen', 'maroon', 'limegreen', 'grey', 'grey', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'darkgrey', 'lime', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.31, y=1.39, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.38, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.255, y=1.28, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.76, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.62, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.56, y=0.35, xanchor='left', showarrow=False, text='<b>Ajutes em<br>ROL</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=11), x=0.595, y=0.25, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.16, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.02, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.60, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.54, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.05, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.775, y=0.94, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.80, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=0.16, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.10, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.51, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.73, y=1.39, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=1.29, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.88, y=1.16, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.93, y=1.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Goiás.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 4, 5, 6, 7,  8,  8,   8,  8,  8,  8, 8, 15, 15, 16, 16, 22] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 7, 8,  9, 10,  11, 12, 13, 14, 15, 16, 21, 17, 18, 15] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 4, 5, 6, 7,  9, 10,  11, 12, 13, 14, 23, 16, 21, 17, 18, 22], np.r_[14]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[14]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55, 0.55,  0.55,  0.60,  0.78, 0.92, 0.92, 0.78,  0.45, 0.45]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, 1.08, 0.00, 0.35, 0.45, 0.60, 0.75, 0.90, 1.03,  1.15, -0.00, -0.10, 0.05, 0.20, 0.30, -0.10, -0.15]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'grey']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'Lime',
                          'indianred', 'indianred', 'darkgrey', 'darkgrey']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.39, y=1.385, xanchor='left', showarrow=False, text='<b>Venda de Direitos<br>Liga Forte</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.45, y=1.27, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.31, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.37, xanchor='left', showarrow=False, text='<b>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.28, showarrow=False, text=f'<b>{dfa.iat[4,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=-0.13, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=-0.19, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.27, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.17, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.37, y=0.90, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.43, y=0.81, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.25, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="LIMEGREEN", size=10), x=0.60, y=1.15, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.34, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.05, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.10, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.20, xanchor='left', showarrow=False, text='<b>Ajuste nas Saídas de<br>Caixa Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.10, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.965, y=0.99, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=0.90, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.81, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.80, y=0.75, xanchor='left', showarrow=False, text='<b>AUMENTO<br>DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.85, y=0.62, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Goiás.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[47, 1:5, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Direitos de transmissão": "Direitos de transmissão" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        st.pyplot(fig)


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    elif clube == "Vasco":
        markdown_1 = f"<div style='text-align:center;  color: black   ; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        def main():
            royal_style = """
            <style>
                .royal-text {
                    font-family: 'Times New Roman', Times, serif; /* Classic, formal font */
                    font-size: 22px; /* Larger text size */
                    color: #000080; /* Royal blue color */
                    text-align: center; /* Centered text */
                    margin: 20px; /* Adds space around the text */
                }
            </style>
            """

            text = """
            "São esses doze jogadores, jovens, quasi todos brasileiros, no começo de sua carreira, e o acto publico que os pode macular, nunca será praticado com a solidariedade dos que dirigem a casa que os acolheu, nem sob o pavilhão que elles com tanta galhardia cobriram de glorias. Nestes termos, sentimos ter que comunicar a V. Exa. que desistimos de fazer parte da A.M.E.A."
            """
            text2 = """
            José Augusto Prestes, 7 de abril de 1924 
            """
            # Inject HTML with style
            st.markdown(royal_style, unsafe_allow_html=True)

            # Display styled text
            st.markdown(f'<div class="royal-text">{text}<br>{text2}</div>', unsafe_allow_html=True)

        if __name__ == "__main__":
            main()

































        def main():
            # URL of the image (make sure it's the raw version if it's hosted on GitHub)
            image_url = 'https://raw.githubusercontent.com/JAmerico1898/Financials/975782cba0c76542a7d5a3c8287c3eda0ad132b3/vasco_5.jpg'

            # Fetch the image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Display the image
            col1, col2, col3 = st.columns([1,2,1])
            with col2:  # Use the middle column to display the image
                st.image(image, caption='', use_column_width=True)

        if __name__ == "__main__":
            main()        



###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    elif clube == "Grêmio":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6, 7, 8, 9,   9, 16, 16, 16, 16, 16, 16, 17, 19] #18 sources
        target =              [6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 18] #18 targets
        value = df.iloc[np.r_[21, 1, 2, 3, 5, 6, 7, 8, 17, 9, 10, 11, 12, 13, 14, 15, 17, 19], np.r_[13]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[13]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.65, 0.75, 0.85]
        y = [-0.23, 0.00, 0.20, 0.40, 0.58, -0.10, 0.20, +0.40, 0.00, 0.00, 0.20, 0.35, 0.50, 0.65, 0.80, 0.30, -0.20, -0.20, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',  
                          'limegreen', 'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'Lime', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.62, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.56, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.42, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.31, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.295, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.29, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.94, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.08, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.99, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.17, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.855, y=0.11, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.65, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.71, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.76, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.33, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.86, y=1.28, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Gremio.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14, 15, 21, 21, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13,  8, 16, 20, 16, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 15, 20, 23, 17, 18, 19], np.r_[13]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[13]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.62]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'Lime', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.33, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.27, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.11, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.05, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.375, y=0.95, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.86, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.31, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.12, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.08, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.98, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=0.92, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.82, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.53, y=0.96, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.60, y=0.86, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Gremio.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })

        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    elif clube == "Atlético":
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 17, 24, 17, 17] #18 sources
        target =              [6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] #18 targets
        value = df.iloc[np.r_[ 0, 1, 2, 3, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 24, 18, 19], np.r_[2]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[2]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.55, 0.40, 0.55, 0.55, 0.25]
        y = [-0.23, 0.00, 0.20, 0.40, -0.10,  0.20,  0.40, 0.00, 0.00, 0.20, 0.35, 0.50, 0.65, 0.80, 0.15, 0.60, 0.65, 0.85, 0.80]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',  
                          'limegreen', 'maroon', 'limegreen']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'darkgrey', 'indianred',
                          'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.62, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.56, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.29, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.20, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.295, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.29, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.29, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.45, y=1.13, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.515, y=1.10, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.55, y=1.04, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.08, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.99, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.17, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.855, y=0.11, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.36, y=0.17, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.40, y=0.12, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.35, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.605, y=0.25, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.17, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.605, y=0.11, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.13, y=0.17, xanchor='left', showarrow=False, text='<b>Outras Receitas<br>Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="darkgrey", size=10), x=0.17, y=0.12, showarrow=False, text=f'<b>{dfa.iat[24,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Atletico.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 6,   7,  8,  8,   8,  8,  8,   8, 15,  16, 20, 15] #21 sources
        target =              [7, 7, 7, 7, 7,   8,  9, 10,  11, 12, 13,  14,  8, 15, 15, 21] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 6,   7,  9, 10,  11, 12, 13,  14, 15, 16, 20, 21], np.r_[2]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[2]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15,   0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.55, 0.60, 0.70,  0.70, 0.70]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, -0.05, 0.20, 0.45, 0.60, 0.75, 0.90, 1.05,  1.20, -0.10, -0.20, 0.00, 0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'limegreen',
                          'limegreen', 'limegreen', 'limegreen', 'limegreen', 'limegreen']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'Lime', 'Lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.33, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.27, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.11, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.05, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.28, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.18, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.375, y=1.15, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=1.04, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.54, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.60, y=1.29, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.31, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.05, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.1, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.25, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.30, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.38, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.795, y=1.30, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.02, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.795, y=0.92, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=0.86, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=0.76, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Atletico.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })

        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


    elif clube == "Santos":
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 5, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 9, 17, 17] #17 sources
        target =              [6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 17, 18, 19] #17 targets
        value = df.iloc[np.r_[ 0, 1, 2, 5, 6, 7, 8, 16, 10, 11, 12, 13, 14, 15, 17, 18, 19], np.r_[17]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[17]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15,  0.295, 0.375,  0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.65, 0.75, 0.86]#, 0.85]
        y = [-0.23, 0.00, 0.20, 0.40, -0.15, 0.20, 0.40,   0.00, -0.05, 0.10, 0.27, 0.43, 0.60, 0.75, 0.30, -0.20, -0.23, -0.17]#, -0.10]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'limegreen'  
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'Lime', 'indianred', 'Lime'
                          ]

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.75, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.62, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.065, y=0.54, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.29, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.77, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.29, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.31, y=0.54, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.45, y=1.24, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.555, y=1, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.94, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.13, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=1.03, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.97, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.87, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.81, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.71, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.58, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.845, y=0.50, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.41, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.30, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.25, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.18, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.65, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.71, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.76, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.30, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.86, y=1.25, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Santos.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 5, 6, 7, 8,  8,  8,  8,  8, 14, 7,  15,  15, 16, 16, 21  ] #18 sources
        target =              [7, 7, 7, 7, 7, 8, 9, 10, 11, 12, 13,  8, 15, 16, 20, 17, 18, 20 ] #18 targets
        value = df2.iloc[np.r_[0, 1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 23, 17, 18, 21], np.r_[17]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[17]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,   0.15, 0.15, 0.15, 0.15, 0.30, 0.45, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78]
        y = [-0.22,  0.00, 0.22, 0.44, 0.66, -0.10, 0.30, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.50, 0.70]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue',
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'Lime', 'maroon', 'maroon',
                          'maroon', 'maroon', 'maroon', 'maroon'
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'LightSkyBlue', 'Limegreen', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.52, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.33, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.27, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=0.97, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.45, y=0.88, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.31, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.22, y=0.13, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=0.07, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.72, y=1.31, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.79, y=1.21, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.08, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.98, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=0.92, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.82, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.85, y=0.64, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=0.56, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.70, y=0.41, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.78, y=0.31, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Santos.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


    elif clube == "Coritiba":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 6, 7, 8,  9, 16, 16, 16, 16, 16, 16, 17, 23, 17, 17, 17] #17 sources
        target =              [6, 6, 6, 6, 9, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 24, 18, 19] #17 targets
        value = df.iloc[np.r_[ 0, 1, 2, 3, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 25, 23, 24, 18, 19], np.r_[7]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[7]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15,  0.295, 0.35,  0.35, 0.425,  0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.52, 0.75, 0.80, 0.42, 0.75]
        y = [-0.23, 0.00, 0.20, 0.40, -0.05,  0.20,   0.40,  0.20, 0.15, 0.30, 0.45, 0.60, 0.75, 0.30, -0.15, -0.10, -0.23, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 
                          'maroon', 'limegreen', 'limegreen', 'maroon','limegreen','gray', 'maroon'  
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'darkgrey', 'indianred',
                          'indianred', 'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.75, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=0.62, xanchor='left', showarrow=False, text='<b>Sócio<br>Torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.065, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.255, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.16, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.24, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.27, y=0.77, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.26, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.28, y=0.54, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.375, y=1.08, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.425, y=0.94, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.56, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.52, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=1.03, xanchor='left', showarrow=False, text='<b>Perda<br>Oper<BR>Líquida</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.90, showarrow=False, text=f'<b>{dfa.iat[25,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.93, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.82, y=0.83, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.78, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.68, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.58, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.50, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.30, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.25, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.18, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.475, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.52, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=1.15, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.90, y=1.13, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.30, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.86, y=1.25, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=1.05, xanchor='left', showarrow=False, text='<b>Outras Despesas<br>Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.02, showarrow=False, text=f'<b>{dfa.iat[24,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.295, y=1.38, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<BR>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=10), x=0.36, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

    


        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Coritiba.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 6, 22,  7, 8,  8,  8,  8,  8, 14, 8,  15, 20, 16, 16, 20  ] #18 sources
        target =              [7, 7, 7, 7, 7, 15,  8, 9, 10, 11, 12, 13, 8, 15, 16, 16, 17, 18, 21 ] #18 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 6, 22,  7, 9, 10, 11, 12, 13, 14, 23, 15, 24, 17, 18, 21], np.r_[7]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[7]].astype(int)

        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.30, 0.45, 0.60, 0.60, 0.60, 0.60, 0.60, 0.30,  0.65,  0.80, 0.90,  0.90, 0.70, 0.85, 0.50]
        y = [0.00, 0.22, 0.44, 0.66, 0.88, 0.05, 0.22, 0.30, 0.47, 0.60, 0.75, 0.90, 1.15,  -0.15, -0.10, -0.20, -0.05, 0.10, 0.30, -0.23]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue',
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon', 'maroon',
                          'maroon', 'maroon', 'limegreen', 'limegreen', 'gray'
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'darkgrey', 'LightSkyBlue', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'LightSkyBlue', 'indianred',
                          'indianred', 'Lime', 'indianred', 'indianred', 'Lime',
                          'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.37, y=1.37, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<br>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.435, y=1.25, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.93, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.86, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.75, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=0.60, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.52, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.05, y=0.33, xanchor='left', showarrow=False, text='<b>Sócio<br>Torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.27, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.12, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.06, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.20, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.10, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.08, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.45, y=0.99, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.65, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.80, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.67, y=0.70, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.58, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.68, y=0.50, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.68, y=0.31, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.69, y=0.16, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.08, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.69, y=0.03, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.17, y=-0.14, xanchor='left', showarrow=False, text='<b>Ajuste nas Saídas de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.22, y=-0.21, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=9), x=0.74, y=1.28, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=9), x=0.81, y=1.19, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.28, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=1.18, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.12, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=1.02, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.75, y=0.97, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.82, y=0.86, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.86, y=0.74, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.94, y=0.61, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.55, y=0.99, xanchor='left', showarrow=False, text='<b>Caixa<br>Negativo</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.58, y=0.88, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Coritiba.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


    elif clube == "Cruzeiro":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6, 7, 9,  16, 16, 16, 16, 16, 16, 17, 23, 17, 18, 17] #17 sources
        target =              [6, 6, 6, 6, 6, 9, 9, 16, 10, 11, 12, 13, 14, 15, 16, 17, 24, 19, 19] #17 targets
        value = df.iloc[np.r_[ 0, 1, 2, 3, 5, 6, 7, 9,  10, 11, 12, 13, 14, 15, 25, 23, 24, 18, 17], np.r_[8]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[8]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15, 0.15, 0.295, 0.35, 0.425,  0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.52, 0.75, 0.90, 0.42, 0.75]
        y = [-0.23, 0.00, 0.20, 0.40, 0.60, -0.05, 0.40,  0.20, 0.15, 0.30, 0.45, 0.60, 0.75, 0.30, -0.15, -0.10, -0.23, -0.25, 0.00]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 
                          'maroon', 'limegreen', 'limegreen', 'maroon','limegreen','gray', 'maroon'  
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'darkgrey', 'indianred',
                          'indianred', 'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.75, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=0.62, xanchor='left', showarrow=False, text='<b>Sócio<br>Torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.065, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.255, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.16, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=0.41, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.065, y=0.30, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.24, y=0.68, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.27, y=0.54, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.375, y=1.08, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.425, y=0.94, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.56, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.52, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=1.03, xanchor='left', showarrow=False, text='<b>Perda<br>Oper<BR>Líquida</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.90, showarrow=False, text=f'<b>{dfa.iat[25,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.93, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.82, y=0.83, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.78, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.68, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.58, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.50, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.41, xanchor='left', showarrow=False, text='<b>Depreciação<br>Amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.30, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.25, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.18, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.475, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.52, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.65, y=1.17, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.71, y=1.08, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.30, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.96, y=1.25, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.79, y=1.05, xanchor='left', showarrow=False, text='<b>Outras Despesas<br>Operacionais</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.93, y=1.02, showarrow=False, text=f'<b>{dfa.iat[24,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.295, y=1.38, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<BR>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=10), x=0.36, y=1.28, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

    


        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cruzeiro.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6, 22,  7, 8,  8,  8,  8,  8, 14, 7,  15, 20, 16, 16, 20  ] #18 sources
        target =              [7, 7, 7, 7, 7, 7, 15,  8, 9, 10, 11, 12, 13, 8,  15, 16, 16, 17, 18, 21 ] #18 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 5, 6, 22,  8, 9, 10, 11, 12, 13, 14, 23, 15, 23, 17, 18, 21], np.r_[8]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[8]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.30, 0.45, 0.60, 0.60, 0.60, 0.60, 0.375,  0.52,  0.65,  0.80, 0.90,   0.60, 0.90,  0.42]
        y = [0.00, 0.22, 0.44, 0.66, 0.88, 1.10, 0.05, 0.22, 0.30, 0.47, 0.60, 0.75, 0.90, -0.15,  -0.15, -0.10, -0.20, -0.05, 0.30, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue',
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon', 'maroon',
                          'maroon', 'maroon', 'limegreen', 'limegreen', 'gray'
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'darkgrey', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.31, y=1.37, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<br>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.375, y=1.25, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.93, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.86, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.75, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=0.60, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.52, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.05, y=0.33, xanchor='left', showarrow=False, text='<b>Sócio<br>Torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.27, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.12, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.06, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.04, y=-0.12, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=-0.18, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.20, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.10, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.06, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.45, y=0.97, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.46, y=1.36, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.52, y=1.27, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.80, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.67, y=0.70, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.58, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.68, y=0.50, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.68, y=0.31, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.21, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.69, y=0.16, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.22, y=0.08, xanchor='left', showarrow=False, text='<b>Ajuste nas Saídas de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.285, y=0.03, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=9), x=0.60, y=1.34, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=9), x=0.65, y=1.25, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.18, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.86, y=1.08, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=1.28, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=1.18, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.55, y=0.97, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.62, y=0.86, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.83, y=0.67, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.91, y=0.54, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cruzeiro.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


    elif clube == "Cuiabá":
        markdown_1 = f"<div style='text-align:center;  color: gold; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 6, 8, 23,  9, 16, 16,  9, 17, 17] #17 sources
        target =              [6, 6, 6, 9, 9, 9,  16, 10, 13, 17, 19, 18] #17 targets
        value = df.iloc[np.r_[ 0, 1, 2, 6, 8, 23, 16, 10, 13, 17, 19, 18], np.r_[9]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[9]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.30, 0.30,  0.45, 0.75,  0.75, 0.60,  0.70, 0.80, 0.80, 0.30]
        y = [0.00, 0.30, 0.50, 0.20,  0.55,  0.30,  0.20, 0.50, 0.40, -0.15, 0.00, -0.25, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'limegreen', 
                          'maroon', 'limegreen', 'limegreen', 'maroon','limegreen','gray', 'maroon',
                          'maroon'  
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'darkgray', 'indianred', 'indianred',
                          'indianred', 'Lime', 'Lime', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.12, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.97, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.77, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.65, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.50, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.065, y=0.40, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.10, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=1.01, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.20, y=0.52, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.22, y=0.40, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.16, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.45, y=1.02, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=0.91, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.87, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.82, y=0.78, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.53, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.44, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.645, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.71, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.30, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="Limegreen", size=10), x=0.86, y=1.25, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=1.39, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<BR>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="gray", size=10), x=0.29, y=1.30, showarrow=False, text=f'<b>{dfa.iat[23,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.10, xanchor='left', showarrow=False, text='<b>Resultado<br>Financeiro</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.86, y=1.00, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cuiaba.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: gold; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2,  22,    7, 8,  8, 14,   7,  15, 16, 16, 15] #18 sources
        target =              [7, 7, 7,  15,    8, 9, 12,  7,  15,  16, 17, 18, 21] #18 targets
        value = df2.iloc[np.r_[0, 1, 2,  22,    8, 9, 12, 14,  23,  16, 17, 18, 21], np.r_[9]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[9]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.30, 0.45, 0.60, 0.60, 0.15,  0.55,  0.70,  0.80,  0.80,  0.80, 0.45,  0.85, 0.90, 0.90, 0.90, 0.90]
        y = [0.20, 0.40, 0.60, 0.20, 0.40, 0.20, 0.60, 0.80, -0.14, -0.17, -0.20,  -0.05, 0.10, -0.23, 0.05, -0.20, -0.20, -0.20, 0.50]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue',
                          'maroon', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'steelblue', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon', 'maroon',
                          'maroon', 'maroon', 'limegreen', 'limegreen', 'grey'
                          ]
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'darkgrey',
                          'indianred', 'indianred', 'indianred', 'LightSkyBlue', 'Lime',
                          'indianred', 'indianred', 'indianred', 'Lime', 'Lime',
                          'LightSkyBlue', 'Lime']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.305, y=1.36, xanchor='left', showarrow=False, text='<b>VENDA DE DIREITOS<br>LIGA FORTE</b>'))
        fig.add_annotation(dict(font=dict(color="grey", size=11), x=0.38, y=1.25, showarrow=False, text=f'<b>{dfa.iat[22,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.91, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.75, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.60, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.52, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.03, y=0.41, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.07, y=0.29, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.08, y=0.00, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=11), x=0.14, y=-0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.17, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.08, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=0.95, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.45, y=0.85, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.49, y=1.38, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.55, y=1.29, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.90, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.67, y=0.80, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.63, y=0.41, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.68, y=0.31, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.29, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.88, y=1.19, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.12, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.87, y=1.02, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.64, y=1.39, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.71, y=1.30, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.83, y=0.97, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.91, y=0.88, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/Cuiaba.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: gold; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


    elif clube == "São Paulo":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Resultado</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6, 7, 8, 9,   9, 16, 16, 16, 16, 16, 16, 17, 19] #18 sources
        target =              [6, 6, 6, 6, 6, 9, 9, 9, 17, 16, 10, 11, 12, 13, 14, 15, 18, 18] #18 targets
        value = df.iloc[np.r_[0, 1, 2, 3, 5, 6, 7, 8, 17, 16, 10, 11, 12, 13, 14, 15, 17, 19], np.r_[18]].astype(int) #18 values
        dfa = df.iloc[:, np.r_[18]].astype(int)
            
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15,  0.15, 0.15, 0.15, 0.15,  0.30, 0.375, 0.375, 0.45, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.60, 0.65, 0.75, 0.85]
        y = [-0.23, 0.00, 0.20, 0.40, 0.58, -0.10, 0.20, +0.40, 0.00, 0.00, 0.20, 0.35, 0.50, 0.65, 0.80, 0.30, -0.20, -0.20, -0.20]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'steelblue', 'limegreen', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'maroon', 'maroon', 'maroon',  
                          'limegreen', 'maroon', 'maroon', 'maroon', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'Lime', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.62, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.56, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.42, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.31, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.25, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>RECORRENTE</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.28, y=1.30, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.27, y=0.88, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.295, y=0.78, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.29, y=0.68, xanchor='left', showarrow=False, text='<b>Outras<br>receitas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.30, y=0.55, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.40, y=1.39, xanchor='left', showarrow=False, text='<b>RECEITA<br>OPERACIONAL<BR>LÍQUIDA</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.45, y=1.23, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.56, y=1, xanchor='left', showarrow=False, text='<b>DESPESAS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.595, y=0.94, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=1.08, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.99, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.88, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.825, y=0.78, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.66, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.84, y=0.58, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.505, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.85, y=0.425, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.35, xanchor='left', showarrow=False, text='<b>Depreciação<br>amortização</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.83, y=0.25, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.78, y=0.17, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.855, y=0.11, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.60, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.65, y=1.28, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.71, y=1.38, xanchor='left', showarrow=False, text='<b>RESULTADO<br>FINANCEIRO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.76, y=1.28, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.82, y=1.33, xanchor='left', showarrow=False, text='<b>RESULTADO</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.86, y=1.28, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/SaoPaulo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom left corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )


        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Demonstração de Fluxo de Caixa</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Defining labels, sources and targets

        source =              [0, 1, 2, 3, 5, 6,  7,  7,  8,  8,   8,  8,  8, 14, 15, 15, 21, 16, 16, 16] #21 sources
        target =              [7, 7, 7, 7, 7, 7, 15,  8,  9, 10,  11, 12, 13,  8, 16, 20, 16, 17, 18, 19] #21 targets
        value = df2.iloc[np.r_[0, 1, 2, 3, 5, 6, 15,  8,  9, 10,  11, 12, 13, 14, 23, 20, 21, 17, 18, 19], np.r_[18]].astype(int) #19 values
        dfa = df2.iloc[:, np.r_[18]].astype(int)
        link = dict(source=source, target=target, value=value, color=color_link)
        node = dict(label = label_caixa, pad=35, thickness=20)
        data = go.Sankey(link=link, node=node)

        # Set our X and Y co-ords 
        x = [0.15, 0.15, 0.15, 0.15, 0.15,   0.15, 0.30, 0.42, 0.55, 0.55, 0.55, 0.55,  0.55,  0.35, 0.55,  0.78, 0.92, 0.92, 0.92, 0.78, 0.68]
        y = [-0.22, -0.00, 0.22, 0.44, 0.66, 0.88, -0.05, 0.35, 0.45, 0.60, 0.75, 0.90, 1.15,  0.90, -0.20, -0.10, 0.05, 0.20, 0.35, 0.50, 0.05]
        x = [.001 if v==0 else .999 if v==1 else v for v in x]
        y = [.001 if v==0 else .999 if v==1 else v for v in y]

        # Node Colors
        color_for_nodes =['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 
                          'steelblue', 'steelblue', 'steelblue', 'maroon', 'maroon', 'maroon', 
                          'maroon', 'maroon', 'maroon', 'steelblue', 'limegreen', 'maroon',
                          'maroon', 'maroon', 'maroon', 'limegreen', 'maroon']
            
        color_for_links =['LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue', 'LightSkyBlue',
                          'LightSkyBlue', 'LightSkyBlue', 'Lime', 'LightSkyBlue',
                          'indianred', 'indianred', 'indianred', 'indianred',
                          'indianred', 'LightSkyBlue', 'indianred', 'Lime', 'indianred',
                          'indianred', 'indianred', 'indianred']

        fig = go.Figure(data=[go.Sankey(
                # The following line hides our labels. They still show
                # when you hover the mouse over an object
                textfont=dict(color="rgba(0,0,0,0)", size=1),
                node = dict(
                    pad = 35,
                    line = dict(color = "white", width = 1),
                    label = label_caixa,
                    x = x,
                    y = y
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                    ))])

        # Update our chart
        fig.update_layout(
            hovermode='x',
        )
        # Apply node and link colour choices
        fig.update_traces(node_color = color_for_nodes,
                        link_color = color_for_links)

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.36, xanchor='left', showarrow=False, text='<b>Direitos de<br>transmissão e<br>Premiações</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=1.20, showarrow=False, text=f'<b>{dfa.iat[0,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=1.08, xanchor='left', showarrow=False, text='<b>Publicidade e<br>patrocínio</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.97, showarrow=False, text=f'<b>{dfa.iat[1,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.87, xanchor='left', showarrow=False, text='<b>Arrecadação<br>de jogos</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.06, y=0.76, showarrow=False, text=f'<b>{dfa.iat[2,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.60, xanchor='left', showarrow=False, text='<b>Sócio-torcedor</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.54, showarrow=False, text=f'<b>{dfa.iat[3,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.33, xanchor='left', showarrow=False, text='<b>Licenciamento<br>da marca</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.27, showarrow=False, text=f'<b>{dfa.iat[5,0]}</b>'))
            
        fig.add_annotation(dict(font=dict(color="black", size=11), x=0.02, y=0.11, xanchor='left', showarrow=False, text='<b>Negociação<br>de atletas</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=11), x=0.05, y=0.05, showarrow=False, text=f'<b>{dfa.iat[6,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.26, y=1.39, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE<br>CAIXA TOTAL</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.285, y=1.29, showarrow=False, text=f'<b>{dfa.iat[7,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.375, y=0.94, xanchor='left', showarrow=False, text='<b>SAÍDAS DE CAIXA<br>OPERACIONAIS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.42, y=0.85, showarrow=False, text=f'<b>{dfa.iat[8,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.50, y=1.385, xanchor='left', showarrow=False, text='<b>GERAÇÃO DE CAIXA<br>OPERACIONAL</b>'))
        fig.add_annotation(dict(font=dict(color="green", size=10), x=0.55, y=1.30, showarrow=False, text=f'<b>{dfa.iat[15,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.58, xanchor='left', showarrow=False, text='<b>Pessoal e<br>encargos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.6, y=0.51, showarrow=False, text=f'<b>{dfa.iat[9,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.41, xanchor='left', showarrow=False, text='<b>Direitos de<br>imagem</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.31, showarrow=False, text=f'<b>{dfa.iat[10,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.21, xanchor='left', showarrow=False, text='<b>Despesas com<br>jogos</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.61, y=0.16, showarrow=False, text=f'<b>{dfa.iat[11,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=0.05, xanchor='left', showarrow=False, text='<b>Despesas gerais<br>e administrativas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.0, showarrow=False, text=f'<b>{dfa.iat[12,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.57, y=-0.15, xanchor='left', showarrow=False, text='<b>Outras despesas</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.62, y=-0.2, showarrow=False, text=f'<b>{dfa.iat[13,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.23, y=0.14, xanchor='left', showarrow=False, text='<b>Ajuste na Geração de<br>Caixa Operacional</b>'))
        fig.add_annotation(dict(font=dict(color="steelblue", size=10), x=0.29, y=0.06, showarrow=False, text=f'<b>{dfa.iat[14,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.725, y=1.32, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A INVESTIMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.795, y=1.22, showarrow=False, text=f'<b>{dfa.iat[16,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.91, y=1.08, xanchor='left', showarrow=False, text='<b>Compra<br>de Jogadores</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.98, showarrow=False, text=f'<b>{dfa.iat[17,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.92, y=0.92, xanchor='left', showarrow=False, text='<b>Compra de<br>Imobilizado</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.97, y=0.82, showarrow=False, text=f'<b>{dfa.iat[18,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.927, y=0.717, xanchor='left', showarrow=False, text='<b>Outras</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.96, y=0.63, showarrow=False, text=f'<b>{dfa.iat[19,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.77, y=0.58, xanchor='left', showarrow=False, text='<b>CAIXA DESTINADO<br>A FINANCIAMENTOS</b>'))
        fig.add_annotation(dict(font=dict(color="limegreen", size=10), x=0.84, y=0.52, showarrow=False, text=f'<b>{dfa.iat[20,0]}</b>'))

        fig.add_annotation(dict(font=dict(color="black", size=10), x=0.68, y=0.97, xanchor='left', showarrow=False, text='<b>AUMENTO/<br>DIMINUIÇÃO DE CAIXA</b>'))
        fig.add_annotation(dict(font=dict(color="indianred", size=10), x=0.77, y=0.87, showarrow=False, text=f'<b>{dfa.iat[21,0]}</b>'))

        fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/JAmerico1898/Financials/b8aa21e79bd9f585f0acd3daf3d22d6c1002c314/SaoPaulo.png",  # Change this to your image path
                xref="paper",  # Use "paper" for relative positioning within the plot
                yref="paper",
                x=1,  # Bottom right corner
                y=0,  # Bottom left corner
                sizex=0.1,  # Size of the image in x-axis proportion of plot's width
                sizey=0.1,  # Size of the image in y-axis proportion of plot's height
                xanchor="right",  # Anchor point is set to the left of the image
                yanchor="bottom"  # Anchor point is set to the bottom of the image
            )
        )

        st.plotly_chart(fig)

#############################################################################################################################################
#############################################################################################################################################

        #Plotar Gráfico Alternativo
        fontsize=28
        # Player Comparison Data
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;'>Comparativo com a Média da Liga</h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        dfb = df1.iloc[np.r_[0:4, 6:8, 22, 26], np.r_[0:21]]
        dfb_transposed = dfb.T
        # Set the first row as the new header
        dfb_transposed.columns = dfb_transposed.iloc[0]
        # Drop the first row
        dfb_transposed = dfb_transposed.iloc[1:]
        # Rename the first column to 'clubs'
        dfb_transposed.index.name = 'Clubes'
        dfb = dfb_transposed
        # Renaming Columns
        dfb = dfb.rename(columns={"Receita c/ Publicidade e patrocínio": "Publicidade/patrocínio",
                                  "Receita c/ Match-Day": "Match-Day",
                                  "Receita c/ Sócio-torcedor": "Sócio-Torcedor",
                                  "Receita c/ Negociação de atletas": "Venda de jogadores",
                                  "Receita c/ Transmissão + Premiações": "Transmissão/Premiações",
                                  "RECEITA RECORRENTE": "Receita Recorrente" 
                                  })
        # Preparing the Graph
        params = list(dfb.columns)
        params = params[0:]

        #Preparing Data
        ranges = []
        a_values = []
        b_values = []

        for x in params:
            a = min(dfb[params][x])
            a = a
            b = max(dfb[params][x])
            b = b
            ranges.append((a, b))

        for x in range(len(dfb.index)):
            if dfb.index[x] == clube:
                a_values = dfb.iloc[x].values.tolist()
            if dfb.index[x] == 'Média da Liga':
                b_values = dfb.iloc[x].values.tolist()
                                    
        a_values = a_values[0:]
        b_values = b_values[0:]

        # Rounding values to no decimal places
        a_values = [round(value) for value in a_values]
        b_values = [round(value) for value in b_values]

        values = [a_values, b_values]

        #Plotting Data
        title = dict(
            title_name = clube,
            title_color = '#B6282F',
            subtitle_name = "(R$ milhões)",
            subtitle_color = '#B6282F',
            title_name_2 = 'Média da Liga',
            title_color_2 = '#344D94',
            subtitle_name_2 = "(R$ milhões)",
            subtitle_color_2 = '#344D94',
            title_fontsize = 18,
        ) 

        ## instantiate object
        radar = Radar()

        ## instantiate object -- changing fontsize
        radar=Radar(fontfamily='Cursive', range_fontsize=14)
        radar=Radar(fontfamily='Cursive', label_fontsize=14)

        fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.6,.5], title=title, compare=True)
        #fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#7eb6e0', '#f77b72'], dpi=600, alphas=[.8,.6], title=title, compare=True)
        st.pyplot(fig)

























###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

elif choose == "Análise Comparativa Univariada":

    highlight = st.selectbox("Escolha o Clube para destacar", options=clubes, index=None, placeholder="Escolha o Clube!")
    tema_cont = st.selectbox("Escolha o Tema Contábil", options=temas_cont, index=None, placeholder="Escolha o Tema Contábil!")
    fontsize = 24
    if tema_cont == "Receita c/ Direitos de Transmissão":

        fontsize = 24
        if highlight:

            tópico = df1.iloc[47, 1:].values
            markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
            st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
            st.markdown(markdown_1, unsafe_allow_html=True)
            st.markdown("---")

            # Pairing clubs with their revenues and sorting them by revenue in descending order
            paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
            sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

            def getImage(url):
                try:
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    return OffsetImage(img, zoom=1.25)
                except Exception as e:
                    print(f"Error loading image from {url}: {e}")
                    return None

            fig, ax = plt.subplots(figsize=(15, 10))
            ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
            # Set ylim if necessary to create space for club icons

            # Increase the ylim if necessary to create more space for club icons
            max_revenue = max(sorted_revenues)
            ax.set_ylim(-max_revenue*0.2, max_revenue*1.2)  # Adjusting space at the bottom for icons

            bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

            # Modify this part of your plotting code
            for i, club in enumerate(sorted_clubes):
                img_url = club_image_paths.get(club)
                if img_url:
                    img = getImage(img_url)
                    if img:
                        # Get the index for the selected categories (eixo_x, eixo_y)
                        ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                            xycoords='data', boxcoords="data",
                                            box_alignment=(0.5, 0), frameon=False)
                        ax.add_artist(ab)
                    else:
                        print(f"Failed to load image for {club}")

            ax.set_xticks([])

            #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
            ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=22, fontweight='bold')
            ax.tick_params(axis='y', labelsize=16)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            # Adding text above bars
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=16)

            fig.tight_layout()
            st.pyplot(fig)

#######################################################################################################################################

            st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
            markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
            st.markdown(markdown_1, unsafe_allow_html=True)
            st.markdown("---")

            years = ['2019', '2020', '2021', '2022', '2023']

            tópico2 = df3.iloc[28, 1:].values
            club_data = {
                'América': tópico2[:5][::-1][:5],
                'Atlético': tópico2[5:10][::-1][:5],
                'Athletico': tópico2[10:15][::-1][:5],
                'Bahia': tópico2[15:20][::-1][:5],
                'Botafogo': tópico2[20:25][::-1][:5],
                'Corinthians': tópico2[25:30][::-1][:5],
                'Coritiba': tópico2[30:35][::-1][:5],
                'Cruzeiro': tópico2[35:40][::-1][:5],
                'Cuiabá': tópico2[40:45][::-1][:5],
                'Flamengo': tópico2[45:50][::-1][:5],
                'Fluminense': tópico2[50:55][::-1][:5],
                'Fortaleza': tópico2[55:60][::-1][:5],
                'Grêmio': tópico2[60:65][::-1][:5],
                'Goiás': tópico2[65:70][::-1][:5],
                'Internacional': tópico2[70:75][::-1][:5],
                'Palmeiras': tópico2[75:80][::-1][:5],
                'Santos': tópico2[80:85][::-1][:5],
                'São Paulo': tópico2[85:90][::-1][:5],
                'Vasco': tópico2[90:95][::-1][:5]
            }

            # Plotting each club's data
            fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

            # Plot each club's data
            for club, data in club_data.items():
                if club == highlight:
                    ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                    # Annotate each point on the highlighted club's line
                    for i, value in enumerate(data):
                        ax.annotate(f'{value:.0f}',  # Text to display
                                    (years[i], value),  # Point to annotate
                                    textcoords="offset points",  # how to position the text
                                    xytext=(0,10),  # distance from text to points (x,y)
                                    ha='center',  # horizontal alignment can be left, right or center
                                    va='bottom',
                                    fontsize=14, 
                                    fontweight='bold')
                else:
                    ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

            # Adding titles and labels
            #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
            ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
            ax.tick_params(axis='y', labelsize=12)
            ax.tick_params(axis='x', labelsize=12)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            # Show the plot
            st.pyplot(fig)


#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita c/ Transmissão + Premiações":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[0, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None
            
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_url = club_image_paths.get(club)
            if img_url:
                img = getImage(img_url)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)


        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[1, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita c/ Publicidade e patrocínio":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[1, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None
            
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_url = club_image_paths.get(club)
            if img_url:
                img = getImage(img_url)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[2, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita de Match-Day":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[2, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[3, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita c/ Sócio-torcedor":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[3, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[4, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Premiações":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[4, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[5, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita c/ Licenciamento da marca":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[5, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[6, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita Recorrente":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[6, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[7, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita c/ Negociação de Atletas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[7, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[8, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Receita Operacional Líquida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[9, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[9, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

########################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Resultado":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[17, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[11, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################


    elif tema_cont == "Dívida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[48, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[29, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_cont == "Despesas gerais e administrativas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_cont:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[13, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[29, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
    tema_esport = st.selectbox("Escolha o Tema Esportivo", options=temas_esport, index=None, placeholder="Escolha o Tema Esportivo!")
    fontsize = 24
    if tema_esport == "Folha do futebol":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[26, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[10, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_esport == "Aquisições de atletas":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[22, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[13, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_esport == "Gastos com a Base":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[23, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[14, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_cont} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_esport == "Base de Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[28, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################
#######################################################################################################################################


    elif tema_esport == "Pontuação Série A 2023":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[29, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[17, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_esport} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
#######################################################################################################################################

    elif tema_esport == "Bilheteria Série A (R$ milhões)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[31, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.10),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2022', '2023']

        tópico2 = df6.iloc[19, 1:].values
        club_data = {
            'América': tópico2[:3][::-1][:3],
            'Atlético': tópico2[3:6][::-1][:3],
            'Athletico': tópico2[6:9][::-1][:3],
            'Bahia': tópico2[9:12][::-1][:3],
            'Botafogo': tópico2[12:15][::-1][:3],
            'Corinthians': tópico2[15:18][::-1][:3],
            'Coritiba': tópico2[18:21][::-1][:3],
            'Cruzeiro': tópico2[21:24][::-1][:3],
            'Cuiabá': tópico2[24:27][::-1][:3],
            'Flamengo': tópico2[27:30][::-1][:3],
            'Fluminense': tópico2[30:33][::-1][:3],
            'Fortaleza': tópico2[33:36][::-1][:3],
            'Grêmio': tópico2[36:39][::-1][:3],
            'Goiás': tópico2[39:42][::-1][:3],
            'Internacional': tópico2[42:45][::-1][:3],
            'Palmeiras': tópico2[45:48][::-1][:3],
            'Santos': tópico2[48:51][::-1][:3],
            'São Paulo': tópico2[51:54][::-1][:3],
            'Vasco': tópico2[54:57][::-1][:3]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
#######################################################################################################################################

    elif tema_esport == "Bilheteria média (R$ mil/jogo)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[32, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2022', '2023']

        tópico2 = df6.iloc[20, 1:].values
        club_data = {
            'América': tópico2[:3][::-1][:3],
            'Atlético': tópico2[3:6][::-1][:3],
            'Athletico': tópico2[6:9][::-1][:3],
            'Bahia': tópico2[9:12][::-1][:3],
            'Botafogo': tópico2[12:15][::-1][:3],
            'Corinthians': tópico2[15:18][::-1][:3],
            'Coritiba': tópico2[18:21][::-1][:3],
            'Cruzeiro': tópico2[21:24][::-1][:3],
            'Cuiabá': tópico2[24:27][::-1][:3],
            'Flamengo': tópico2[27:30][::-1][:3],
            'Fluminense': tópico2[30:33][::-1][:3],
            'Fortaleza': tópico2[33:36][::-1][:3],
            'Grêmio': tópico2[36:39][::-1][:3],
            'Goiás': tópico2[39:42][::-1][:3],
            'Internacional': tópico2[42:45][::-1][:3],
            'Palmeiras': tópico2[45:48][::-1][:3],
            'Santos': tópico2[48:51][::-1][:3],
            'São Paulo': tópico2[51:54][::-1][:3],
            'Vasco': tópico2[54:57][::-1][:3]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
#######################################################################################################################################

    elif tema_esport == "Público Médio (pagantes)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[33, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=14)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2022', '2023']

        tópico2 = df6.iloc[21, 1:].values
        club_data = {
            'América': tópico2[:3][::-1][:3],
            'Atlético': tópico2[3:6][::-1][:3],
            'Athletico': tópico2[6:9][::-1][:3],
            'Bahia': tópico2[9:12][::-1][:3],
            'Botafogo': tópico2[12:15][::-1][:3],
            'Corinthians': tópico2[15:18][::-1][:3],
            'Coritiba': tópico2[18:21][::-1][:3],
            'Cruzeiro': tópico2[21:24][::-1][:3],
            'Cuiabá': tópico2[24:27][::-1][:3],
            'Flamengo': tópico2[27:30][::-1][:3],
            'Fluminense': tópico2[30:33][::-1][:3],
            'Fortaleza': tópico2[33:36][::-1][:3],
            'Grêmio': tópico2[36:39][::-1][:3],
            'Goiás': tópico2[39:42][::-1][:3],
            'Internacional': tópico2[42:45][::-1][:3],
            'Palmeiras': tópico2[45:48][::-1][:3],
            'Santos': tópico2[48:51][::-1][:3],
            'São Paulo': tópico2[51:54][::-1][:3],
            'Vasco': tópico2[54:57][::-1][:3]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)


#######################################################################################################################################
#######################################################################################################################################
        
    elif tema_esport == "Sócios-Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[34, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=14)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################
########################################################################################################################################

    elif tema_esport == "Valor do Elenco (€ milhões)":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_esport:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[37, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_esport}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################
########################################################################################################################################

    tema_ger = st.selectbox("Escolha o Tema Gerencial", options=temas_ger, index=None, placeholder="Escolha o Tema Gerencial!")
    fontsize = 24
    if tema_ger == "Público Médio / Sócios-Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger} (%)</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[35, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (%)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height*100:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Receita Operacional Líquida / Base de Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ / Torcedor)</b></h6>", unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[38, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[22, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.0f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_ger == "Receita Operacional Líquida / Sócios Torcedores":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ mil / Torcedor)</b></h6>", unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[39, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Receita com Venda de Direitos Econômicos / Gastos com a Base":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[40, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=19, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[23, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.1f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=12.5, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=12.5, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_ger == "Receita com Venda de Direitos Econômicos / Pontuação Série A":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ milhões / Ponto conquistado)</b></h6>", unsafe_allow_html=True)

        st.markdown("---")

        tópico = df1.iloc[41, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=18, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[24, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.1f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=12.5, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12, left=False, labelleft=False)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_ger == "Receita com Premiação / Folha do Futebol":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[42, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[25, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.2f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_ger == "Folha do futebol / Pontuação Série A":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ milhões / Ponto conquistado)</b></h6>", unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[43, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[26, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.1f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

#######################################################################################################################################
########################################################################################################################################

    elif tema_ger == "Receita Operacional Líquida / Pontuação Série A":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ milhões / Ponto conquistado)</b></h6>", unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[44, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[27, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.1f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################

    elif tema_ger == "Dívida / Receita Operacional Líquida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[50, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[31, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.2f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################

    elif tema_ger == "Folha do futebol / Receita Operacional Líquida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[51, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[32, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.2f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (%)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################

    elif tema_ger == "Folha futebol + Compra jogadores / Rec Oper Líquida":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[52, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

#######################################################################################################################################

        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa 2019-2023 (em moeda constante)</b></h4>", unsafe_allow_html=True)
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{highlight:} (em destaque)</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        years = ['2019', '2020', '2021', '2022', '2023']

        tópico2 = df3.iloc[33, 1:].values
        club_data = {
            'América': tópico2[:5][::-1][:5],
            'Atlético': tópico2[5:10][::-1][:5],
            'Athletico': tópico2[10:15][::-1][:5],
            'Bahia': tópico2[15:20][::-1][:5],
            'Botafogo': tópico2[20:25][::-1][:5],
            'Corinthians': tópico2[25:30][::-1][:5],
            'Coritiba': tópico2[30:35][::-1][:5],
            'Cruzeiro': tópico2[35:40][::-1][:5],
            'Cuiabá': tópico2[40:45][::-1][:5],
            'Flamengo': tópico2[45:50][::-1][:5],
            'Fluminense': tópico2[50:55][::-1][:5],
            'Fortaleza': tópico2[55:60][::-1][:5],
            'Grêmio': tópico2[60:65][::-1][:5],
            'Goiás': tópico2[65:70][::-1][:5],
            'Internacional': tópico2[70:75][::-1][:5],
            'Palmeiras': tópico2[75:80][::-1][:5],
            'Santos': tópico2[80:85][::-1][:5],
            'São Paulo': tópico2[85:90][::-1][:5],
            'Vasco': tópico2[90:95][::-1][:5]
        }

        # Plotting each club's data
        fig, ax = plt.subplots(figsize=(11, 8))  # Set the size of the plot

        # Plot each club's data
        for club, data in club_data.items():
            if club == highlight:
                ax.plot(years, data, label=club, linewidth=3.5, linestyle='-', color='steelblue')  # Highlighted line
                # Annotate each point on the highlighted club's line
                for i, value in enumerate(data):
                    ax.annotate(f'{value:.2f}',  # Text to display
                                (years[i], value),  # Point to annotate
                                textcoords="offset points",  # how to position the text
                                xytext=(0,10),  # distance from text to points (x,y)
                                ha='center',  # horizontal alignment can be left, right or center
                                va='bottom',
                                fontsize=14, 
                                fontweight='bold')
            else:
                ax.plot(years, data, label=club, linewidth=1, linestyle='--', color='black')  # Non-highlighted lines

        # Adding titles and labels
        #ax.set_xlabel('Anos', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (%)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot
        st.pyplot(fig)

########################################################################################################################################

    elif tema_ger == "Receita c/ Pay-per-View":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center;  color: black;'>(R$ milhões)</b></h6>", unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[56, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=True)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger} (R$ milhões)', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################

    elif tema_ger == "Despesas Administrativas / Folha do Futebol":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{tema_ger:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Univariada (2023)</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        tópico = df1.iloc[57, 1:].values

        # Pairing clubs with their revenues and sorting them by revenue in descending order
        paired_clubs_revenues = sorted(zip(clubes, tópico), key=lambda x: x[1], reverse=False)
        sorted_clubes, sorted_revenues = zip(*paired_clubs_revenues)

        def getImage(url):
            try:
                with urllib.request.urlopen(url) as response:
                    img = Image.open(response)
                    return OffsetImage(img, zoom=1.25)
            except Exception as e:
                st.error(f"Error loading image from {url}: {e}")
                return None

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_xlim(-0.5, len(sorted_clubes)-0.5)
        # Set ylim if necessary to create space for club icons

        # Increase the ylim if necessary to create more space for club icons
        max_revenue = max(sorted_revenues)
        ax.set_ylim(-max_revenue*0.2, max_revenue*1.07)  # Adjusting space at the bottom for icons

        bars = ax.bar(range(len(sorted_clubes)), sorted_revenues, color='skyblue')

        # Modify this part of your plotting code
        for i, club in enumerate(sorted_clubes):
            img_path = club_image_paths.get(club)
            if img_path:
                img = getImage(img_path)
                if img:
                    # Get the index for the selected categories (eixo_x, eixo_y)
                    ab = AnnotationBbox(img, (i, -max_revenue*0.15),  # Adjusting for better alignment
                                        xycoords='data', boxcoords="data",
                                        box_alignment=(0.5, 0), frameon=False)
                    ax.add_artist(ab)
                else:
                    print(f"Failed to load image for {club}")

        ax.set_xticks([])

        #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
        ax.set_ylabel(f'{tema_ger}', fontsize=20, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16, left=False, labelleft=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Adding text above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=15)

        fig.tight_layout()
        st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################

elif choose == "Análise Comparativa Bivariada":
    fontsize = 24
    st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Bivariada<br>2023</b></h4>", unsafe_allow_html=True)
    st.markdown("---")

    eixo_x = st.selectbox("Escolha o primeiro Tema (eixo horizontal)", options=temas_x, index=None, placeholder="Escolha o primeiro Tema!")
    eixo_y = st.selectbox("Escolha o primeiro Tema (eixo vertical)", options=temas_y, index=None, placeholder="Escolha o segundo Tema!")
    if eixo_x:
        # Filtering the row where column 0 matches the category (eixo_x)
        filtered_row_x = df1.loc[df1.iloc[:, 0] == eixo_x]
        # Capturing columns "1:" from the filtered row
        result_x = filtered_row_x.iloc[:, 1:20].values.flatten()  # Flattening the result for easy handling
        if eixo_y:
            # Filtering the row where column 0 matches the category (eixo_x)
            filtered_row_y = df1.loc[df1.iloc[:, 0] == eixo_y]
            # Capturing columns "1:" from the filtered row
            result_y = filtered_row_y.iloc[:, 1:20].values.flatten()  # Flattening the result for easy handling
            # Plotting using "fig"
            fig, ax = plt.subplots(figsize=(10, 7))

            club_image_paths = {club: f'https://raw.githubusercontent.com/JAmerico1898/Financials/49279e3070c69907190ddd0762322bb47fb0eac7/{alt_club}.png'
                    for club, alt_club in zip(clubs['Clubes'], alt_clubs['alt_clubs'])}
            def getImage(url):
                try:
                    with urllib.request.urlopen(url) as response:
                        img = Image.open(response)
                        return OffsetImage(img, zoom=0.65)
                except Exception as e:
                    st.error(f"Error loading image from {url}: {e}")
                    return None

            # Modify this part of your plotting code
            for i, club in enumerate(df1.columns[1:]):
                img_path = club_image_paths.get(club)
                if img_path:
                    img = getImage(img_path)
                    if img:
                        # Get the index for the selected categories (eixo_x, eixo_y)
                        x = result_x[i]
                        y = result_y[i]
                        ab = AnnotationBbox(img, (x, y), frameon=False)
                        ax.add_artist(ab)
                    else:
                        print(f"Failed to load image for {club}")

            # Calculate coefficients for the line of best fit
            slope, intercept = np.polyfit(result_x, result_y, 1)  # 1 means linear fit

            # Generate y-values based on the fit for plotting
            fit_line = np.polyval([slope, intercept], result_x)

            # Plot the line of best fit
            ax.plot(result_x, fit_line, color='red', linestyle='-', linewidth=2, label='OLS Regression Line')

            # Plotting using "fig"
            ax.scatter(result_x, result_y, color='green', alpha=0.5)
            ax.set_title(f'{eixo_x} vs {eixo_y}', fontsize=15, fontweight='bold', pad=25)
            ax.set_xlabel(eixo_x, fontsize=13, fontweight='bold')
            ax.set_ylabel(eixo_y, fontsize=13, fontweight='bold')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.set_ylim([min(result_y) - 1, max(result_y) + 20])
            #current_ticks = ax.get_xticks()
            #ax.set_xticklabels([f'{int(tick)}' for tick in current_ticks])

            # Calculate Pearson correlation coefficient
            corr_coef, _ = pearsonr(result_x, result_y)

            ax.text(0.95, 0.05, f'Pearson r={corr_coef:.2f}', transform=ax.transAxes, 
            horizontalalignment='right', verticalalignment='bottom', fontsize=12)

            # Dynamically adjust y-axis limits based on data
            y_min, y_max = min(result_y), max(result_y)
            if y_max <= 1:  # Check if the data is in the range 0 to 1
                y_range = y_max - y_min
                ax.set_ylim([y_min - 0.1 * y_range, y_max + 0.1 * y_range])
            else:
                ax.set_ylim([y_min - 1, y_max + 20])

            # Updating x-tick labels
            current_ticks = ax.get_xticks()
            ax.set_xticklabels([f'{int(tick)}' if tick.is_integer() else f'{tick:.2f}' for tick in current_ticks])

            plt.tight_layout()
            st.pyplot(fig)

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

if choose == "Análise Individual - Histórica":
    clube = st.selectbox("Escolha o Clube", options=clubes, index=None, placeholder="Escolha o Clube!")
    fontsize = 24

    if clube == "América":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 1:6]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Sócio-Torcedor."
        note_text_3 = "3. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 1:6]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 26], 1:6]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 1:6]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Atlético":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 6:11]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")


        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 6:11]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 6:11]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 6:11]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Athletico":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 11:16]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Nota:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 11:16]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 11:16]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 11:16]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Bahia":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 16:21]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Sócio-Torcedor."
        note_text_3 = "3. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 11:16]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 11:16]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 11:16]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Botafogo":
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 21:26]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Sócio-Torcedor."
        note_text_3 = "3. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 21:26]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 21:26]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 21:26]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Corinthians":
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 26:31]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 26:31]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of binary
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Nota:"
        note_text_1 = "1. O clube não informa com clareza os Gastos com a Base."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 26:31]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of binary
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 26:31]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of binary
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Coritiba":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 31:36]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 31:36]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Nota:"
        note_text_1 = "1. O clube não informa com clareza os Gastos com a Base."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 31:36]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 31:36]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Cruzeiro":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 36:41]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 36:41]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 36:41]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 36:41]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Cuiabá":
        markdown_1 = f"<div style='text-align:center;  color: gold; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 41:46]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Wistia')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Sócio-Torcedor."
        note_text_3 = "3. O clube não informa com clareza a Receita com Licenciamento da Marca."
        note_text_4 = "4. O clube não informa com clareza a Receita com Negociação de Atletas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.49, note_text_4, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 41:46]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Wistia')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube não informa com clareza a Aquisição de Atletas."
        note_text_2 = "2. O clube não informa com clareza os Gastos com a Base."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: gold; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 41:46]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Wistia')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 41:46]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Wistia')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Flamengo":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 46:51]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 46:51]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 46:51]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 46:51]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Fluminense":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 51:56]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 51:56]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 51:56]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 51:56]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Fortaleza":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 56:61]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 56:61]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 56:61]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 56:61]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Grêmio":
        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 61:66]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Match-Day."
        note_text_3 = "3. O clube não informa com clareza a Receita com Sócio-Torcedor (Rec Patrimoniais)."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")


        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 61:66]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: blue; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 61:66]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 61:66]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Goiás":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 66:71]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 66:71]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 66:71]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 66:71]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Internacional":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 71:76]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=18, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita com Sócio-Torcedor em conjunto com a Receita de Sócios Patrimoniais."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 71:76]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 71:76]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 71:76]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Palmeiras":
        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 76:81]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of greens
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 76:81]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: green; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 76:81]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 76:81]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greens')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Santos":
        markdown_1 = f"<div style='text-align:center;  color: grey; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[1:7, 8], 81:86]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greys
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Transmissão + Premiação", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Notas:"
        note_text_1 = "1. O clube informa a Receita de Premiação em conjunto com a Receita de Transmissão."
        note_text_2 = "2. O clube não informa com clareza a Receita com Sócio-Torcedor."
        note_text_3 = "3. O clube não informa com clareza a Receita com Licenciamento da Marca."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_1, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.37, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.43, note_text_3, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 81:86]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: gray; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 81:86]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 81:86]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Greys')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "São Paulo":
        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 86:91]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greys
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        note_text = "Nota: Em 2023, o São Paulo informou a Receita c/ Direitos de Transmissão em conjunto com a"
        note_text_2 = "Receita c/ Premiações."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")


        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 86:91]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: red; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 86:91]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 86:91]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of reds
        cmap = plt.get_cmap('Reds')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

    if clube == "Vasco":
        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Receitas e Despesas</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em R$ milhões, em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        def main():
            # URL of the image (make sure it's the raw version if it's hosted on GitHub)
            image_url = 'https://raw.githubusercontent.com/JAmerico1898/Financials/975782cba0c76542a7d5a3c8287c3eda0ad132b3/vasco_4.jpg'

            # Fetch the image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Display the image
            col1, col2, col3 = st.columns([1,2,1])
            with col2:  # Use the middle column to display the image
                st.image(image, caption='', use_column_width=True)

        if __name__ == "__main__":
            main()        

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[28, 2:7, 8], 91:96]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Greys
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Direitos de transmissão", "Publicidade e patrocínio", "Match-Day", 
                 "Sócio-torcedor", "Premiações", "Licenciamento da marca", "Negociação de atletas"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Receitas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Receitas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[10, 13:15], 91:96]
        selected_data = selected_data.round(0)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of Blues
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        # Adding value labels on top of each bar
        for p in ax.patches:
            # Format the height as integer
            height = int(p.get_height())  # Convert to integer to avoid decimals
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Folha do futebol (Pessoal + Imagem)", "Aquisições de atletas", "Gastos com a Base"]
        
        # Function to break labels into two lines if longer than a given number of characters
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Split the label by spaces and attempt to divide into two roughly equal parts
                    words = label.split()
                    midpoint = len(words) // 2
                    label = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=19, rotation=0)
        ax.set_title('Despesas', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: Em 2023, o Clube informou adições desprezíveis de Atletas em Formação na"
        note_text_2 = "Nota Explicativa sobre Intangíveis. Por esse motivo, o valor aparece zerado."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################
######################################################################################################################

        markdown_1 = f"<div style='text-align:center;  color: black; font-weight: bold; font-size:{fontsize}px'>{clube:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Histórico de Índices</b></h4>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;  color: black;'>(em moeda constante)<br></b></h5>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[22:25, 27], 91:96]
        selected_data = selected_data.round(1)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of binary
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.9, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=16)

        # Setting the labels and title using ax methods
        custom_labels = ["Rec Oper Líquida / Base Torcedores", 
                         "Rec Venda Jogadores / Gastos Base", 
                         "Rec Venda Jogadores / Pontuação Série A",
                         "Rec Oper Líquida / Pontuação Série A"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em Reais/torcedor, Proporção de gastos na base,"
        note_text_2 = "e milhões/ponto conquistado nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

######################################################################################################################

        st.markdown("---")

        # Selecting the rows 1 to 6 and columns 76 to 81
        selected_data = df3.iloc[np.r_[25:27, 31, 33], 91:96]
        selected_data = selected_data.round(2)
        selected_data.columns = [2023, 2022, 2021, 2020, 2019]

        # Create a colormap of binary
        cmap = plt.get_cmap('binary')
        colors = cmap(np.linspace(1, 0.3, num=len(selected_data.columns)))

        # Creating a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plotting using ax
        selected_data.plot(kind='bar', ax=ax, width=0.95, color=colors)

        for p in ax.patches:
            # Format the height with one decimal place
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=14)

        # Setting the labels and title using ax methods
        custom_labels = ["Receita com Premiação / Folha do Futebol",
                         "Folha do futebol / Pontuação Série A", 
                         "Dívida / Rec Oper Líquida", 
                         "Folha futebol + Compra jogadores / Rec Oper Líquida"]
        
        def adjust_labels(labels, max_len=18):
            adjusted_labels = []
            for label in labels:
                if len(label) > max_len:
                    # Find the index of the slash in the label
                    slash_index = label.find('/')
                    if slash_index != -1:
                        # Split the label right after the slash and keep the slash at the end of the first line
                        label = label[:slash_index + 1] + '\n' + label[slash_index + 1:]
                adjusted_labels.append(label)
            return adjusted_labels

        # Apply the function to custom_labels
        adjusted_custom_labels = adjust_labels(custom_labels)

        ax.set_xticklabels(adjusted_custom_labels, fontsize=16, rotation=0)
        #ax.set_title('Índices', fontsize=24, fontweight="bold")
        ax.tick_params(axis='y', labelsize=16)
        ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=5, fontsize=18, frameon=False)
        #ax.set_ylabel('Despesas (em R$ milhões, em moeda constante)', fontsize=18)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Adding a note below the graph using the axes
        note_text = "Nota: As variáveis estão, respectivamente, em % da Folha do futebol, milhões/ponto conquistado,"
        note_text_2 = "e % da Rec Operacional Líquida nas duas últimas."
        ax.text(0, -0.25, note_text, transform=ax.transAxes, ha="left", fontsize=18, color="black")
        ax.text(0, -0.31, note_text_2, transform=ax.transAxes, ha="left", fontsize=18, color="black")

        # Adjust layout and show plot
        fig.tight_layout()
        st.pyplot(fig)        

        def main():
            # URL of the image (make sure it's the raw version if it's hosted on GitHub)
            image_url = 'https://raw.githubusercontent.com/JAmerico1898/Financials/975782cba0c76542a7d5a3c8287c3eda0ad132b3/vasco_1.png'

            # Fetch the image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Display the image
            col1, col2, col3 = st.columns([1,2,1])
            with col2:  # Use the middle column to display the image
                st.image(image, caption='', use_column_width=True)

        if __name__ == "__main__":
            main()        



######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

elif choose == "Índice de Transparência":
    st.markdown("<h4 style='text-align: center;  color: black;'>Índice de Transparência das<br> Demonstrações Financeiras - 2023</b></h4>", unsafe_allow_html=True)
    #st.markdown("---")

    def main():
        royal_style = """
        <style>
            .royal-text {
                font-family: 'Times New Roman', Times, serif; /* Classic, formal font */
                font-size: 18px; /* Larger text size */
                color: #000080; /* Royal blue color */
                text-align: center; /* Centered text */
                margin: 18px; /* Adds space around the text */
            }
        </style>
        """

        text = """Inspirado nos trabalhos de Capelo, Grafietti, Kessel e Salomão (2021), Horvath e Vaško (2012) e Antunes, De Moraes e Grapiúna (2023)."""

        # Inject HTML with style
        st.markdown(royal_style, unsafe_allow_html=True)

        # Display styled text
        st.markdown(f'<div class="royal-text">{text}</div>', unsafe_allow_html=True)

    if __name__ == "__main__":
        main()    

    tópico = df4.iloc[0:3, 1:].transpose()

    # Retrieve labels for the bars from the first row
    labels = df4.iloc[0:3, 0]  # Assuming labels are in the first column

# Pairing clubs with their revenues and sorting them by revenue in descending order
    df_sorted = tópico.assign(Total=tópico.sum(axis=1)).sort_values(by='Total', ascending=False)
    sorted_clubes = df_sorted.index

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_ylim(-0.15 * df_sorted['Total'].max(), df_sorted['Total'].max() * 1.1)

    # Colors for the bars can be adjusted as needed
    colors = ['skyblue', 'lightgreen', 'salmon']
    bottom = None

    for name, color, label in zip(df_sorted.columns[:-1], colors, labels):
        bars = ax.bar(sorted_clubes, df_sorted[name], bottom=bottom, label=label, color=color)
        bottom = df_sorted[name] if bottom is None else bottom + df_sorted[name]

    def getImage(url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            return OffsetImage(img, zoom=1.25)
        except Exception as e:
            print(f"Error loading image from {url}: {e}")
            return None

    # Modify this part of your plotting code for images
    for i, club in enumerate(sorted_clubes):
        img_url = club_image_paths.get(club)
        if img_url:
            img = getImage(img_url)
            if img:
                ab = AnnotationBbox(img, (i, -0.05 * df_sorted['Total'].max()),  # Adjust this offset as needed
                                    xycoords='data', boxcoords="data",
                                    box_alignment=(0.5, 1), frameon=False)
                ax.add_artist(ab)
            else:
                print(f"Failed to load image for {club}")

    ax.set_xticks([])

    #ax.set_xlabel('Clubes', fontsize=20, fontweight='bold')
    ax.set_ylabel(f'Índice de Transparência', fontsize=20, fontweight='bold')
    ax.tick_params(axis='y', labelsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Adding text above bars
    cum_values = df_sorted.iloc[:, :-1].cumsum(axis=1)
    for i, club in enumerate(sorted_clubes):
        total_height = cum_values.loc[club, tópico.columns[-1]]
        ax.annotate(f'{total_height:.1f}', xy=(i, total_height),
                    xytext=(0, 3),  # 3 points vertical offset to place text above the bar
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=16)

    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fontsize=16, frameon=False, ncol=3)
    fig.tight_layout()
    st.pyplot(fig)

    #Detalhando
    st.markdown("<h4 style='text-align: center;  color: black;'><br>Detalhando o Índice de Transparência</b></h4>", unsafe_allow_html=True)
    #st.markdown("---")


    tabela = df5.iloc[0:4, 1:]
    tabela.set_index('Clubes', inplace=True)
    tabela_t = tabela.T
    # Sort the DataFrame by the last column, descendingly
    last_column = tabela_t.columns[-1]  # Get the last column name
    tabela_t = tabela_t.sort_values(by=last_column, ascending=False)

    # Styling DataFrame using Pandas
    def style_table(df):
        return df.style.format("{:.1f}").set_table_styles(
            [{
                'selector': 'thead th',
                'props': [('font-weight', 'bold'),
                        ('border-style', 'solid'),
                        ('border-width', '0px 0px 2px 0px'),
                        ('border-color', 'black')]
            }, {
                'selector': 'thead th:not(:first-child)',
                'props': [('text-align', 'center')]  # Centering all headers except the first
            }, {
                'selector': 'thead th:last-child',
                'props': [('color', 'red')]  # Make last column header red
            }, {
                'selector': 'td',
                'props': [('border-style', 'solid'),
                        ('border-width', '0px 0px 1px 0px'),
                        ('border-color', 'black'),
                        ('text-align', 'center')]
            }, {
                'selector': 'td:last-child',
                'props': [('font-weight', 'bold'),
                        ('color', 'red')]  # Make last column data bold and red
            }, {
                'selector': 'th',
                'props': [('border-style', 'solid'),
                        ('border-width', '0px 0px 1px 0px'),
                        ('border-color', 'black'),
                        ('text-align', 'left')]
            }]
        ).set_properties(**{
            'padding': '8px',
#            'text-align': 'center'
            
        })

    # Displaying in Streamlit
    def main():
        st.title("")

        # Convert the styled DataFrame to HTML and display it
        styled_html = style_table(tabela_t).to_html(escape=False)
        st.markdown(styled_html, unsafe_allow_html=True)

    if __name__ == '__main__':
        main()

    #Acessando a Metodologia do Índice: 
    st.markdown("<h4 style='text-align: center;  color: black;'><br>Metodologia do Índice de Transparência</b></h4>", unsafe_allow_html=True)

    #Downloading Transparency Index Methodology
    button = st.link_button("Metodologia do Índice", 'https://raw.githubusercontent.com/JAmerico1898/Financials/55e6685a50b56052dbb6ba674c963a1426044435/Indice%20de%20Transparencia%20-%20Metodologia.pdf')

    def main1():

        # URL of the PDF document
        # Make sure to use a raw string for the file path
        pdf_url = 'https://raw.githubusercontent.com/JAmerico1898/Financials/55e6685a50b56052dbb6ba674c963a1426044435/Indice%20de%20Transparencia%20-%20Metodologia.pdf'

        # Button to open PDF in a new tab
        if st.link_button('Metodologia do Índice'):
            # Open URL in a new tab using JavaScript
            js = f"window.open('{pdf_url}')"  # JavaScript to open a new window/tab
            st.markdown(f'<img src onerror="{js}">', unsafe_allow_html=True)

    if __name__ == '__main1__':
        main1()    

elif choose == "Metodologia da Análise":
    st.markdown("<h4 style='text-align: center;  color: black;'>Metodologia da Análise</b></h4>", unsafe_allow_html=True)
    st.markdown("---")

    #Downloading Transparency Index Methodology
    button = st.link_button("Metodologia da Análise", 'https://github.com/JAmerico1898/Financials/blob/f63bd35d8bf4073d1f669c83248604ffa4b9f217/Metodologia%20da%20Analise.pdf')

    def main2():

        # URL of the PDF document
        # Make sure to use a raw string for the file path
        pdf_url = 'https://github.com/JAmerico1898/Financials/blob/f63bd35d8bf4073d1f669c83248604ffa4b9f217/Metodologia%20da%20Analise.pdf'

        # Button to open PDF in a new tab
        if st.link_button('Metodologia da Análise'):
            # Open URL in a new tab using JavaScript
            js = f"window.open('{pdf_url}')"  # JavaScript to open a new window/tab
            st.markdown(f'<img src onerror="{js}">', unsafe_allow_html=True)

    if __name__ == '__main2__':
        main2()    



