# -*- coding: utf-8 -*-
"""ドットの数のカウント.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z1YJyWz34J_ISFtjNk2hN1PKBC2pSk9P
"""

pip install requests opencv-python-headless numpy beautifulsoup4

import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np

def get_image_url_from_page(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 画像のURLを抽出 (例では最初のimgタグのsrc属性を使用)
    img_tag = soup.find('img')
    if img_tag and 'src' in img_tag.attrs:
        img_url = img_tag['src']
        # img_urlが相対パスの場合、絶対URLに変換する
        if not img_url.startswith('http'):
            from urllib.parse import urljoin
            img_url = urljoin(page_url, img_url)
        return img_url
    return None

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # エラーがあれば例外を発生させる
    image_data = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return image

def count_dots(image):
    # 画像のサイズ取得
    height, width, _ = image.shape

    # 100x100ピクセルごとの分割
    grid_size = 100

    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            # グリッド内の領域を取得
            grid = image[y:y+grid_size, x:x+grid_size]

            # 青色と赤色のマスクを作成
            lower_blue = np.array([100, 0, 0])
            upper_blue = np.array([255, 150, 150])
            blue_mask = cv2.inRange(grid, lower_blue, upper_blue)

            lower_red = np.array([0, 0, 100])
            upper_red = np.array([150, 150, 255])
            red_mask = cv2.inRange(grid, lower_red, upper_red)

            # ドットの数をカウント
            blue_dots = cv2.countNonZero(blue_mask)
            red_dots = cv2.countNonZero(red_mask)

            # 結果を表示
            print(f"Grid ({x}, {y}) - Blue dots: {blue_dots}, Red dots: {red_dots}")

if __name__ == "__main__":
    page_url = 'https://example.com'  # ホームページのURLを指定
    image_url = get_image_url_from_page(page_url)
    if image_url:
        print(f"Image URL: {image_url}")
        image = download_image(image_url)
        count_dots(image)
    else:
        print("画像のURLが見つかりませんでした。")