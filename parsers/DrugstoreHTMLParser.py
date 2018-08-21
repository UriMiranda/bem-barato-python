from html.parser import HTMLParser
import re

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
            # else:
            #     self._items.append(self._item)
            matches =re.search(r"(?P<mcg>(\d+mcg|\d+mg))",data,flags=re.IGNORECASE)
            if matches:
                self._item = {'drugstore': self.get_drugstore(), 'name': data, 'mcg': matches.group('mcg'), 'values': list()}
            else:
                self._item = {'drugstore': self.get_drugstore(), 'name': data, 'mcg': 0, 'values': list()}
        elif value_pattern:
            if self._item != None:
                values = self._item['values']
                if len(values) < 1:
                    values.append(value_pattern.group('Price'))
                    self._items.append(self._item)
