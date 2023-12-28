import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import unidecode
from plotly.subplots import make_subplots
import plotly.graph_objs as go

st.set_page_config(
  page_title='Estatísticas Over / Under Gols',
  page_icon='⚽',
  layout="wide")

liga1 = ['alemanha','alemanha2','espanha','espanha2','franca','franca2',
            'inglaterra','inglaterra2','italia','belgica','holanda','portugal',
            'turquia','grecia','escocia']

liga2 = ['dinamarca','suica']

liga3 = ['noruega','suecia','brasil']

ligas = ['Alemanha','Alemanha2','Espanha','Espanha2','França','França2',
        'Inglaterra','Inglaterra2','Itália','Itália2','Bélgica','Holanda','Portugal',
        'Turquia','Grécia','Escócia','Dinamarca','Noruega','Suíça','Suécia',
        'Brasil','Austrália']

def calcula(df, texto):
  # prompt: crie 2 dataframes, a partir do df, CASA e FORA e ordene ambos em ordem decrescente

  tab_casa = df.sort_values(by=['CASA'], ascending=True)
  tab_fora = df.sort_values(by=['FORA'], ascending=True)

  # prompt: crie 2 gráfico2 de barras com os dataframes tab_casa com o Título "TEXTO - MANDANTE" e tab_fora com o Título "TEXTO - VISITANTE"

  fig = make_subplots(
      rows=1, cols=2,
      shared_xaxes=True,
      vertical_spacing=0.05,
      horizontal_spacing=0.2,
      subplot_titles=("MANDANTE","VISITANTE")
  )

  fig.add_trace(
      go.Bar(
          x=tab_casa['CASA'],
          y=tab_casa['CLUBE'],
          name="CASA",
          orientation='h',
          marker_color='rgb(112, 112, 255)'
      ),
      row=1, col=1
  )

  fig.add_trace(
      go.Bar(
          x=tab_fora['FORA'],
          y=tab_fora['CLUBE'],
          name="FORA",
          orientation='h',
          marker_color='rgb(69, 94, 69)'
      ),
      row=1, col=2
  )

  fig.update_layout(
     font=dict(
     size=8,
     color="Black"
    ),
    title=atributo.upper() + ' - ' + liga.upper(),
      showlegend=False,
      barmode='group',
      height=800,
      width=1200,
      paper_bgcolor='rgb(255, 255, 255)',
      plot_bgcolor='rgb(240,240,240)',
  )
  
  st.plotly_chart(fig, use_container_width=True)

def casa_fora(df):
  clubes = list(df.Home.unique())

  df['GOLS'] = df['HG'] + df['AG']
  df['AM'] = ((df['HG'] > 0) & (df['AG'] > 0)).astype(int)

  # JOGOS 0X0
  df_0 = df.query('GOLS < 1')

  # JOGOS OVER 2.5
  df_O25 = df.query('GOLS > 2.5')

  # JOGOS OVER 1.5
  df_O15 = df.query('GOLS > 1.5')

  # JOGOS OVER 0.5
  df_O5 = df.query('GOLS > 0.5')

  # JOGOS AMBAS
  df_AM = df.query('AM == 1')

  tabela_H = []
  tabela_A = []
  tab_0x0 = []
  tab_05 = []
  tab_15 = []
  tab_25 = []
  tab_am = []

  for clube in (clubes):
    casa = 'Home == "'+clube+'"'
    fora = 'Away == "'+clube+'"'

    taxa25c = 100 * (df_O25.query(casa).shape[0] / df.query(casa).shape[0])
    taxa25f = 100 * (df_O25.query(fora).shape[0] / df.query(fora).shape[0])
    taxa15c = 100 * (df_O15.query(casa).shape[0] / df.query(casa).shape[0])
    taxa15f = 100 * (df_O15.query(fora).shape[0] / df.query(fora).shape[0])
    taxa05c = 100 * (df_O5.query(casa).shape[0] / df.query(casa).shape[0])
    taxa05f = 100 * (df_O5.query(fora).shape[0] / df.query(fora).shape[0])
    
    taxa0x0c = 100 * (df_0.query(casa).shape[0] / df.query(casa).shape[0])
    taxa0x0f = 100 * (df_0.query(fora).shape[0] / df.query(fora).shape[0])

    taxaAMc = 100 * (df_AM.query(casa).shape[0] / df.query(casa).shape[0])
    taxaAMf = 100 * (df_AM.query(fora).shape[0] / df.query(fora).shape[0])

    tabela_H.append([clube,round(taxa0x0c,2),round(taxa05c,2),round(taxa15c,2),round(taxa25c,2),round(taxaAMc,2)])
    tabela_A.append([clube,round(taxa0x0f,2),round(taxa05f,2),round(taxa15f,2),round(taxa25f,2),round(taxaAMf,2)])

    tab_0x0.append([clube,round(taxa0x0c,2),round(taxa0x0f,2)])
    tab_05.append([clube,round(taxa05c,2),round(taxa05f,2)])
    tab_15.append([clube,round(taxa15c,2),round(taxa15f,2)])
    tab_25.append([clube,round(taxa25c,2),round(taxa25f,2)])
    tab_am.append([clube,round(taxaAMc,2),round(taxaAMf,2)])

  tabela_H = pd.DataFrame(tabela_H, columns=['CLUBE','0x0','OVER 0.5','OVER 1.5','OVER 2.5','AMBAS'])
  tabela_A = pd.DataFrame(tabela_A, columns=['CLUBE','0x0','OVER 0.5','OVER 1.5','OVER 2.5','AMBAS'])

  tab_0x0 = pd.DataFrame(tab_0x0,columns=['CLUBE','CASA','FORA'])
  tab_05 = pd.DataFrame(tab_05,columns=['CLUBE','CASA','FORA'])
  tab_15 = pd.DataFrame(tab_15,columns=['CLUBE','CASA','FORA'])
  tab_25 = pd.DataFrame(tab_25,columns=['CLUBE','CASA','FORA'])
  tab_am = pd.DataFrame(tab_am,columns=['CLUBE','CASA','FORA'])
  
  if atributo == 'Over 0.5':
    df1 = tab_05
  elif atributo == 'Over 1.5':
    df1 = tab_15
  elif atributo == 'Over 2.5':
    df1 = tab_25
  elif atributo == 'Ambos Marcam':
    df1 = tab_am
  else:
    df1 = tab_0x0

  calcula(df1,atributo)

with st.container():
  liga = st.selectbox('Escolha a liga',ligas)
  liga = unidecode.unidecode(liga.lower())

  atributo = st.selectbox('Escolha o atributo:',('Over 0.5','Over 1.5', 'Over 2.5', 'Ambos Marcam','Jogos 0x0'))

  if liga in liga1:
    if liga == 'alemanha':
      ligacod = 'D1'
    if liga == 'alemanha2':
      ligacod = 'D2'
    if liga == 'espanha':
      ligacod = 'SP1'
    if liga == 'espanha2':
      ligacod = 'SP2'
    if liga == 'franca':
      ligacod = 'F1'
    if liga == 'franca2':
      ligacod = 'F2'
    if liga == 'inglaterra':
      ligacod = 'E0'
    if liga == 'inglaterra2':
      ligacod = 'E1'
    if liga == 'italia':
      ligacod = 'I1'
    if liga == 'italia2':
      ligacod = 'I2'
    if liga == 'belgica':
      ligacod = 'B1'
    if liga == 'holanda':
      ligacod = 'N1'
    if liga == 'portugal':
      ligacod = 'P1'
    if liga == 'turquia':
      ligacod = 'T1'
    if liga == 'grecia':
      ligacod = 'G1'
    if liga == 'escocia':
      ligacod = 'SC0'

    link = 'https://www.football-data.co.uk/mmz4281/2324/'+ligacod+'.csv'
    df = pd.read_csv(link)
    df = df[['HomeTeam', 'AwayTeam', 'FTHG','FTAG']].copy()
    df.rename(columns={'HomeTeam':'Home','AwayTeam':'Away','FTHG': 'HG', 'FTAG': 'AG'}, inplace=True)

  if liga in liga2:
    if liga == 'dinamarca':
      link = 'https://www.football-data.co.uk/new/DNK.csv'
    if liga == 'suica':
      link = 'https://www.football-data.co.uk/new/SWZ.csv'
    df = pd.read_csv(link)
    df = df.query("Season == '2023/2024'")

  if liga in liga3:
    if liga == 'noruega':
      link = 'https://www.football-data.co.uk/new/NOR.csv'
    if liga == 'suecia':
      link = 'https://www.football-data.co.uk/new/SWE.csv'
    if liga == 'brasil':
      link = 'https://www.football-data.co.uk/new/BRA.csv'
    df = pd.read_csv(link)
    df = df.query("Season == 2023")

  if liga == 'australia':
      df = pd.read_excel('https://www.aussportsbetting.com/historical_data/a-league.xlsx',skiprows=[0])
      df = df[['Date','Home Team', 'Away Team', 'Home Goals','Away Goals']].copy()
      df.rename(columns={'Home Team':'Home','Away Team':'Away','Home Goals': 'HG', 'Away Goals': 'AG'}, inplace=True)
      df = df.query('Date > "2023-10-01"')
      df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.strftime('%d-%m-%Y')

  casa_fora(df)
