import urllib.parse
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Funktion för att kontrollera om SKU och pris redan finns i values.txt
def sku_price_exists(sku, price_text, filename):
    with open(filename, 'r') as f:
        for line in f:
            if sku in line and price_text in line:
                return True
    return False

# Funktion för att skriva SKU och pris till values.txt
def write_sku_price(sku, price_text, filename):
    # Öppna filen för läsning och skrivning
    with open(filename, 'r+') as f:
        # Läs in alla rader i filen
        lines = f.readlines()

        # Sök efter en befintlig post med samma SKU
        for i, line in enumerate(lines):
            if sku in line:
                # Om en match hittas, uppdatera priset för den befintliga posten
                lines[i] = f'{sku}\t{price_text}\n'
                break
        else:
            # Om ingen match hittas, lägg till en ny post för den nya SKU:en och priset
            lines.append(f'{sku}\t{price_text}\n')

        # Gå tillbaka till början av filen och skriv över alla rader med uppdaterade rader
        f.seek(0)
        f.writelines(lines)
        # Beskär eventuell överbliven text från tidigare version av filen
        f.truncate()

# Hitta sökvägen till skriptets katalog och filerna
script_dir = os.path.dirname(os.path.realpath(__file__))
pages_file = os.path.join(script_dir, 'pages.txt')
values_file = os.path.join(script_dir, 'values.txt')

# Läs in listan av sidor från filen pages.txt
with open(pages_file, 'r') as f:
    pages = [line.strip() for line in f]
    pages = [page.split('\t') for page in pages]


# Skapa instans av Chrome med Selenium-webdrivrutinerna
chrome_options = Options()
chrome_options.add_argument('--headless') # Kör utan grafiskt gränssnitt

# Iterera över listan och samla in pris från alla sidor
for address, sku, name in pages:
    # Undersök om adressen är en giltig URL
    parsed_url = urllib.parse.urlparse(address)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f'{address} is not a valid URL!')
        continue

    # Starta en webdriver och öppna en ny sida
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(address)

    # Hitta elementet som innehåller pris
    price_element = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'p.sc-iqsfdx.cuTrvl.sc-jUotMc.gQYeO'))
    )
    # hämta pristexten från elementet
    price_text = price_element.text.strip()

    # stäng webbläsaren
    driver.quit()

    # Skriv SKU och pris till values.txt om det inte redan finns
    if not sku_price_exists(sku, price_text, values_file):
        write_sku_price(sku, price_text, values_file)

    # Printa ut produkt och pris
    print(name)
    print(price_text)
