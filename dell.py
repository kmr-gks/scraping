from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import datetime
import socket
import os


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


# ターゲットのURL
urls = [
	"https://www.dell.com/ja-jp/shop/laptops/amd/spd/inspiron-14-7445-2-in-1-laptop/sic7445200201monojp",
	"https://www.dell.com/ja-jp/shop/laptops/intel/spd/inspiron-14-7440-2-in-1-laptop/sic7440100101monojp"]

# 前回の価格を格納するファイル名
file_name = "dell.txt"
# ログファイル
log_file = "log.txt"
price_data = ""

try:
	for url in urls:
		cpu_type = "AMD" if "amd" in url else "Intel"

		# SeleniumのWebDriverを設定
		options = webdriver.ChromeOptions()
		# options.add_argument('--headless')  # ヘッドレスモード（ブラウザを表示しない）
		driver = webdriver.Chrome(options=options)

		driver.get(url)

		# ページがロードされるまで待機
		wait = WebDriverWait(driver, 10)

		print("通常モデル")
		price_data += "通常モデル\n"

		# ページの内容を取得
		page_source = driver.page_source

		# BeautifulSoupを使用してHTMLを解析
		soup = BeautifulSoup(page_source, 'html.parser')

		# 商品名と価格を含む要素を検索
		item_name_element = soup.find("span", {"class": "page-title"})
		price_element = soup.find("span", {"class": "h3 font-weight-bold mb-1 text-nowrap sale-price"})

		# 商品名が見つかれば表示
		if item_name_element:
			item_name = item_name_element.get_text(strip=True)
			print(f"{item_name}({cpu_type})")
			price_data += f"{item_name}({cpu_type})\n"
		# 見つからない場合
		else:
			print("商品情報が見つかりませんでした。")
			price_data += "商品情報が見つかりませんでした。\n"

		# 価格が見つかれば表示
		if price_element:
			price = price_element.get_text(strip=True)
			print(f"価格: {price}")
			price_data += f"価格: {price}\n"
		# 見つからない場合
		else:
			print("価格情報が見つかりませんでした。")
			price_data += "価格情報が見つかりませんでした。\n"

		# 「即納モデルを表示」ボタンを探してクリック
		elem = driver.find_element(By.CLASS_NAME, 'toggle-label')
		# elem=driver.find_element(By.XPATH,'//label[@for="ready-to-ship"]')
		elem.click()

		# ページが更新されるまで待機
		time.sleep(5)  # 5秒待機（必要に応じて調整）

		print("即納モデル")
		price_data += "即納モデル\n"

		# ページの内容を取得
		page_source = driver.page_source

		# ブラウザを閉じる
		driver.quit()

		# BeautifulSoupを使用してHTMLを解析
		soup = BeautifulSoup(page_source, 'html.parser')

		# 商品名と価格を含む要素を検索
		item_name_element = soup.find("span", {"class": "page-title"})
		price_element = soup.find("span", {"class": "h3 font-weight-bold mb-1 text-nowrap sale-price"})

		# 商品名が見つかれば表示
		if item_name_element:
			item_name = item_name_element.get_text(strip=True)
			print(f"{item_name}({cpu_type})")
			price_data += f"{item_name}({cpu_type})\n"
		# 見つからない場合
		else:
			print("商品情報が見つかりませんでした。")
			price_data += "商品情報が見つかりませんでした。\n"

		# 価格が見つかれば表示
		if price_element:
			price = price_element.get_text(strip=True)
			print(f"価格: {price}")
			price_data += f"価格: {price}\n"
		# 見つからない場合
		else:
			print("価格情報が見つかりませんでした。")
			price_data += "価格情報が見つかりませんでした。\n"
	print(price_data)
	# 前回の価格と比較
	# ファイルが存在しない場合は作成する
	if not os.path.exists(file_name):
		with open(file_name, "w", encoding='utf-8') as f:
			f.write(' ')
	with open(file_name, "r", encoding='utf-8') as f:
		before_price_data = f.read()
	if before_price_data != price_data:
		send_message("価格が変更されました。" + price_data)
		with open(file_name, "w", encoding='utf-8') as f:
			f.write(price_data)

	# ログファイルに記録
	with open(log_file, 'a', encoding='utf-8') as f:
		f.write(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "\n" + price_data + "\n")

except Exception as e:
	print("エラーが発生しました。" + str(e))
	send_message("エラーが発生しました。" + str(e))
	exit()
