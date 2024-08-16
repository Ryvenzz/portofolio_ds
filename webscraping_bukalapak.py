import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

url = input("Masukkan url toko : ")
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)

data = []
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nama_produk = soup.find('h1', {'class': 'c-main-product__title u-txt--large'}).text.strip()
    nama_toko = soup.find('a', {'class': 'c-link--primary--black'}).text.strip()
    for item in soup.findAll('div', {'class': 'c-reviews-item'}):
        user_div = item.find('div', {'class': 'c-reviews-item__user'})
        if user_div:
            user_link = user_div.find('a', {'data-testid': 'reviewer-name'})
            if user_link:
                nama = user_link.text.strip()
            else:
                nama = user_div.find('span', {'data-testid': 'reviewer-name'}).text.strip()
        else:
            nama = "Nama tidak ditemukan"
        print(nama)
        # nama = item.find('div', {'class': 'c-reviews-item__user'}).find('a',{'data-testid': 'reviewer-name'}).text.strip()
        komen1 = item.find('div', {'class': 'c-reviews-item__head-content'}).find('h4', {'class': 'c-reviews-item__title u-mrgn-top--1'}).text.strip()
        komen2 = item.find('p', {'data-testid': 'content'})
        if komen2:
            komen2_kiw = komen2.text.strip()
        else:
            komen2_kiw = ''
        komentar = komen1 + ' ' + komen2_kiw
        tanggal = item.find('div', {'class': 'c-reviews-item__head-content'}).find('p', {'class': 'c-reviews-item__date u-fg--ash'}).text.strip()
        
        rating_style = item.find('div', {'class': 'c-rating'}).find('div', {'class': 'c-rating__fg c-rating__fg--default'}).get('style')
        width_percent = float(rating_style.split('width: ')[1].replace('%;', ''))
        rating = round(width_percent / 20)


        data.append({
            'Toko': nama_toko,
            'Produk': nama_produk,
            'Nama Reviewer': nama,
            'Komentar': komentar,
            'Rating': rating,
            'Tanggal': tanggal
        })

    try:
        # Wait until the "Next" button is clickable and click it
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.c-pagination__item > a.c-pagination__btn > span.c-icon--arrow-forward'))
        )
        next_button.click()
        time.sleep(3)  # Wait for the next page to load
    except Exception as e:
        print("Tidak ada tombol Next atau tidak dapat diklik:", e)
        break


driver.quit()

def clean_filename(name):
    # Menghapus karakter yang tidak valid untuk nama file
        return re.sub(r'[\\/*?:"<>|]', "", name)
cleaned_nama_toko = clean_filename(nama_toko)
file_name = f"{cleaned_nama_toko}.xlsx"
df = pd.DataFrame(data)
df.to_excel(file_name, index=False)


