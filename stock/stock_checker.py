import datetime
import pandas as pd
import numpy as np
import yfinance as yf
import sys
import os
sys.path.append(os.path.dirname(__file__)+'/..')
from linenotify import send_message

os.chdir(os.path.dirname(__file__))
message=""
log_file="log.txt"
log_str=""

#target,threshold,high_or_lowをcsvファイルから読み込む
df = pd.read_csv('tickers.csv')
for i in range(len(df)):
	#会社名
	name=df.iloc[i]['name']
	#ターゲット
	target = df.iloc[i]['target']
	#通知する基準値
	threshold = df.iloc[i]['threshold']
	#基準値よりも高いときに通知するか低いときに通知するか
	high_or_low = df.iloc[i]['high_or_low']

	#株価を取得
	data=yf.download(target, period='1d', interval='1m')
	currency=yf.Ticker(target).info['currency']

	#最後の列の株価を取得
	value=data.iloc[-1]['Close']
	stock_time=data.index[-1].strftime('%Y/%m/%d %H:%M:%S')

	#通知するか判定
	if high_or_low == "+":
		if value > threshold:
			message+=f"{name}の株価が{threshold}を超えました。現在の株価は{value:.4g}{currency}です。\n"
	elif high_or_low == "-":
		if value < threshold:
			message+=f"{name}の株価が{threshold}を下回りました。現在の株価は{value:.4g}{currency}です。\n"

	print(stock_time,name,value,currency)
	log_str+=f"{stock_time},{name},{value},{currency}\n"

if message != "":
	message=stock_time+"\n"+message
	print(message)
	send_message(message)
	log_str+=message

# ファイルが存在しない場合は作成
if not os.path.exists(log_file):
	with open(log_file, 'w', encoding='utf-8') as f:
		f.write("\n")

#ログを書き込む
with open(log_file, 'a', encoding='utf-8') as f:
	f.write(log_str)