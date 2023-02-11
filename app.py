import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import unidecode
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode,ColumnsAutoSizeMode

st.set_page_config(
  page_title='Favorito segundo as odds - BET365',
  page_icon='⚽',
  layout="wide")

st.sidebar.header(
    """
    **LIGAS**

    """
)
tab1,tab2 = st.tabs([
                  "📊 ESTATÍSTICAS",
                  "🥅 FAVORITOS"])

def limpa_e_calcula(liga,ano):
    liga1 = ['alemanha','alemanha2','espanha','espanha2','franca','franca2',
            'inglaterra','inglaterra2','italia','belgica','holanda','portugal',
            'turquia','grecia','escocia']

    liga = unidecode.unidecode(liga.lower())
    
    if liga in liga1:
        if liga == 'alemanha':
            ligacod = 'D1'
        if liga == 'alemanha2':
            ligacod = 'D1'
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

        if ano == '2022/2023':
            anocod = '2223'
        if ano == '2021/2022':
            anocod = '2122'
        if ano == '2020/2021':
            anocod = '2021'

        link = 'https://www.football-data.co.uk/mmz4281/'+anocod+'/'+ligacod+'.csv'

    else:
        if liga == 'dinamarca':
            link = 'https://www.football-data.co.uk/new/DNK.csv'
        if liga == 'noruega':
            link = 'https://www.football-data.co.uk/new/NOR.csv'
        if liga == 'suica':
            link = 'https://www.football-data.co.uk/new/SWZ.csv'
        if liga == 'suecia':
            link = 'https://www.football-data.co.uk/new/SWE.csv'
        if liga == 'brasil':
            link = 'https://www.football-data.co.uk/new/BRA.csv'

    df = pd.read_csv(link)

    if liga in liga1:
        df.drop(['Div','Time','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','BWH','BWD','BWA','IWH','IWD',
                    'IWA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA','P>2.5',
                    'P<2.5','Max>2.5','Max<2.5','Avg>2.5','Avg<2.5','AHh','B365AHH','B365AHA','PAHH','PAHA','MaxAHH','MaxAHA','AvgAHH',
                    'AvgAHA','B365CH','B365CD','B365CA','BWCH','BWCD','BWCA','IWCH','IWCD','IWCA','PSCH','PSCD','PSCA','WHCH','WHCD',
                    'WHCA','VCCH','VCCD','VCCA','MaxCH','MaxCD','MaxCA','AvgCH','AvgCD','AvgCA','B365C>2.5','B365C<2.5','PC>2.5',
                    'PC<2.5','MaxC>2.5','MaxC<2.5','AvgC>2.5','AvgC<2.5','AHCh','B365CAHH','B365CAHA','PCAHH','PCAHA','MaxCAHH',
                    'MaxCAHA','AvgCAHH','AvgCAHA','HTHG','HTAG','HTR','B365>2.5','B365<2.5'],axis=1,inplace=True)
        
        df.rename(columns={'HomeTeam':'Home','AwayTeam':'Away','FTHG': 'HG', 'FTAG': 'AG','FTR':'Res','B365H':'PH','B365D':'PD','B365A':'PA'}, inplace=True)
    
    else:
        if liga in ['dinamarca','suica']:
            df = df.query("Season == " + ano)
        else:
            if ano == '2020/2021':
                ano1 = '2021'
            if ano == '2021/2022':
                ano1 = '2022'
            if ano == '2022/2023':
                ano1 = '2023'
            df = df.query("Season == "+ano1)

        df.drop(['Country','League','Season','Time','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA'],axis=1,inplace=True)

    clubes = list(df.Home.unique())

    casa = st.sidebar.selectbox('Mandante',clubes)
    fora = st.sidebar.selectbox('Visitante',clubes)
    
    df['GOLS'] = df['HG'] + df['AG']

    def fav_h(df):
        if (df['PH'] <= df['PA']):
            if (df['PH'] <= df['PD']):
                return 1
        else:
            return 0

    def fav_a(df):
        if (df['PA'] <= df['PH']):
            if (df['PA'] <= df['PD']):
                return 1
        else:
            return 0

    def fav_d(df):
        if (df['FAV_H'] == 1):
            return 0       
        if (df['FAV_A'] == 1):
            return 0
        else:
            return 1

    def fav_bet(df):
        if (df['FAV_H']  == 1):
            return "H"
        elif (df['FAV_A'] == 1):
            return "A"
        else:
            return "D"

    def fav_fim(df):
        if (df['Res'] == df['FAV_BET']):
            return 1
        else:
            return 0

    def tabela(df,time,mando):
        if mando == "casa":
            txt = 'Home == "'+time+'" & FAV_H == 1'
            tmp1 = df.query(txt).sum()[-5]
        else:
            txt = 'Away == "'+time+'" & FAV_A == 1'
            tmp1 = df.query(txt).sum()[-4]
        
        tmp2 = df.query(txt).sum()[-1]
        
        if tmp1 > 0:
            des = 100 * tmp2 / tmp1
            return round(des,2),tmp1
        else:
            return 0,tmp1
    
    def desempenho(tabH,tabA,liga):
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(16,12))
        fs = 20
        ls = 20
        tabH = tabH.sort_values(tabH.columns[1],ascending=True)
        tabA = tabA.sort_values(tabA.columns[1],ascending=True)

        jgH = list(tabH.JOGOS)
        jgA = list(tabA.JOGOS)

        ax1.barh(tabH.CLUBE,tabH.APROVEITAMENTO,height=0.6,color='green',edgecolor="k",linewidth=0.3)
        ax2.barh(tabA.CLUBE,tabA.APROVEITAMENTO,height=0.6,color='green',edgecolor="k",linewidth=0.3)

        ax1.set_title('Favorito como Mandante (# jogos)',fontsize=fs)
        ax1.set_facecolor('ivory')
        ax1.set_xlabel('Aproveitamento %',fontsize=20)
        ax1.grid(axis='x',color='k',alpha=0.3)
        ax1.tick_params(axis='y', which='major', labelsize=ls)
        ax1.tick_params(axis='x', which='both', labelsize=ls)
        ax1.set_xlim([0, 120])

        for i, p in enumerate(ax1.patches):
            #width = p.get_width()
            ax1.text(10+p.get_width(), p.get_y()+0.55*p.get_height(),
                    '({:2.0f})'.format(jgH[i]),
                    ha='center', va='center',size=fs)

        ax2.set_title('Favorito como Visitante (# jogos)',fontsize=fs)
        ax2.set_facecolor('ivory')
        ax2.set_xlabel('Aproveitamento %',fontsize=20)
        ax2.grid(axis='x',color='k',alpha=0.3)
        ax2.tick_params(axis='y', which='major', labelsize=ls)
        ax2.tick_params(axis='x', which='both', labelsize=ls)
        ax2.set_xlim([0, 120])

        for i, p in enumerate (ax2.patches):
            #width = p.get_width()
            ax2.text(10+p.get_width(), p.get_y()+0.55*p.get_height(),
                    '({:2.0f})'.format(jgA[i]),
                    ha='center', va='center',size=fs)
        
        fig.tight_layout(pad=3.0)
        with tab2:
            st.pyplot(fig)

    # CALCULO DOS FAVORITOS ====================================
    df['FAV_H'] = df.apply(fav_h,axis=1)
    df['FAV_A'] = df.apply(fav_a,axis=1)
    df['FAV_D'] = df.apply(fav_d,axis=1)
    df['FAV_BET'] = df.apply(fav_bet,axis=1)
    df['FAV'] = df.apply(fav_fim,axis=1)

    listaH = df.Home.unique()
    listaA = df.Away.unique()
    
    tabelaH=[]
    for time in listaH:
        des1,jc = tabela(df,time,'casa')
        tabelaH.append([time,des1,jc])
    
    tabelaA=[]
    for time in listaA:
        des2,jf = tabela(df,time,'fora')
        tabelaA.append([time,des2,jf])

    tabH = pd.DataFrame(tabelaH, columns=['CLUBE','APROVEITAMENTO','JOGOS'])
    tabA = pd.DataFrame(tabelaA, columns=['CLUBE','APROVEITAMENTO','JOGOS'])

    desempenho(tabH,tabA,liga)

    # FIM DO FAVORITO =================================================

    def ambas(df):
        if (df['HG'] > 0) & (df['AG'] > 0):
            return 1
        else:
            return 0
    
    df['AMBAS'] = df.apply(ambas,axis=1)

    # JOGOS OVER 2.5
    df_O25 = df.query('GOLS > 2.5')
    # JOGOS OVER 1.5
    df_O15 = df.query('GOLS > 1.5')
    # JOGOS OVER 0.5
    df_O5 = df.query('GOLS > 0.5')
    # JOGOS AMBAS MARCAM
    df_ambas = df.query('AMBAS == 1')
    
    stats1 = []
    stats2 = []
    textoc = 'Home == "'+casa+'"'
    textof = 'Away == "'+fora+'"'
    textoamc = 'Home == "'+casa+'" | Away == "'+casa+'"'
    textoamf = 'Home == "'+fora+'" | Away == "'+fora+'"'

    taxa_c_o05 = 100 * (df_O5.query(textoc).shape[0] / df.query(textoc).shape[0])
    taxa_c_o15 = 100 * (df_O15.query(textoc).shape[0] / df.query(textoc).shape[0])
    taxa_c_o25 = 100 * (df_O25.query(textoc).shape[0] / df.query(textoc).shape[0])
    taxa_am_c = 100 * (df_ambas.query(textoc).shape[0] / df.query(textoc).shape[0])
    taxa_f_o05 = 100 * (df_O5.query(textof).shape[0] / df.query(textof).shape[0])
    taxa_f_o15 = 100 * (df_O15.query(textof).shape[0] / df.query(textof).shape[0])
    taxa_f_o25 = 100 * (df_O25.query(textof).shape[0] / df.query(textof).shape[0])
    taxa_am_f = 100 * (df_ambas.query(textof).shape[0] / df.query(textof).shape[0])

    taxa_cg_o05 = 100 * (df_O5.query(textoamc).shape[0] / df.query(textoamc).shape[0])
    taxa_cg_o15 = 100 * (df_O15.query(textoamc).shape[0] / df.query(textoamc).shape[0])
    taxa_cg_o25 = 100 * (df_O25.query(textoamc).shape[0] / df.query(textoamc).shape[0])    
    taxa_amg_c = 100 * (df_ambas.query(textoamc).shape[0] / df.query(textoamc).shape[0])
    taxa_fg_o05 = 100 * (df_O5.query(textoamf).shape[0] / df.query(textoamf).shape[0])
    taxa_fg_o15 = 100 * (df_O15.query(textoamf).shape[0] / df.query(textoamf).shape[0])
    taxa_fg_o25 = 100 * (df_O25.query(textoamf).shape[0] / df.query(textoamf).shape[0])    
    taxa_amg_f = 100 * (df_ambas.query(textoamf).shape[0] / df.query(textoamf).shape[0])

    stats1.append([casa,round(taxa_c_o05),round(taxa_c_o15),round(taxa_c_o25),round(taxa_am_c)])
    stats1.append([fora,round(taxa_f_o05),round(taxa_f_o15),round(taxa_f_o25),round(taxa_am_f)])
    stats1.append(['MÉDIA',round((taxa_c_o05+taxa_f_o05)/2),round((taxa_c_o15+taxa_f_o15)/2),
                          round((taxa_c_o25+taxa_f_o25)/2),round((taxa_am_c+taxa_am_f)/2)])

    stats2.append([casa,round(taxa_cg_o05),round(taxa_cg_o15),round(taxa_cg_o25),round(taxa_amg_c)])
    stats2.append([fora,round(taxa_fg_o05),round(taxa_fg_o15),round(taxa_fg_o25),round(taxa_amg_f)])
    stats2.append(['MÉDIA',round((taxa_cg_o05+taxa_fg_o05)/2),round((taxa_cg_o15+taxa_fg_o15)/2),
                          round((taxa_cg_o25+taxa_fg_o25)/2),round((taxa_amg_c+taxa_amg_f)/2)])
    
    stats1 = pd.DataFrame(stats1, columns=['CLUBE','0.5 (%)','1.5 (%)','2.5 (%)','AM (%)'],
                index=['Mandante','Visitante','MÉDIA'])

    stats2 = pd.DataFrame(stats2, columns=['CLUBE','0.5 (%)','1.5 (%)','2.5 (%)','AM (%)'],
                index=['','','MÉDIA'])
    with tab1:
        stats1.reset_index(inplace=True)
        stats2.reset_index(inplace=True)
        stats1.rename(columns={ stats1.columns[0]: " " }, inplace = True)
        stats2.rename(columns={ stats2.columns[0]: " " }, inplace = True)

        st.title('Estatísticas por mando')

        builder = GridOptionsBuilder.from_dataframe(stats1)
        builder.configure_default_column(filterable=False,editable=False,sortable=False,resizable=False)

        go = builder.build()

        AgGrid(stats1,gridOptions = go,
        fit_columns_on_grid_load=True,
        theme="alpine",
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True)

        st.title('Estatísticas por time')
        builder = GridOptionsBuilder.from_dataframe(stats2)
        builder.configure_default_column(filterable=False,editable=False,sortable=False,resizable=False)

        go = builder.build()

        AgGrid(stats2,gridOptions = go,
        fit_columns_on_grid_load=True,
        theme="alpine",
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True)

def figura(df,casa,fora):
    fig, ax = plt.subplots(figsize=(3,3))
    fs = 6
    ls = 6

    df = df.sort_values('TAXA',ascending=True)
    lista = df.CLUBE.tolist()
    ncasa = lista.index(casa)
    nfora = lista.index(fora)

    cor = ["indigo"]*len(lista)
    cor[ncasa] = "lime"
    cor[nfora] = "lime"
    
    ax.barh(df.CLUBE,df.TAXA,height=0.6,color=cor,edgecolor="k",linewidth=0.3)
    
    ax.set_title(dropdown+' - '+gols+' - '+mando+'\n',fontsize=fs)
    ax.set_facecolor('ivory')

    ax.set_xlim([0, 100])
    ax.set_xlabel('Aproveitamento %\n')
    ax.grid(axis='x',color='k',alpha=0.3)
    ax.tick_params(axis='y', which='major', labelsize=ls)
    ax.tick_params(axis='x', which='both', labelsize=ls)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    plt.xticks(np.arange(0, 110, 10))

    with tab2:
        st.pyplot(fig)

ligas = ["Alemanha","Alemanha2",
        "Espanha","Espanha2",
        "França","França2",
        "Inglaterra","Inglaterra2",
        "Itália","Itália2",
        "Bélgica","Holanda",
        "Portugal","Turquia","Grécia",
        "Dinamarca","Noruega",
        "Suiça","Suécia",
        "Escócia","Brasil",]

liga = st.sidebar.selectbox('Escolha a liga', ligas)
st.sidebar.header("TEMPORADA / ANO")
ano = st.sidebar.selectbox('Temporada / Ano', ['2022/2023','2021/2022','2020/2021'])

limpa_e_calcula(liga,ano)
