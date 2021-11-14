import helpers
import json

class Redis:

    def __init__(self, db=0, data={}):
        self.db = db
        self.data = {self.db: data}

    def __exists(self, key):
        if key in self.data[self.db]:
            return True
        return False

    def dump_to_storage(self):
        """Dumps memory data to storage file"""
        try:
            with open(helpers.PathUtil.get_rdb_file_path(), 'w') as stream:
                json.dump(self.data, stream, indent=2)
                stream.close()
        except (Exception, IOError, OSError) as e:
            return False
        return True

    def load_to_memory(self):
        """Load dump.rdb data to memory"""
        try:
            with open(helpers.PathUtil.get_rdb_file_path(), 'r') as stream:
                data = json.load(stream)
                for key in data.__iter__():
                    data = data[key]
                self.data = {self.db: data}
                stream.close()
        except (Exception, IOError, OSError) as e:
            return False
        return True

    def getall(self):
        """Gets the values associated in memory"""
        data = self.data.get(self.db, {})
        return data

    def get(self, key):
        """Gets the value associated with a key"""
        data = self.data.get(self.db, {}).get(key)
        return data

    def set(self, key, value):
        """Sets a key-to-value association"""
        if self.__exists(key):
            self.data.get(self.db)[key] = value
        else:
            self.data.get(self.db).setdefault(key, value)
        return True

    def delete(self, key):
        """Deletes a key"""
        if self.__exists(key):
            del self.data[self.db][key]
            return True
        return False
