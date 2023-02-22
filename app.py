import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import unidecode
from st_aggrid import AgGrid, GridOptionsBuilder,ColumnsAutoSizeMode

st.set_page_config(
  page_title='Estatísticas Over / Under Gols',
  page_icon='⚽',
  layout="wide")

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)
        
tab1,tab2 = st.tabs([
                  "📊 DESEMPENHO COMO MANDANTE",
                  "🥅 DESEMPENHO COMO VISITANTE"])

liga1 = ['alemanha','alemanha2','espanha','espanha2','franca','franca2',
            'inglaterra','inglaterra2','italia','belgica','holanda','portugal',
            'turquia','grecia','escocia']

liga2 = ['dinamarca','suica']

liga3 = ['noruega','suecia','brasil']

ligas = ['Alemanha','Alemanha2','Espanha','Espanha2','França','França2',
        'Inglaterra','Inglaterra2','Itália','Itália2','Bélgica','Holanda','Portugal',
        'Turquia','Grécia','Escócia','Dinamarca','Noruega','Suíça','Suécia',
        'Brasil','Austrália']

liga = st.sidebar.selectbox('Escolha a liga',ligas)
liga = unidecode.unidecode(liga.lower())

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
    
  link = 'https://www.football-data.co.uk/mmz4281/2223/'+ligacod+'.csv'
  df = pd.read_csv(link)
  df = df[['HomeTeam', 'AwayTeam', 'FTHG','FTAG']].copy()
  df.rename(columns={'HomeTeam':'Home','AwayTeam':'Away','FTHG': 'HG', 'FTAG': 'AG'}, inplace=True)

if liga in liga2:
  if liga == 'dinamarca':
    link = 'https://www.football-data.co.uk/new/DNK.csv'
  if liga == 'suica':
    link = 'https://www.football-data.co.uk/new/SWZ.csv'
  df = pd.read_csv(link)
  df = df.query("Season == '2022/2023'")

if liga in liga3:
  if liga == 'noruega':
    link = 'https://www.football-data.co.uk/new/NOR.csv'
  if liga == 'suecia':
    link = 'https://www.football-data.co.uk/new/SWE.csv'
  if liga == 'brasil':
    link = 'https://www.football-data.co.uk/new/BRA.csv'
  df = pd.read_csv(link)
  df = df.query("Season == 2022")

if liga == 'australia':
    df = pd.read_excel('https://www.aussportsbetting.com/historical_data/a-league.xlsx',skiprows=[0])
    df = df[['Date','Home Team', 'Away Team', 'Home Goals','Away Goals']].copy()
    df.rename(columns={'Home Team':'Home','Away Team':'Away','Home Goals': 'HG', 'Away Goals': 'AG'}, inplace=True)
    df = df.query('Date > "2022-10-01"')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.strftime('%d-%m-%Y')

def casa_fora(df):
  clubes = list(df.Home.unique())

  df['GOLS'] = df['HG'] + df['AG']
  df['AM'] = ((df['HG'] > 0) & (df['AG'] > 0)).astype(int)

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

  for clube in (clubes):
    casa = 'Home == "'+clube+'"'
    fora = 'Away == "'+clube+'"'

    taxa25c = 100 * (df_O25.query(casa).shape[0] / df.query(casa).shape[0])
    taxa25f = 100 * (df_O25.query(fora).shape[0] / df.query(fora).shape[0])
    taxa15c = 100 * (df_O15.query(casa).shape[0] / df.query(casa).shape[0])
    taxa15f = 100 * (df_O15.query(fora).shape[0] / df.query(fora).shape[0])
    taxa05c = 100 * (df_O5.query(casa).shape[0] / df.query(casa).shape[0])
    taxa05f = 100 * (df_O5.query(fora).shape[0] / df.query(fora).shape[0])
    taxaAMc = 100 * (df_AM.query(casa).shape[0] / df.query(casa).shape[0])
    taxaAMf = 100 * (df_AM.query(fora).shape[0] / df.query(fora).shape[0])

    tabela_H.append([clube,round(taxa05c,2),round(taxa15c,2),round(taxa25c,2),round(taxaAMc,2)])
    tabela_A.append([clube,round(taxa05f,2),round(taxa15f,2),round(taxa25f,2),round(taxaAMf,2)])

  tabela_H = pd.DataFrame(tabela_H, columns=['CLUBE','OVER 0.5','OVER 1.5','OVER 2.5','AMBAS'])
  tabela_A = pd.DataFrame(tabela_A, columns=['CLUBE','OVER 0.5','OVER 1.5','OVER 2.5','AMBAS'])
  
  return tabela_H, tabela_A

stats1,stats2 = casa_fora(df)
fontsize = '20px'

with tab1: 
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)    

    st.title('Aproveitamento como Mandante (%)')
    builder1 = GridOptionsBuilder.from_dataframe(stats1)
    builder1.configure_default_column(cellStyle={'color': 'black', 'font-size': fontsize},
                                        filterable=False,editable=False,
                                        sortable=False,resizable=False)

    go1 = builder1.build()

    AgGrid(stats1,gridOptions = go1,
    fit_columns_on_grid_load=True,
    theme="alpine",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True)

with tab2:
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    
    st.title('Aproveitamento como Visitante (%)')
    builder2 = GridOptionsBuilder.from_dataframe(stats2)
    builder2.configure_default_column(cellStyle={'color': 'black', 'font-size': fontsize},
                                        filterable=False,editable=False,
                                        sortable=False,resizable=False)

    go2 = builder2.build()

    AgGrid(stats2,gridOptions = go2,
    fit_columns_on_grid_load=True,
    theme="alpine",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True)