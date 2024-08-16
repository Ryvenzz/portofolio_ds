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

# Hari ini
today = datetime.today()

# Tanggal 3 bulan yang lalu (dihitung sebagai 90 hari yang lalu)
three_months_ago = today - timedelta(days=90)

# Fungsi untuk menghasilkan tanggal acak dalam rentang yang ditentukan
def generate_random_date(start_date, end_date):
    # Menghitung selisih hari antara dua tanggal
    delta = end_date - start_date
    # Menghasilkan hari acak dalam rentang selisih hari
    random_days = random.randint(0, delta.days)
    # Menghasilkan tanggal acak
    random_date = start_date + timedelta(days=random_days)
    return random_date

url = input("Masukkan url toko : ")

if url :
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    z = 0
    data = []
    for i in range(0, 100):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs = {'class':'css-ccpe8t'})
        nama_toko = soup.find('h1', {'class': 'css-fzzhh3'}).text.strip()
        for container in containers:
            try:
                elements = container.find_all('a', {'class': 'styProduct'})
                # Memfilter nama produk dan varian berdasarkan konten teks
                nama_produk = None
                varian_produk = None
                for element in elements:
                    if "Varian:" not in element.text:
                        # varian_produk = element.text.strip()
                        nama_produk = element.text.strip()
                    else:
                        nama_produk = element.text.strip()
                # nama_produk = container.find('p', {'class': 'css-1ig3wia-unf-heading e1qvo2ff8'}).text.strip()
                reviewer = container.find('span', {'class': 'name'}).text.strip()
                review = container.find('span', attrs = {'data-testid':'lblItemUlasan'}).text
                bintang1 = container.find('div', {'class': 'css-1w6pe1p'}).find('div', {'class': 'rating'}).get('aria-label')
                bintang2 = int(bintang1.split()[1]) 
                tanggal1 = generate_random_date(three_months_ago, today)
                tanggal = "ditulis " + tanggal1.strftime("%Y-%m-%d")
                data.append({
                    'Toko' : nama_toko,
                    'Produk' : nama_produk,
                    'Nama Reviewer' : reviewer,
                    'Komentar' : review,
                    'Rating' : bintang2,
                    'Tanggal' : tanggal
                })
                
            except AttributeError:
                continue

        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
        time.sleep(3)
    
    driver.quit()
    def clean_filename(name):
    # Menghapus karakter yang tidak valid untuk nama file
        return re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned_nama_toko = clean_filename(nama_toko)
    file_name = f"{cleaned_nama_toko}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    