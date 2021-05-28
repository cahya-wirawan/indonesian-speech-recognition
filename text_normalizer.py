import re
from num2words import num2words

class TextProcessor:
    thousands = ["ratus", "ribu", "juta", "miliar", "milyar", "triliun"]
    months = ["Januari", "Februari", "Maret", "April",
              "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]
    measurements_path = "measurements.tsv"
    currencies_path = "currency.tsv"
    timezones_path = "timezones.tsv"

    def __init__(self):
        self.measurements = {}
        with open(TextProcessor.measurements_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.measurements[line[0]] = line[1]

        self.currencies = {}
        with open(TextProcessor.currencies_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.currencies[line[0]] = line[1]

        self.timezones = {}
        with open(TextProcessor.timezones_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.timezones[line[0]] = line[1]

        self.re_thousands = '|'.join([t for t in TextProcessor.thousands])
        self.re_currencies = '|'.join([c for c in self.currencies]).replace('$', '\\$')
        self.re_moneys = r'(({}) ?([\d\.\,]+) (({})?(an)?))'.format(self.re_currencies, self.re_thousands)
        self.re_measurements = '|'.join([t for t in self.measurements])
        self.re_measurements = r'(([\d\.\,]+) ?({}) )'.format(self.re_measurements)
        self.re_timezones = '|'.join([c for c in self.timezones])
        self.re_timezones = r'((\d{1,2})[\.:](\d{1,2}) ' + '({}))'.format(self.re_timezones)
        print(self.re_measurements)
        print(self.re_timezones)

    def normalize(self, text):
        found_errors = False
        # Currency
        moneys = re.findall(self.re_moneys, text)
        for money in moneys:
            number = re.sub(',', '.', re.sub(r'\.', '', money[2].strip(" ,.")))
            try:
                if number == "":
                    continue
                if re.search(r'\.', number):
                    number = float(number)
                else:
                    number = int(number)
                number = num2words(number, to='cardinal', lang='id')
                text = text.replace(money[0].strip(" ,."), f'{number} {money[3]} {self.currencies[money[1]]}')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with money: <{text}>: {number}')

        # Measurements
        units = re.findall(self.re_measurements, text)
        for unit in units:
            number = re.sub(',', '.', re.sub(r'\.', '', unit[1].strip(" ,.")))
            try:
                if number == "":
                    continue
                if re.search(r'\.', number):
                    number = float(number)
                else:
                    number = int(number)
                number = num2words(number, to='cardinal', lang='id')
                text = text.replace(unit[0].strip(" ,."), f'{number} {self.measurements[unit[2]]}')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with measurements: <{text}>: {number}')

        # Date
        dates = re.findall(r'(\((\d{1,2})/(\d{1,2})(/(\d+))?\))', text)
        for date in dates:
            try:
                day = num2words(int(date[1]), to='cardinal', lang='id')
                month = self.months[int(date[2]) - 1]
                if date[4] != "":
                    year = num2words(int(date[4]), to='cardinal', lang='id')
                    date_string = f'{day} {month} {year}'
                else:
                    date_string = f'{day} {month}'
                text = text.replace(date[0], f' {date_string} ')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with dates: <{text}>: {date}')

        # Timezones
        timezones = re.findall(self.re_timezones, text)
        for timezone in timezones:
            try:
                hour = num2words(int(timezone[1]), to='cardinal', lang='id')
                minute = num2words(int(timezone[2]), to='cardinal', lang='id')
                zone = self.timezones[timezone[3]]
                if minute == "nol":
                    time_string = f'{hour} {zone}'
                else:
                    time_string = f'{hour} lewat {minute} menit {zone}'
                text = text.replace(timezone[0], f'{time_string}')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with timezones: <{text}>: {timezone}')

        # Number
        numerics = re.findall(r'([\d.,]+)', text)
        for numeric in numerics:
            number = re.sub(',', '.', re.sub(r'\.', '', numeric.strip(" ,.")))
            if number == "":
                continue
            try:
                if re.search(r'\.', number):
                    number = float(number)
                else:
                    number = int(number)
                number = num2words(number, to='cardinal', lang='id')
                text = text.replace(numeric.strip(" ,."), f' {number} ')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with number: <{text}>: {number}')

        # Any number
        numerics = re.findall(r'(\d+)', text)
        for numeric in numerics:
            number = numeric
            try:
                number = num2words(int(number), to='cardinal', lang='id')
                text = text.replace(numeric, f'{number}')
            except Exception as error:
                found_errors = True
                print(error)
                print(f'Problem with number: <{text}>: {number}')

        text = text.replace("  ", " ")
        if found_errors:
            print(text)
        return text

tp = TextProcessor()
texts = [
    "\"Untuk kesiapsiagaan, 16.180.234 untuk literasi jam 13.40 WIT, sedangkan nomor 1,2,3,4 dan 5 untuk edukasi jam 12:05 WIT, dari sisi itu,\" kata Hary kepada CNNIndonesia.com, Jumat (2/3)",
    "Lenovo 13,,4 Chromebook 100. 200e b 50 78.5 senin (12/2/2011) dibanderol. (20/10) 205 kg 5,6 cm seharga US$219,50 €20,50 ¥ 30,5 (Rp 6,5 juta) £ 100,50. 320 sementara model 33 dihargai sekitar $279 (Rp3,8 miliaran) sekitar pukul 06.00 WIB"
]
for text in texts:
    print(tp.normalize(text))
