import os
import io

NOT_FOUND = -1

class Tracker:
    def __init__(self, table='tracker', data_dir='./tracker', entry_size=8):
        self.ENTRY_SIZE = entry_size
        self.ROW_SIZE = self.ENTRY_SIZE * 2
        self.DATA_DIR = data_dir
        self.DAT_NAME = table + '.dat'
        self.DAT_PATH = self.DATA_DIR + '/' + self.DAT_NAME
        
        os.makedirs(self.DATA_DIR, exist_ok=True)
        if not os.path.exists(self.DAT_PATH):
            open(self.DAT_PATH, mode='ab').close()

        self.fhandle = open(self.DAT_PATH, mode='rb+')

    def set_row(self, row_num, stat_tuple): # stat_tuple in form (story_id, val)
        if (row_num * self.ROW_SIZE) >= os.path.getsize(self.DAT_PATH):
            return NOT_FOUND
        
        self.fhandle.seek(row_num * self.ROW_SIZE, io.SEEK_SET)
    
        self.fhandle.write(stat_tuple[0].to_bytes(self.ENTRY_SIZE, byteorder='little'))
        self.fhandle.write(stat_tuple[1].to_bytes(self.ENTRY_SIZE, byteorder='little'))

        self.fhandle.flush()
        return 0
    
    def get_row(self, row_num):
        if (row_num * self.ROW_SIZE) >= os.path.getsize(self.DAT_PATH):
            return (NOT_FOUND, 0)
        
        self.fhandle.seek(row_num * self.ROW_SIZE, io.SEEK_SET)
    
        story_id_b = self.fhandle.read(self.ENTRY_SIZE)
        val_b = self.fhandle.read(self.ENTRY_SIZE)
    
        story_id = int.from_bytes(story_id_b, byteorder='little')
        val = int.from_bytes(val_b, byteorder='little')

        self.fhandle.flush()
        return (story_id, val) # stat_tuple
    
    def new_row(self, stat_tuple):
        self.fhandle.seek(0, io.SEEK_END)
            
        self.fhandle.write(stat_tuple[0].to_bytes(self.ENTRY_SIZE, byteorder='little'))
        self.fhandle.write(stat_tuple[1].to_bytes(self.ENTRY_SIZE, byteorder='little'))
    
        self.fhandle.flush()
        return os.path.getsize(self.DAT_PATH) // self.ROW_SIZE # row num created
    
    def find_stat(self, story_id):
        self.fhandle.seek(0, io.SEEK_SET)
        row = 0
        while True:
            chunk = self.fhandle.read(self.ROW_SIZE)
            if not chunk:
                break
                
            sid_b = chunk[0:self.ENTRY_SIZE]
            sid = int.from_bytes(sid_b, byteorder='little')
    
            if sid == story_id:
                self.fhandle.flush()
                return row
                
            row += 1

        self.fhandle.flush()
        return NOT_FOUND
    
    def set_stat(self, story_id, val):
        row_at = self.find_stat(story_id)
        if val < 0:
            raise ValueError("unsigned value required")
        
        if row_at == NOT_FOUND:
            self.new_row((story_id, val))
        else:
            self.set_row(row_at, (story_id, val))
    
    
    def mod_stat(self, story_id, off):
        row_at = self.find_stat(story_id)    
        if row_at == NOT_FOUND:
            if off < 0:
                raise ValueError("unsigned value required")
            self.new_row((story_id, off))
        else:
            row = self.get_row(row_at)
            val = row[1] + off
            if val < 0:
                raise ValueError("unsigned value required")
            self.set_row(row_at, (story_id, val))

    def inc_stat(self, story_id):
        self.mod_stat(story_id, 1)
    
    def get_stat(self, story_id):
        row_at = self.find_stat(story_id)
        
        if row_at == NOT_FOUND:
            return 0
        else:
            return self.get_row(row_at)[1]

    def extract(self, out_file='dump.csv', threshold=0): # creates csv file containing data
        self.fhandle.seek(0, io.SEEK_SET)
        with open(self.DATA_DIR + '/' + out_file, mode='w') as dump:
            dump.write("Story ID,Number of Hits\n")
            while True:
                chunk = self.fhandle.read(self.ROW_SIZE)
                if not chunk:
                    break
                
                sid_b = chunk[0:self.ENTRY_SIZE]
                val_b = chunk[self.ENTRY_SIZE:self.ROW_SIZE]
                    
                sid = int.from_bytes(sid_b, byteorder='little')
                val = int.from_bytes(val_b, byteorder='little')

                if val > threshold:
                    dump.write(str(sid) + ',' + str(val) + '\n')
    
                    
                
        
