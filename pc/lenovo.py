import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import datetime
import socket

def send_message(message):
	line_token_file = "linetoken.txt"
	with open(line_token_file, 'r', encoding='utf-8') as f:
		line_token = f.read()
	line_notify_api = 'https://notify-api.line.me/api/notify'
	headers = {
		'Authorization': f'Bearer {line_token}'
	}
	data = {
		'message': socket.gethostname() + '\n' + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "\n" + message
	}
	requests.post(line_notify_api, headers=headers, data=data)

file_name = "ideapad-5-2-in-1-gen-9" + ".txt"
log_file = "log.txt"

url = "https://www.lenovo.com/jp/ja/p/laptops/ideapad/ideapad-5/lenovo-ideapad-5-2-in-1-gen-9-(14-inch-amd)/len101i0105"

# ファイルが存在しない場合は作成
if not os.path.exists(file_name):
	with open(file_name, 'w', encoding='utf-8') as f:
		f.write("empty file")
if not os.path.exists(log_file):
	with open(log_file, 'w', encoding='utf-8') as f:
		f.write("\n")

new_prices = ""

try:
	# ブラウザのオプションを格納する変数をもらってきます。
	options = Options()

	# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
	options.add_argument('--headless')

	# ブラウザを起動する
	driver = webdriver.Chrome(options=options)
	print("loading...")
	driver.implicitly_wait(5)
	driver.get(url)
	# 下までスクロールしないと全情報が取得できない

	req_text = driver.page_source

	# HTMLの解析
	bsObj = BeautifulSoup(req_text, "html.parser")

	# 要素の抽出
	new_found_name = None  # 最後に登場した商品名
	items = bsObj.find_all("span")
	for item in items:
		if 'class' in item.attrs:
			if 'lazy_href' in item['class'] and item.text.startswith("Lenovo"):
				new_found_name = item.text
			if 'final-price' in item['class']:
				if new_found_name != None:
					new_prices += new_found_name + " : " + item.text + "\n"
					new_found_name = None

except Exception as e:
	send_message("エラーが発生しました。" + str(e))
	with open(log_file, 'a', encoding='utf-8') as f:
		f.write(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "\n" + str(e) + "\n")
	exit()

# 前回の価格と比較
with open(file_name, 'r', encoding='utf-8') as f:
	old_prices = f.read()
if old_prices != new_prices:
	send_message("価格が変更されました。" + new_prices)
	with open(file_name, 'w', encoding='utf-8') as f:
		f.write(new_prices)
else:
	print("価格に変更はありません。")
with open(log_file, 'a', encoding='utf-8') as f:
	f.write(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "\n" + file_name + "\n" + new_prices + "\n")
