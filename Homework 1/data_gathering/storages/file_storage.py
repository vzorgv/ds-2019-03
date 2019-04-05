import os

from storages.storage import Storage


class FileStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        if not os.path.exists(self.file_name):
            raise StopIteration

        with open(self.file_name, encoding='UTF-8') as f:
            data = f.read().strip()

        return data

    def write_data(self, data_array):
        """
        :param data_array: collection of strings that
        should be written as lines
        """
        with open(self.file_name, 'w', encoding='UTF-8') as f:
            f.write(data_array)

    def append_data(self, data):
        """
        :param data: string
        """
        with open(self.file_name, 'a', encoding='UTF-8') as f:
            f.write(data + '\n')
