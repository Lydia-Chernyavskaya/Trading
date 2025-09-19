#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 16:45:32 2025

@author: lydiachernyavskaya
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from prettytable import PrettyTable
import datetime
from datetime import date
from datetime import datetime

print("\\\\\\\\\MONTE CARLO OPTION PRICE CALCULATOR////////////")


stocks = yf.download(["AAPL", "GOOG", "ORCL", "NVDA", "PLTR", "AVGO"], start="2015-09-11", end="2025-09-11")


ticker = yf.Ticker(str(input("Choose underlying asset from the following: AAPL, GOOG, ORCL, NVDA, PLTR, AVGO      ")))
info = ticker.info

print(f"Company name: {info["longName"]}")
c = info["currentPrice"]
print(f"Current price: {c}")

def volatility():
    data = ticker.history(period = "10y")
    daily_returns = data["Close"].pct_change()
    daily_returns = daily_returns.dropna()
    std_dev = daily_returns.std()
    annualized_vol = float(daily_returns.std()) * np.sqrt(252)
    return annualized_vol

vol = volatility()
print(f"Annualized volatility: {float(vol)* 100}")

    

#input variables
S = c

expiration = input(f"Choose expiration date from the following: {ticker.options}")
today = date.today()
exp = datetime.strptime(expiration, "%Y-%m-%d").date()
delta = exp - today
D = delta.days


T = D / 252


Ks = [float(c) - 50,float(c) - 40, float(c) - 30, float(c) - 20, float(c) - 10, float(c), float(c) + 10, float(c) + 20, float(c) + 30, float(c) + 40, float(c) + 50]
r = 0.04104
N = 100
M = 1000



def simulate_S():
    #precompute variables
    dt = T/N
    mudt = (r - (vol ** 2)/2) * dt
    vol_z = vol * np.sqrt(dt)
    lnS = np.log(S)
    
    
    #simulate matrix of price paths in N steps for M trials
    Z = np.random.normal(size = (N,M)) #create matrix with N rows M columns
    delta_lnSt = mudt + vol_z * Z #simulate changes in lnS for each random change in the matrix
    lnSt = lnS + np.cumsum(delta_lnSt, axis = 0) #add together all of the random changes to get final lnS
    lnSt = np.concatenate( (np.full(shape = (1,M), fill_value = lnS), lnSt)) #take the column of final lnSt prices
    
    ST = np.exp(lnSt)
    return ST
 
prices = simulate_S()    

def plot():
    plt.plot(prices)
    plt.xlabel = "time"
    plt.ylabel = "stock price"
    plt.title = "Stock price path simulation"



table = PrettyTable()
table.field_names = ["Strike", "Calls", "Puts"]

Cs = []
Ps = []    

def price_option():
    CT = np.maximum(0, (prices - K))
    PT = np.maximum(0, (K - prices))
    C0 = np.exp(-r * T) * np.sum(CT[- 1])/M
    P0 = np.exp(-r * T) * np.sum(PT[- 1])/M
    
    table.add_row([K, C0, P0])
    Cs.append(C0)
    Ps.append(P0)

    
    

for K in Ks:
    price_option()
    

print(table)

plt.plot(Ks, Cs)

plt.plot(Ks, Ps)





