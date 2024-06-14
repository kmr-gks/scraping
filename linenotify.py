import requests
import datetime
import socket
import os

#LINEに通知を送る関数
def send_message(message):
	line_token_file = os.path.dirname(__file__)+"/linetoken.txt"
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
