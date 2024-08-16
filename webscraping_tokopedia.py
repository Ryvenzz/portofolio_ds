from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random
from datetime import datetime, timedelta
import re

url = input("Masukkan url toko : ")

if url :
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data = []
    for i in range(0, 100):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs = {'class':'css-ccpe8t'})
        nama_toko = soup.find('h1', {'class': 'css-fzzhh3'}).text.strip()
        for container in containers:
            try:
                elements = container.find_all('a', {'class': 'styProduct'})
                nama_produk = None
                varian_produk = None
                for element in elements:
                    if "Varian:" not in element.text:
                        nama_produk = element.text.strip()
                    else:
                        nama_produk = element.text.strip()
                reviewer = container.find('span', {'class': 'name'}).text.strip()
                review = container.find('span', attrs = {'data-testid':'lblItemUlasan'}).text
                bintang1 = container.find('div', {'class': 'css-1w6pe1p'}).find('div', {'class': 'rating'}).get('aria-label')
                bintang2 = int(bintang1.split()[1]) 
                data.append({
                    'Toko' : nama_toko,
                    'Produk' : nama_produk,
                    'Nama Reviewer' : reviewer,
                    'Komentar' : review,
                    'Rating' : bintang2
                })
                
            except AttributeError:
                continue

        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
        time.sleep(3)
    
    driver.quit()
    def clean_filename(name):
        return re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned_nama_toko = clean_filename(nama_toko)
    file_name = f"{cleaned_nama_toko}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    
