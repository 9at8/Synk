import os.path
from main import Sync
from config_handler import Config


def validate_paths():
    while True:
        source = input('Enter path of source file/folder: ').rstrip('/') + '/'
        if os.path.exists(source):
            source_type = 'file'
            if os.path.isdir(source):
                source_type = 'directory'
            break
        else:
            print('File/Folder doesn\'t exist. Try again.\n')

    while True:
        destination = input('Enter location of destination folder: ').rstrip('/') + '/'
        if source_type == 'directory' and destination:
            try:
                if os.path.exists(destination):
                    break
                os.mkdir(destination)
                os.rmdir(destination)
                break
            except FileNotFoundError as e:
                print('Error:', e)
        elif destination:
            if not os.path.isdir(destination):
                try:
                    os.mkdir(destination)
                except FileNotFoundError as e:
                    print('Error:', e)
            break
        else:
            print('Enter something please!\n')
    return source, destination


def tasker(operation, everything=False):
    operating = None
    if operation == 'Sync':
        operating = 'Syncing'
    elif operation == 'Delete':
        operating = 'Deleting'
    pairs = Config.get_data()
    counter = 0
    for i in range(len(pairs)):
        source = pairs[i]['source']
        destination = pairs[i]['destination']
        choice = ''
        while not everything:
            choice = input('\n' + operation + '\n' + source + '\nto\n' + destination + '? (y/n): ').lower()
            if choice == 'y' or choice == 'n':
                print()
                break
        if everything or choice == 'y':
            print('\n' + operating + '\n' + source + '\nto\n' + destination + '\n')
            if operation == 'Sync':
                this = Sync(source, destination)
                try:
                    result = this.copy()
                    if not result:
                        print('Could not Sync paths. Source does not exist anymore.')
                        while True:
                            choice = input('Delete ' + source + '? (y/n): ').lower()
                            if choice == 'y':
                                print()
                                old = Config(source, destination)
                                old.delete()
                                break
                        continue
                except PermissionError:
                    print('Could not Sync paths. Permission Denied.')
                    continue
            elif operation == 'Delete':
                this = Config(source, destination)
                this.delete()
            counter += 1

    if everything:
        return len(pairs)
    else:
        return counter


def __main__():
    print('\n\nPsynk\n-----')
    print('(P)Syn(k)chronizes local files and directories\n')
    while True:
        input('Press enter to continue...\n')
        try:
            choice = int(input('1) Add a path to previous config.\n' +
                               '2) Sync all saved objects in existing config.\n' +
                               '3) Sync specific objects in existing config.\n' +
                               '4) Delete existing config.\n' +
                               '5) Delete specific objects in existing config.\n' +
                               '6) Quit!\n\nEnter Choice: '))
        except ValueError:
            print('Invalid input! Try again!\n\n')
            continue
        if not 1 <= choice <= 6:
            print('Invalid input! Try again!\n\n')
            continue

        if choice == 6:
            print('Bye!\n\n')
            break
        elif choice == 1:
            source, destination = validate_paths()
            this = Config(source, destination)
            this.insert()
        elif choice == 2:
            number = tasker('Sync', everything=True)
            print('Successfully synced ' + str(number) + ' paths!\n\n')
        elif choice == 3:
            number = tasker('Sync', everything=False)
            print('Successfully synced ' + str(number) + ' paths!\n\n')
        elif choice == 4:
            number = tasker('Delete', everything=True)
            print('Successfully removed ' + str(number) + ' paths from config!\n\n')
        elif choice == 5:
            number = tasker('Delete', everything=False)
            print('Successfully removed ' + str(number) + ' paths from config!\n\n')


if __name__ == '__main__':
    __main__()
