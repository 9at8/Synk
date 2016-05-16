import os
import shutil


class Sync(object):
    def __init__(self):
        self.source = ['', '']
        self.destination = ''
        Sync.input_locations(self)

    def copy(self):
        if self.source[1] == 'file':
            print 'Copying', self.source, 'to', self.destination, '...'
            print 'Please be patient...\n'
            shutil.copy2(self.source[0], self.destination)
            print 'Mission Accomplished!'
        elif self.source[1] == 'directory':
            print 'Copying', self.source, 'to', self.destination, '...'
            print 'Please be patient...\n'
            try:
                shutil.copytree(self.source[0], self.destination)
            except OSError, e:
                if e.errno == 17:
                    print self.destination, 'already exists.'
                    print self.destination, 'will be emptied. Press enter to continue.'
                    x = raw_input()
                    shutil.rmtree(self.destination)
                    shutil.copytree(self.source[0], self.destination)
            print 'Mission Accomplished!'

    def input_locations(self):
        def _input_source_():
            src = raw_input('Enter location of source file/folder: ').rstrip('/')
            print src
            source = [src, 'directory']
            try:
                os.listdir(source[0])
                return source
            except OSError, e:
                if e.errno == 2:
                    print 'File/Folder doesn\'t exist. Try again.\n'
                    _input_source_()
                elif e.errno == 20:
                    source[1] = 'file'
                    return source

        def _input_destination_():
            destination = raw_input('Enter location of destination folder: ').rstrip('/')
            if self.source[1] == 'directory':
                return destination
            elif self.source[1] == 'file':
                try:
                    os.listdir(destination)
                    return destination
                except OSError, e:
                    if e.errno == 2 or e.errno == 20:
                        choice = raw_input('Destination folder doesn\'t exist.\n\
Do you want to create a new folder of the same name? (y/n) ')
                    if choice.lower() == 'y':
                        os.mkdir(destination)
                        return destination
                    elif choice.lower() == 'n':
                        print 'Try again. \n'
                        _input_destination_()

        self.source = _input_source_()
        self.destination = _input_destination_()
