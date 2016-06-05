import os
import shutil
import time


class Sync(object):
    def __init__(self):
        self.source = ''
        self.__source_type = ''
        self.destination = ''
        self.__config = ''
        Sync.input_locations(self)

    def input_locations(self):
        def _input_source_():
            src = raw_input('Enter location of source file/folder: ').rstrip('/')
            print src
            source, source_type = src, 'directory'
            try:
                os.listdir(source)
                return source, source_type
            except OSError, e:
                if e.errno == 2:
                    print 'File/Folder doesn\'t exist. Try again.\n'
                    _input_source_()
                elif e.errno == 20:
                    source_type = 'file'
                    return source, source_type
                else:
                    print 'There is some error.'
                    print e.message

        def _input_destination_():
            destination = raw_input('Enter location of destination folder: ').rstrip('/')
            if self.__source_type == 'directory':
                return destination
            elif self.__source_type == 'file':
                try:
                    os.listdir(destination)
                    return destination
                except OSError, e:
                    if e.errno == 2 or e.errno == 20:
                        choice = raw_input('''Destination folder doesn't exist.
Do you want to create a new folder of the same name? (y/n): ''')
                        if choice.lower() == 'y':
                            os.mkdir(destination)
                            return destination
                        elif choice.lower() == 'n':
                            print 'Try again.\n'
                            _input_destination_()
                    else:
                        print 'There is some kind of an error.'
                        print e.message

        self.source, self.__source_type = _input_source_()
        self.destination = _input_destination_()

    def create_config(self, task):
        self.__config = open(self.source + '.psynk', 'a+')
        self.__config.write(self.destination + '\n')
        self.__config.write(task + '\n')
        present = time.localtime()
        year = str(present.tm_year)
        month = str(present.tm_mon)
        day = str(present.tm_mday)
        hours = str(present.tm_hour)
        minutes = str(present.tm_min)
        seconds = str(present.tm_sec)
        date = hours + ':' + minutes + '::' + seconds + ' - ' + \
               day + '/' + month + '/' + year
        self.__config.write(date + '\n\n')
        self.__config.close()

    def copy(self):
        if self.__source_type == 'file':
            print 'Copying', self.source, 'to', self.destination, '...'
            print 'Please be patient...\n'
            shutil.copy2(self.source, self.destination)
            Sync.create_config(self, 'copy')
            print 'Mission Accomplished!'
        elif self.__source_type == 'directory':
            print 'Copying', self.source, 'to', self.destination, '...'
            print 'Please be patient...\n'
            try:
                shutil.copytree(self.source, self.destination)
            except OSError, e:
                if e.errno == 17:
                    print self.destination, 'already exists.'
                    print self.destination, 'will be emptied. Press enter to continue.'
                    raw_input()
                    shutil.rmtree(self.destination)
                    shutil.copytree(self.source, self.destination)
            Sync.create_config(self, 'copy')
            print 'Mission Accomplished!'

    def move(self):
        choice = raw_input('Are you sure about moving file(s)? (y/n): ').lower()
        if choice == 'y':
            shutil.move(self.source, self.destination)
            Sync.create_config(self, 'copy')
            print 'Mission Accomplished!'
        elif choice == 'n':
            copy = 'y' == raw_input('Do you want to copy files instead? (y/n): ').lower()
            if copy:
                Sync.copy(self)
