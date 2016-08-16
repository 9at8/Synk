import os
import shutil
import time
import sys


class Sync(object):
    def __init__(self):
        self.source = ''
        self.__source_type = ''
        self.destination = ''
        self.task = ''
        self.input_locations()

    def check_config(self):
        try:
            config = open(self.source + '.psynk')
        except IOError:
            return False, False
        choice = input('Do you want to repeat a previous operation for the directory? ')
        if choice.lower() == 'y':
            destination = config.readline().strip('\n')
            task = config.readline().strip('\n')
            date = config.readline().strip('\n')
            destinations = []
            tasks = []
            dates = []
            destinations.append(destination)
            tasks.append(task)
            dates.append(date)
            while True:
                destination = config.readline().strip('\n')
                if destination:
                    task = config.readline().strip('\n')
                    date = config.readline().strip('\n')
                    destinations.append(destination)
                    tasks.append(task)
                    dates.append(date)
                else:
                    break
            config.close()
            text = ''
            for i in range(len(destinations)):
                text += str(i + 1) + '.\nDestination: ' + destinations[i]
                text += '\nTask: ' + tasks[i]
                text += '\nDate: ' + dates[i] + '\n\n'

            def choose():
                print('Choose from the following options:')
                try:
                    number = int(input(text))
                    if (number >= 1) and (number <= len(destinations)):
                        return number
                    else:
                        print('Invalid entry. Try again.\n')
                        choose()
                except ValueError:
                    print('Invalid entry. Try again.\n')
                    choose()

            chosen = choose() - 1
            return destinations[chosen], tasks[chosen]

        elif choice.lower() == 'n':
            return False, False
        else:
            print('Invalid input. Try again.')
            self.check_config()

    def input_locations(self):
        def _input_source_():
            src = input('Enter location of source file/folder: ').rstrip('/')
            source, source_type = src, 'directory'
            try:
                os.listdir(source)
                return source, source_type
            except FileNotFoundError:
                print('File/Folder doesn\'t exist. Try again.\n')
                _input_source_()
            except NotADirectoryError:
                source_type = 'file'
                return source, source_type
            except:
                print('Unexpected Error:', sys.exc_info()[0])
                raise

        def _input_destination_():
            destination = input('Enter location of destination folder: ').rstrip('/')
            if self.__source_type == 'directory':
                return destination
            elif self.__source_type == 'file':
                try:
                    os.listdir(destination)
                    return destination
                except (NotADirectoryError, FileNotFoundError):
                    choice = input('Destination folder doesn\'t exist.\n\
                                        Do you want to create a new folder of the same name? (y/n): ')
                    if choice.lower() == 'y':
                        os.mkdir(destination)
                        return destination
                    elif choice.lower() == 'n':
                        print('Try again.\n')
                        _input_destination_()
                except:
                    print('Unexpected Error:', sys.exc_info()[0])
                    raise

        self.source, self.__source_type = _input_source_()
        self.destination, self.task = self.check_config()
        if self.destination:
            if self.task == 'copy':
                self.copy()
            elif self.task == 'move':
                self.move()
        else:
            self.destination = _input_destination_()
            self.task = ''

    def create_config(self, task):
        config = open(self.source + '.psynk', 'a+')
        config.write(self.destination + '\n')
        config.write(task + '\n')
        present = time.localtime()
        year = str(present.tm_year)
        month = str(present.tm_mon)
        day = str(present.tm_mday)
        hours = str(present.tm_hour)
        minutes = str(present.tm_min)
        seconds = str(present.tm_sec)
        date = day + '/' + month + '/' + year + ' - ' + \
               hours + ':' + minutes + '::' + seconds
        config.write(date + '\n')
        config.close()

    def copy(self):
        if self.__source_type == 'file':
            print('Copying', self.source, 'to', self.destination, '...\n')
            print('Please be patient...\n')
            shutil.copy2(self.source, self.destination)
            Sync.create_config(self, 'copy')
            print('Mission Accomplished!')
        elif self.__source_type == 'directory':
            print('Copying', self.source, 'to', self.destination, '...')
            print('Please be patient...\n')
            try:
                shutil.copytree(self.source, self.destination)
            except FileExistsError:
                print(self.destination, 'already exists.')
                print(self.destination, 'will be emptied. Press enter to continue.')
                input()
                shutil.rmtree(self.destination)
                shutil.copytree(self.source, self.destination)
            self.create_config('copy')
            print('Mission Accomplished!')

    def move(self):
        choice = input('Are you sure about moving file(s)? (y/n): ').lower()
        if choice == 'y':
            print('Moving', self.source, 'to', self.destination, '...\n')
            print('Please be patient...\n')
            shutil.move(self.source, self.destination)
            self.create_config('move')
            print('Mission Accomplished!')
        elif choice == 'n':
            copy = 'y' == input('Do you want to copy files instead? (y/n): ').lower()
            if copy:
                Sync.copy(self)


s1 = Sync()
