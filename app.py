# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import widgets

import pandas as pd

import numpy as np
import requests
from datetime import timedelta
import datetime
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

def date_format_convertor(date):
    if len(date)==24:
        return datetime.fromisoformat(date[:-1])
    if len(date)==10:
        return datetime.strptime(date,'%Y-%m-%d')
    if len(date)==8:
        return datetime.strptime(date,'%Y%m%d')

def load_dataframe(sector):
    # api data load
    url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=1000&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d&tagSlugs={}'.format(sector)
    r = requests.get(url)
    data = r.json()

    sector_data = {'Sector':[],
                  'Name':[],
                  'Symbol':[],
                  'CoinMarketCap Rank':[],
                  'Market Cap':[],
                  'Circulating Supply':[],
                  'Total Supply':[],
                  'ATH':[],
                  'ATL':[],
                  'Price':[],
                  '24H High':[],
                  '24H Low':[],
                  'Percent Change 1h':[],
                  'Percent Change 24h':[],
                  'Percent Change 7d':[],
                  'Percent Change 30d':[],
                  'Percent Change 60d':[],
                  'Percent Change 90d':[],
                  'Percent Change YTD':[],
                  'Volume 24h':[],
                  'Volume 7d':[],
                  'Volume 30d':[],
                  'Last Updated':[]
                  }

    for x in data.get('data').get('cryptoCurrencyList'):
        if x.get('isActive')==0:
            continue
        sector_data['Sector'].append(sector)
        sector_data['Name'].append(x.get('name'))
        sector_data['Symbol'].append(x.get('symbol'))
        sector_data['CoinMarketCap Rank'].append(x.get('cmcRank'))
        sector_data['Circulating Supply'].append(x.get('circulatingSupply'))
        sector_data['Total Supply'].append(x.get('totalSupply'))
        sector_data['ATH'].append(x.get('ath'))
        sector_data['ATL'].append(x.get('atl'))
        sector_data['24H High'].append(x.get('high24h'))
        sector_data['24H Low'].append(x.get('low24h'))
        sector_data['Last Updated'].append(x.get('lastUpdated'))
        sector_data['Price'].append(x.get('quotes')[2]['price'])
        sector_data['Market Cap'].append(x.get('quotes')[2]['marketCap'])
        sector_data['Percent Change 1h'].append(x.get('quotes')[2]['percentChange1h'])
        sector_data['Percent Change 24h'].append(x.get('quotes')[2]['percentChange24h'])
        sector_data['Percent Change 7d'].append(x.get('quotes')[2]['percentChange7d'])
        sector_data['Percent Change 30d'].append(x.get('quotes')[2]['percentChange30d'])
        sector_data['Percent Change 60d'].append(x.get('quotes')[2]['percentChange60d'])
        sector_data['Percent Change 90d'].append(x.get('quotes')[2]['percentChange90d'])
        sector_data['Percent Change YTD'].append(x.get('quotes')[2]['ytdPriceChangePercentage'])
        sector_data['Volume 24h'].append(x.get('quotes')[2]['volume24h'])
        sector_data['Volume 7d'].append(x.get('quotes')[2]['volume7d'])
        sector_data['Volume 30d'].append(x.get('quotes')[2]['volume30d'])

    sector_df = pd.DataFrame(sector_data)
    sector_df['Last Updated'] = sector_df['Last Updated'].apply(lambda x: date_format_convertor(x)+timedelta(hours=9))
    sector_df['Log Scale Market Cap'] = np.log(1+sector_df['Market Cap'])

    return sector_df

sector_list = ['transport','options','retail','real-estate','derivatives','education','tourism','polychain-capital-portfolio',
                'cms-holdings-portfolio','trustswap-launchpad','binance-launchpad','galaxy-digital-portfolio','logistics',
                'interoperability','fantom-ecosystem','bounce-launchpad','avalanche-ecosystem','alameda-research-portfolio',
                'solana-ecosystem','scaling','dragonfly-capital-portfolio','parafi-capital','kinetic-capital','hashkey-capital-portfolio',
                'blockchain-capital-portfolio','duckstarter','vr-ar','coinbase-ventures-portfolio','three-arrows-capital-portfolio',
                'defiance-capital','decentralized-exchange','hacken-foundation','paradigm-xzy-screener','electric-capital-portfolio',
                'iot','privacy','framework-ventures','entertainment','collectibles-nfts','coinfund-portfolio','polkastarter',
                'smart-contracts','polygon-ecosystem','oracles','ledgerprime-portfolio','gaming','play-to-earn',
                'exnetwork-capital-portfolio','amm','insurance','e-commerce','rebase','eth-2-0-staking','fabric-ventures-portfolio',
                'defi-index','defi','ai-big-data','doggone-doggerel','media','huobi-capital','marketing','1confirmation-portfolio',
                'binance-labs-portfolio','social-money','analytics','a16z-portfolio','dcg-portfolio','sharing-economy',
                'boostvc-portfolio','petrock-capital','poolz-finance','masternodes','launchpad','wrapped-tokens','distributed-computing',
                'placeholder-ventures-portfolio','fenbushi-capital-portfolio','cosmos-ecosystem','dao','asset-management','heco-ecosystem',
                'fan-token','multicoin-capital-portfolio','dao-maker','yield-farming','seigniorage','health','yearn-partnerships',
                'polkadot-ecosystem','pantera-capital-portfolio','filesharing','binance-smart-chain','content-creation','synthetics',
                'sports','stablecoin','metaverse','yield-aggregator','storage','binance-launchpool','memes','centralized-exchange',
                'lending-borowing','music','hospitality','winklevoss-capital','aave-tokens','chromia-ecosystem','cybersecurity',
                'usv-portfolio','research','polkafoundry-red-kite','tokenized-stock','events','video','gambling',
                'communications-social-media','loyalty','identity','energy','jobs','genpad']

axis_list = ['Percent Change 1h', 'Percent Change 24h','Percent Change 7d', 'Percent Change 30d', 'Percent Change 60d','Percent Change 90d']
axis_dict = [
    {'label': '1시간 변화율', 'value' : 'Percent Change 1h'},
    {'label': '24시간 변화율', 'value' : 'Percent Change 24h'},
    {'label': '7일 변화율', 'value' : 'Percent Change 7d'},
    {'label': '30일 변화율', 'value' : 'Percent Change 30d'} ,
    {'label': '60일 변화율', 'value' : 'Percent Change 60d'},
    {'label': '90일 변화율', 'value' : 'Percent Change 90d'},
]

app.layout = html.Div([
    html.Div([
        html.H1(children='Crypto Social Sentiment Index'),

        html.H3(children='''
            테마별 주요 가상화폐 가격 변화량 차트
            '''),

        html.Div([
            html.Label('sector setting'),
            dcc.Dropdown(
                id='sector-column',
                options=[{'label': i, 'value': i} for i in sector_list],
                value='derivatives'
            )
            ], style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            html.Label('x축 setting'),
            dcc.Dropdown(
                id='xaxis-column',
                #options=[{'label': i, 'value': i} for i in axis_list],
                options=axis_dict,
                value='Percent Change 24h'
            ),
        ], style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

        html.Div([
            html.Label('y축 setting'),
            dcc.Dropdown(
                id='yaxis-column',
                options=axis_dict,
                value='Percent Change 7d'
            ),
        ], style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='indicator-graphic'),
    
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('sector-column', 'value'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))
def update_graph(sector, xaxis, yaxis):
    df = load_dataframe(sector)
    
    # Create figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=df[xaxis],y=df[yaxis], mode="markers+text",text=df['Symbol'],marker=dict(color="black")))
    fig.add_trace(go.Scatter(x=[df[xaxis].mean()],y=[df[yaxis].mean()],mode="markers+text",text=['평균'],marker=dict(color="red",symbol=18, size=12), name='평균'))

    fig.update_traces(textposition='top center')
    #fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    # Add figure title
    fig.update_layout(template='plotly_white')    
    # Set x-axis title
    fig.update_xaxes(title_text="<b>{}</b>".format(xaxis))
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>{}</b> ".format(yaxis))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
