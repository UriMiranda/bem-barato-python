#! /usr/bin/env python3

import urllib.request
import io, re, sys
import time
from optparse import OptionParser
from models.Medicine import Medicine
from datetime import datetime
from parsers.DrugstoreHTMLParser import DrugstoreHTMLParser

def get_webpage(url, headers=None):
    try: 
        if headers is None:
            req = urllib.request.Request(url, data=None)
        else:
            req = urllib.request.Request(url, data=None, headers=headers)
        res = urllib.request.urlopen(req)
        time.sleep(10)
        f = io.TextIOWrapper(res, encoding='utf-8')
        html = f.read()
        return html
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())

parser = DrugstoreHTMLParser()

argsParser = OptionParser()
argsParser.add_option("--mcg", dest="mcg", help="Adicione o filtro de mcg")

medicine = sys.argv[1]
parser.set_medicine(medicine)

headers = { 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "utf-8, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com.br/",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

parser.set_drugstore("Onofre")
parser.feed(get_webpage("https://www.onofre.com.br/search?Ntt="+medicine))

# Blocked
# print("Droga Raia")
parser.set_drugstore("Droga Raia")
parser.feed(get_webpage("https://busca.drogaraia.com.br/search?w="+medicine, headers))

# Blocked
parser.set_drugstore("Drogazil")
parser.feed(get_webpage("https://busca.drogasil.com.br/search?w="+medicine, headers))

parser.set_drugstore("Drogaria São Paulo")
parser.feed(get_webpage("https://www.drogariasaopaulo.com.br/"+medicine+"?"))

parser.set_drugstore("Pague Menos")
parser.feed(get_webpage("https://www.paguemenos.com.br/"+medicine))

# parser.set_drugstore("Ultrafarma")
# parser.feed(get_webpage("http://busca.ultrafarma.com.br/search#w="+medicine))

def map_cheap_price(item):
    values = item['values']
    if len(values) >= 1:
        price = values[len(values)-1].replace("R$","").replace(",",".").strip()
    else:
        price = 0.00
    item['price'] = float(price)
    return item

items = parser.get_items()

if  items == None:
    print("Remédio não encontrado")
    sys.exit(2)

medicines = filter(lambda i: i['price'] != 0.00,list(map(map_cheap_price, items)))


medicine_price_sorted = sorted(medicines, key=lambda medicine: medicine['price'])

# print("Farmacia; Nome; Preço")
for me in medicine_price_sorted:
    medicine = Medicine()
    medicine.name = me['name']
    medicine.drugstore = me['drugstore']
    medicine.mcg = me['mcg']
    medicine.price = me['price']
    medicine.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    medicine.save()
