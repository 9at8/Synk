import os
import shutil
import platform
from config_handler import Config


class Sync(object):
    PLATFORM = platform.system()

    def __init__(self, source, destination):
        self.source = source

        if os.path.exists(source):
            self.__source_type = 'file'
            if os.path.isdir(source):
                self.__source_type = 'directory'
        else:
            self.__source_type = False

        self.destination = destination

    @staticmethod
    def __merge(source, destination):
        paths = os.listdir(source)
        for path in paths:
            src = source + path + '/'
            dst = destination + path + '/'
            if os.path.isdir(src):
                if os.path.isdir(dst):
                    Sync.__merge(src, dst)
                else:
                    if os.path.exists(dst):
                        os.rename(dst, dst.rstrip('/') + '.file')
                    shutil.copytree(src, dst)
            elif os.path.exists(dst.rstrip('/')):
                is_new = Sync.__is_new(src.rstrip('/'), dst.rstrip('/'))
                if is_new == 'Synced':
                    pass
                elif is_new:
                    shutil.copy2(src.rstrip('/'), dst.rstrip('/'))
                else:
                    shutil.copy2(dst.rstrip('/'), src.rstrip('/'))
            elif os.path.exists(src.rstrip('/')):
                shutil.copy2(src.rstrip('/'), dst.rstrip('/'))

    def __create_config(self):
        obj = Config(self.source, self.destination)
        obj.insert()

    @staticmethod
    def __is_new(source, destination):
        if Sync.PLATFORM == 'Windows':
            source_time = os.path.getmtime(source)
            destination_time = os.path.getmtime(destination)
        else:
            source_time = os.stat(source).st_mtime
            destination_time = os.stat(destination).st_mtime

        # Common to all platforms
        if source_time > destination_time:
            return True
        elif source_time == destination_time:
            return 'Synced'
        else:
            return False

    def copy(self):
        if self.__source_type == 'file':
            shutil.copy2(self.source, self.destination)
        elif self.__source_type:
            try:
                shutil.copytree(self.source, self.destination)
            except FileExistsError:
                Sync.__merge(self.source, self.destination)
        else:
            return False
        self.__create_config()
        return True
