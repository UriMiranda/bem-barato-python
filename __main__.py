#! /usr/bin/env python3

import urllib.request
import io, re, sys
from html.parser import HTMLParser
import time

class DrugstoreHTMLParser(HTMLParser):
    _items = None
    _name = ""
    _medicine = ""
    _item = None

    def set_medicine(self, medicine):
        self._medicine = medicine

    def get_medicine(self):
        return self._medicine

    def set_drugstore(self, name):
        self._name = name
    
    def get_drugstore(self):
        return self._name

    def get_items(self):
        return self._items

    def handle_data(self, data):
        name_pattern = re.compile("^"+self.get_medicine()+"((\s+?(\d+mcg|\d+mg))?\s+?(c\/|com)?\s+?(\d+)?\s+?(Comprimidos|cápsulas)?)?",flags=re.IGNORECASE)
        value_pattern = re.search(r"^((R\$)?\s+?)?(?P<Price>\d{1,3},\d{2})$",data, flags=re.IGNORECASE)
        if re.match(name_pattern, data):      
            if self._items is None:
                self._items = list()
            else:
                self._items.append(self._item)
            matches =re.search(r"(?P<mcg>(\d+mcg|\d+mg))",data,flags=re.IGNORECASE)
            if matches:
                self._item = {'drugstore': self.get_drugstore(), 'name': data, 'mcg': matches.group('mcg'), 'values': list()}
            else:
                self._item = {'drugstore': self.get_drugstore(), 'name': data, 'mcg': 0, 'values': list()}
        elif value_pattern:
            if self._item != None:
                values = self._item['values']
                values.append(value_pattern.group('Price'))
                # self._items.append(self._item)

def get_webpage(url, headers=None):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
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

parser.set_drugstore("Ultrafarma")
parser.feed(get_webpage("http://busca.ultrafarma.com.br/search#w="+medicine))

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

print("Farmacia; Nome; Preço")
for medicine in medicine_price_sorted:
    print("%s; %s; %7.2f"%(medicine['drugstore'],medicine['name'],medicine['price']))