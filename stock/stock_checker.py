import datetime
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('.')
from linenotify import send_message

#ターゲット
target = "GOOGL"
#通知する基準値
threshold = 170
#基準値よりも高いときに通知するか低いときに通知するか
high_or_low = "+"

data=yf.Ticker(target)
#通貨を取得
print(data.info['currency'])

#今日の日付を取得
data=yf.download(target, period='1d', interval='1m')
#最後の列の株価を取得
value=data.iloc[-1]['Close']

if high_or_low == "+":
	if value > threshold:
		send_message(f"{target}の株価が{threshold}を超えました。現在の株価は{value}です。")
elif high_or_low == "-":
	if value < threshold:
		send_message(f"{target}の株価が{threshold}を下回りました。現在の株価は{value}です。")
