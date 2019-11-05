'''
Created on Sep 8, 2019

@author: rich
'''

import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

class Plotter(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def showPlot(df):
        
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])])
        # show volume too

        fig.show()

    @staticmethod
    def showOHLCPlot(df):
        
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])])
        # show volume too

        fig.show()
        
    @staticmethod
    def showSinglePlot(df):
        
        fig = go.Figure(data=[go.Scatter(x=df.index,
                        y=df['open'],
                        mode='lines+markers',
                        marker_color=df['target'],
                        marker_colorscale=[[0, 'blue'], [0.5, 'green'], [1, 'red']]
                        )])
        # show volume too

        fig.show()

        
    