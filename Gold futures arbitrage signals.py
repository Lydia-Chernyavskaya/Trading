#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 21:22:22 2025

@author: lydiachernyavskaya
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import date

data = yf.download(["XAUS.L","GCU25.CMX"], start = "2025-01-01", end = "2025-09-19")
future = yf.Ticker("GCU25.CMX")
spot = yf.Ticker("XAUS.L")

f_history = future.history(period = "1mo")
s_history = spot.history(period = "1mo")


plt.plot(f_history["Close"])
plt.plot(s_history["Close"])
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()


s = spot.info["regularMarketPrice"]
f = future.info["regularMarketPrice"]

print(f"Spot price = {s}.")
print(f"Future price = {f}.")

def trade_signal():
    if f > s:
        print("Market is in contango")
        print(f"Buy {spot.info["longName"]}, sell {future.info["longName"]}")
    elif s > f:
        print("Market is in backwardation")
        print(f"Buy {future.info["longName"]}, sell {spot.info["longName"]}")
    else:
        print("No trade opportunity")
        
    
trade_signal()

