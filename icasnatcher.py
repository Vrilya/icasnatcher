import sys
import asyncio
import urllib.parse
from pyppeteer import launch

# hjälpfunktion för att läsa adresser och namn från values.txt
def read_file(filename):
    with open(filename) as f:
        lines = f.read().split('\n')
        addresses = lines[::3]
        names = lines[1::3]
        products = lines[2::3]
        return list(zip(addresses, names, products))

# Hjälpfunktion för att undersköka om SKU samt priskombinationer redan finns i values.txt
def sku_price_exists(sku, price, filename):
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(sku) and line.endswith(price + '\n'):
                return True
    return False

# Hjällpfunktio för att skriva SKU och priskombination till values.txt
def write_sku_price(sku, price, filename):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        sku_found = False
        for i, line in enumerate(lines):
            if line.startswith(sku):
                lines[i] = sku + '\t' + price + '\n'
                sku_found = True
                break
        if not sku_found:
            lines.append(sku + '\t' + price + '\n')
        f.writelines(lines)



async def main():
    # Läs listan över adresser och namn från pages.txt
    pages = read_file('pages.txt')

    # Undersök om SKU finns specifierat som ett terminal-argument
    product_name = ''
    if len(sys.argv) > 1:
        product_name = sys.argv[1]

    # Iterera över listan och samla in pris från alla sidor
    for address, name, product in pages:
        # Undersök om SKU är specifierat och matcha det med det jag specifierat som terminalkommando
        if product_name and product.lower() != product_name.lower():
            continue

        # Undersök om adressen är en giltig URL
        parsed_url = urllib.parse.urlparse(address)
        if not parsed_url.scheme or not parsed_url.netloc:
            print(f'{address} is not a valid URL!')
            continue

        # Starta en huvudlös browser och öppna en ny sidda
        browser = await launch(headless=True)
        page = await browser.newPage()

        # Navigera till sida och vänta på att den ska laddas
        await page.goto(address)

        # Hitta elementet som innehåller pris
        price_element = await page.xpath("//p[contains(@class, 'sc-iqsfdx')]")
        if len(price_element) > 0:
            price = await price_element[0].getProperty('textContent')
            price_text = await price.jsonValue()

            # Skriv SKU och pris till values.txt om det inte redan finns
            sku = product.split()[0]
            if not sku_price_exists(sku, price_text, 'values.txt'):
                write_sku_price(sku, price_text, 'values.txt')

            # Printa ut produkt och pris och stäng ned browser
            print(name)
            print(price_text)
        await browser.close()

asyncio.get_event_loop().run_until_complete(main())
