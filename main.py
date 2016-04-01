import os
import shutil


class Sync(object):
    def __init__(self):
        def input_source():
            src = raw_input('Enter location of source file/folder: ')
            source = [src, 'directory']
            try:
                os.listdir(source[0])
                return source
            except OSError, e:
                if e.errno == 2:
                    print 'File/Folder doesn\'t exist. Try again.\n'
                    input_source()
                elif e.errno == 20:
                    source[1] = 'file'
                    return source

        def input_destination():
            destination = raw_input('Enter location of \
                                    destination folder: ')
            try:
                os.listdir(destination)
                return destination
            except OSError, e:
                if e.errno == 2 or e.errno == 20:
                    choice = raw_input('Destination folder doesn\'t exist.\n\
                                        Do you want to create a new folder \
                                        of the same name? (y/n) ')
                    if choice.lower() == 'y':
                        os.mkdir(destination)
                        return destination
                    elif choice.lower() == 'n':
                        print 'Try again. \n'
                        input_destination()

        self.source = input_source()
        self.destination = input_destination()

    def copy(self):
        if self.source[1] == 'file':
            shutil.copy2(self.source[0], self.destination)
        elif self.source[1] == 'directory':
            temp = self.source[0]
            contents = os.listdir(self.source[0])
            for file_name in contents:
                print 'Copying', file_name, 'from', self.source
                self.source[0] = temp
                if self.source[0][-1] == '/':
                    self.source[0] += file_name
                elif self.source[0][-1] == '\\':
                    self.source[0] += file_name
                elif 'win' in os.uname()[0]:
                    self.source[0] += '\\' + file_name
                else:
                    self.source[0] += '/' + file_name
                Sync.copy(self)