import os
import io
from collections import Counter

class Tracker:
    def __init__(self, table='tracker', data_dir='./tracker', entry_size=4):
        self.ENTRY_SIZE = entry_size
        self.ROW_SIZE = self.ENTRY_SIZE * 2
        self.DATA_DIR = data_dir
        self.DAT_PATH = self.DATA_DIR + '/' + table + '.dat'
        
        os.makedirs(data_dir, exist_ok=True)
        if not os.path.exists(self.DAT_PATH):
            open(self.DAT_PATH, mode='ab').close()

        self.counter = Counter()
        self.read()

    def write(self):
        with open(self.DAT_PATH, mode='wb') as file:
            for i in self.counter:
                file.write(i.to_bytes(self.ENTRY_SIZE, byteorder='little'))
                file.write(self.counter[i].to_bytes(self.ENTRY_SIZE, byteorder='little'))

    def read(self):
        with open(self.DAT_PATH, mode='rb') as file:
            while True:
                chunk = file.read(self.ROW_SIZE)
                if not chunk:
                    break
                
                sid_b = chunk[0:self.ENTRY_SIZE]
                val_b = chunk[self.ENTRY_SIZE:self.ROW_SIZE]
                    
                sid = int.from_bytes(sid_b, byteorder='little')
                val = int.from_bytes(val_b, byteorder='little')

                self.counter[sid] = val

    def extract(self, out_file='dump.csv'):
        with open(self.DATA_DIR+'/'+out_file, mode='w') as file:
            for i in self.counter:
                file.write(str(i) + ',' + str(self.counter[i]) + '\n')
