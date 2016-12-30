import json
import time
from os.path import expanduser


class Config(object):
    __CONFIG = expanduser('~') + '/.psynk.json'
    try:
        __JSONFILE = open(__CONFIG)
        __DATA = json.load(__JSONFILE)
        __JSONFILE.close()
    except FileNotFoundError:
        __DATA = {'objects': []}

    def __init__(self, src, dst):
        self.source = src
        self.destination = dst

    def __str__(self):
        return 'Source: ' + self.source + '\nDestination: ' + self.destination

    def __binsearch(self):
        lower = 0
        upper = len(Config.__DATA['objects']) - 1
        while lower <= upper:
            middle = (lower + upper) // 2
            if self.source == Config.__DATA['objects'][middle]['source']:
                if self.destination == Config.__DATA['objects'][middle]['destination']:
                    return middle
                elif self.destination < Config.__DATA['objects'][middle]['destination']:
                    upper = middle - 1
                else:
                    lower = middle + 1
            elif self.source < Config.__DATA['objects'][middle]['source']:
                upper = middle - 1
            else:
                lower = middle + 1
        else:
            return False

    @staticmethod
    def __date():
        present = time.localtime()
        year = str(present.tm_year)
        month = str(present.tm_mon)
        day = str(present.tm_mday)
        hours = str(present.tm_hour)
        minutes = str(present.tm_min)
        seconds = str(present.tm_sec)
        date = day + '/' + month + '/' + year + ' - ' + hours + ':' + minutes + '::' + seconds
        return date

    @staticmethod
    def __read_obj(obj):
        string = 'Source:' + obj['source'] + '\n'
        string += 'Destination:', obj['destination'] + '\n'
        string += 'Date:', obj['date']
        return string

    @staticmethod
    def __write():
        json_file = open(Config.__CONFIG, 'w')
        json.dump(Config.__DATA, json_file)
        json_file.close()

    def delete(self):
        position = self.__binsearch()
        if position:
            Config.__DATA.pop(position)
        Config.__write()

    @staticmethod
    def get_data():
        return Config.__DATA['objects']

    def insert(self):
        obj = {'source': self.source,
               'destination': self.destination,
               'date': Config.__date()}
        if not Config.__DATA['objects']:
            Config.__DATA['objects'] = [obj]
            Config.__write()
        else:
            position = 0
            # Identifies the position to insert
            for i in range(len(Config.__DATA['objects'])):
                if obj['source'] < Config.__DATA['objects'][i]['source']:
                    pass
                elif obj['source'] == Config.__DATA['objects'][i]['source']:
                    if obj['destination'] == Config.__DATA['objects'][i]['destination']:
                        Config.__DATA['objects'][i]['date'] = obj['date']
                        Config.__write()
                        return
                    elif obj['destination'] < Config.__DATA['objects'][i]['destination']:
                        position = i
                        break
                elif obj['source'] > Config.__DATA['objects'][i]['source']:
                    position = i
                    break
            Config.__DATA['objects'].append(None)
            new_obj = obj
            # Insert at 'position' and moves the rest
            for i in range(position + 1, len(Config.__DATA['objects'])):
                last_obj = Config.__DATA['objects'][i]
                Config.__DATA['objects'][i] = new_obj
                new_obj = last_obj
            Config.__write()

    @staticmethod
    def read():
        string = ''
        for i in range(len(Config.__DATA['objects'])):
            string += str(i + 1) + '\n'
            string += Config.__read_obj(Config.__DATA['objects'][i]) + '\n\n'
        return string

    @staticmethod
    def selector(i):
        try:
            data = Config.__DATA[i]
            return data
        except IndexError:
            return False
