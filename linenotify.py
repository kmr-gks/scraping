#LINEに通知を送るための関数を定義

import requests
import datetime
import socket

def send_message(message):
	line_token_file = "linetoken.txt"
	with open(line_token_file, 'r', encoding='utf-8') as f: 
		line_token = f.read()
	line_notify_api = 'https://notify-api.line.me/api/notify'
	headers ={
		'Authorization': f'Bearer {line_token}'
	}
	data = {
		'message': socket.gethostname()+'\n'+datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "\n" + message
	}
	requests.post(line_notify_api, headers = headers, data = data)

send_message("ああああ")