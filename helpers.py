from os.path import join, dirname, abspath
from platform import platform
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances[cls]:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PathUtil(object, metaclass=Singleton):
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
        else:
            base_path = join(dirname(abspath(__file__)), '..')
        print("Loading Directory:", join(base_path, relative_path))
        return join(base_path, relative_path)

    @staticmethod
    def get_rdb_file_path():
        if platform().lower().startswith('win'):
            final_path = PathUtil.resource_path('dump.rdb')
            database_path = final_path
        else:
            final_path = PathUtil.resource_path('dump.rdb')
            database_path = final_path
        return database_path
