import os
import shutil
import time


class Sync(object):
    def __init__(self):
        self.source = ''
        self.__source_type = ''
        self.destination = ''
        self.task = ''
        self.input_locations()

    def check_config(self):
        while True:
            try:
                config = open(self.source.rstrip('/') + '.psynk')
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

                while True:
                    print('Choose from the following options:')
                    try:
                        number = int(input(text))
                        if (number >= 1) and (number <= len(destinations)):
                            chosen = number - 1
                            break
                        else:
                            print('Invalid entry. Try again.\n')
                    except ValueError:
                        print('Invalid entry. Try again.\n')

                return destinations[chosen], tasks[chosen]

            elif choice.lower() == 'n':
                return False, False
            else:
                print('Invalid input. Try again.')

    def input_locations(self):
        def _input_source_():
            while True:
                src = input('Enter location of source file/folder: ').rstrip('/') + '/'
                source, source_type = src, 'directory'
                if os.path.exists(source):
                    if os.path.isdir(source):
                        return source, source_type
                    else:
                        source_type = 'file'
                        return source, source_type
                else:
                    print('File/Folder doesn\'t exist. Try again.\n')

        def _input_destination_():
            while True:
                destination = input('Enter location of destination folder: ').rstrip('/') + '/'
                if self.__source_type == 'directory' and destination:
                    return destination
                elif self.__source_type == 'file':
                    if os.path.isdir(destination):
                        return destination
                    else:
                        choice = input('Destination folder doesn\'t exist.\n\
                        Do you want to create a new folder of the same name? (y/n): ')
                        if choice.lower() == 'y':
                            os.mkdir(destination)
                            return destination
                        elif choice.lower() == 'n':
                            print('Try again.\n')

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
        config = open(self.source.rstrip('/') + '.psynk', 'a+')
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
        def merge(source, destination):
            def merge_choice(x):
                while True:
                    print(x, 'already exists in the destination as a file.')
                    choice = input('Do you want to overwrite it? (y/n): ')
                    if choice.lower() == 'y':
                        print('-----')
                        os.remove(x)
                        print(x, 'file successfully deleted.')
                        print('-----')
                        break
                    elif choice.lower() == 'n':
                        print('-----')
                        os.rename(x, x.rstrip('/') + '(1)')
                        print(x, 'renamed to', x.rstrip('/') + '(1)')
                        print('-----')
                        break
                    else:
                        print('Invalid entry. Try again.')

            for item in os.listdir(source):
                src = source + item
                dst = destination + item
                if os.path.isdir(src):
                    if os.path.isdir(dst):
                        merge(src, dst)
                    else:
                        if os.path.exists(dst):
                            merge_choice(dst)
                        shutil.copytree(src, dst)
                else:
                    if os.path.exists(dst):
                        merge_choice(dst)
                    shutil.copy2(src, dst)

        if self.__source_type == 'file':
            print('Copying', self.source, 'to', self.destination, '...\n')
            print('Please be patient...\n')
            shutil.copy2(self.source, self.destination)
            Sync.create_config(self, 'copy')
            print('Mission Accomplished!')
        elif self.__source_type == 'directory':
            print('Copying', self.source, 'to', self.destination, '...')
            try:
                shutil.copytree(self.source, self.destination)
            except FileExistsError:
                print(self.destination, 'already exists.')
                print('Do you want to:')
                text = '1. Merge the directories?\n2. Delete the destination directory?\n(1/2): '
                while True:
                    choice = input(text)
                    if choice == '1':
                        print('Please be patient...\nMerging directories...\n')
                        merge(self.source, self.destination)
                        break
                    elif choice == '2':
                        print(self.destination, 'will be emptied. Press enter to continue.')
                        input()
                        print('Please be patient...\n')
                        shutil.rmtree(self.destination)
                        shutil.copytree(self.source, self.destination)
                    else:
                        print('Invalid entry. Try again.\n')

            self.create_config('copy')
            print('Mission Accomplished!')

    def move(self):
        choice = input('Are you sure about moving file(s)? (y/n): ').lower()
        if choice == 'y':
            print('Moving', self.source, 'to', self.destination, '...\n')
            print('Please be patient...\n')
            shutil.move(self.source, self.destination)
            self.create_config('move')
            shutil.move(self.source.rstrip('/') + '.psynk', self.destination)
            print('Mission Accomplished!\n')
        elif choice == 'n':
            copy = 'y' == input('Do you want to copy files instead? (y/n): ').lower()
            if copy:
                Sync.copy(self)

#Yay
