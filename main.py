import re
from urllib.request import urlopen


class Rooter:

    def __init__(self):
        self.URLS = {
            'bus_babka': "https://yandex.ru/maps/213/moscow/stops/stop__9641561/?ll=37.652162%2C55.871319&z=17.96",
            'tram': "https://yandex.ru/maps/213/moscow/stops/stop__9642452/?ll=37.652162%2C55.871319&z=17.96",
            'otradnoe': "https://yandex.ru/maps/213/moscow/stops/stop__9641574/?ll=37.652162%2C55.871319&z=17.96",
            'avt_649': 'https://yandex.ru/maps/213/moscow/stops/stop__9711575/?ll=37.652712%2C55.871607&z=18.22'
        }
        self.TIME_DELTAS = {
            'bus_babka': 5,
            'tram': 5,
            'otradnoe': 4,
            'avt_649': 3
        }

    def print_schedule(self, data):
        for line in data:
            if self.on_time(line):
                if {line[2]} == '17':
                    time = 4
                elif {line[2]} == '649':
                    time = 7
                elif {line[2]} in ['605', '880']:
                    time = 18
                else:
                    time = 4
                print(f'{line[2]} будет через {line[0]}, до метро - {line[0] + time}')

    def on_time(self, data):
        if data[0] - self.TIME_DELTAS[data[3]] >= 0:
            return True
        else:
            return False

    def schedule(self, key, good=False):
        url = self.URLS[key]
        html = urlopen(url)
        content = html.read().decode('utf-8')
        content = re.findall(r'<ul class=\"masstransit-brief-schedule-view__vehicles\">(.*?)</ul>', content)
        if content:
            content = content[0]
        roots = re.findall(r'<li class=\"masstransit-vehicle-snippet-view _clickable\">(.*?)</li>', content)
        result = []
        for root in roots:
            transp_type = re.findall(r'(Автобус|Трамвай)', root)
            transp_num = re.findall(r' (\d*?) в', root)
            time = re.findall(r'<span class=\"masstransit-prognoses-view__title-text\">(\d+? мин)</span>', root)
            if good:
                if transp_num and transp_num[0] not in good:
                    continue
            if time and transp_num and transp_type:
                result.append((int(time[0].split(' ')[0]), transp_type[0], transp_num[0], key))
        return result

    def metro(self):
        result = self.avt_649()
        result += self.tram()
        result += self.bus_babka()
        return sorted(result)

    def bus_babka(self):
        good_to_babka = ['124', '174', '238', '309', '880', '928', 'С15']
        return self.schedule(key="bus_babka", good=good_to_babka)

    def tram(self):
        return self.schedule(key='tram')

    def avt_649(self):
        return self.schedule(key='avt_649')

    def otradnoe(self):
        good_to_otradnoe = ['605', '880']
        return self.schedule(key="otradnoe", good=good_to_otradnoe)

    def altufan(self):
        good = ['928']
        return self.schedule(key="otradnoe", good=good)


if __name__ == '__main__':
    rooter = Rooter()
    data = rooter.metro()
    rooter.print_schedule(data)

