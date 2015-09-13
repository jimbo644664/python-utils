import os
import io

NOT_FOUND = -1

class Tracker:
    def __init__(self, table='tracker', data_dir='./tracker', entry_size=8):
        self.ENTRY_SIZE = entry_size
        self.ROW_SIZE = self.ENTRY_SIZE * 2
        self.DATA_DIR = data_dir
        self.DAT_NAME = table + '.dat'
        
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.chdir(self.DATA_DIR)
        
        if not os.path.exists(self.DAT_NAME):
            open(self.DAT_NAME, mode='ab').close

    def set_row(self, row_num, stat_tuple): # stat_tuple in form (story_id, val)
        if (row_num * self.ROW_SIZE) >= os.path.getsize(self.DAT_NAME):
            return NOT_FOUND
        
        with open(self.DAT_NAME, mode='rb+') as file:
            file.seek(row_num * self.ROW_SIZE, io.SEEK_SET)
    
            file.write(stat_tuple[0].to_bytes(self.ENTRY_SIZE, byteorder='little'))
            file.write(stat_tuple[1].to_bytes(self.ENTRY_SIZE, byteorder='little'))
            return 0
    
    def get_row(self, row_num):
        if (row_num * self.ROW_SIZE) >= os.path.getsize(self.DAT_NAME):
            return (NOT_FOUND, 0)
        
        with open(self.DAT_NAME, mode='rb') as file:
            file.seek(row_num * self.ROW_SIZE, io.SEEK_SET)
    
            story_id_b = file.read(self.ENTRY_SIZE)
            val_b = file.read(self.ENTRY_SIZE)
    
            story_id = int.from_bytes(story_id_b, byteorder='little')
            val = int.from_bytes(val_b, byteorder='little')
            return (story_id, val) # stat_tuple
    
    def new_row(self, stat_tuple):
        with open(self.DAT_NAME, mode='rb+') as file:
            file.seek(0, io.SEEK_END)
            
            file.write(stat_tuple[0].to_bytes(self.ENTRY_SIZE, byteorder='little'))
            file.write(stat_tuple[1].to_bytes(self.ENTRY_SIZE, byteorder='little'))
    
            return os.path.getsize(self.DAT_NAME) // self.ROW_SIZE # row num created
    
    def find_story(self, story_id):
        with open(self.DAT_NAME, mode='rb') as file:
            row = 0
            while True:
                chunk = file.read(self.ROW_SIZE)
                if not chunk:
                    break
                
                sid_b = chunk[0:self.ENTRY_SIZE]
                sid = int.from_bytes(sid_b, byteorder='little')
    
                if sid == story_id:
                    return row
                
                row += 1
    
            return NOT_FOUND
    
    def set_stat(self, story_id, val):
        row_at = self.find_story(story_id)
        if val < 0:
            raise ValueError("unsigned value required")
        
        if row_at == NOT_FOUND:
            self.new_row((story_id, val))
        else:
            self.set_row(row_at, (story_id, val))
    
    
    def mod_stat(self, story_id, off):
        row_at = self.find_story(story_id)    
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
        row_at = self.find_story(story_id)
        
        if row_at == NOT_FOUND:
            return 0
        else:
            return self.get_row(row_at)[1]

    def extract(self, out_file='dump.csv', threshold=0): # creates csv file containing data
        with open(self.DAT_NAME, mode='rb') as file:
            with open(out_file, mode='w') as dump:
                dump.write("Story ID,Number of Hits\n")
                while True:
                    chunk = file.read(self.ROW_SIZE)
                    if not chunk:
                        break
                
                    sid_b = chunk[0:self.ENTRY_SIZE]
                    val_b = chunk[self.ENTRY_SIZE:self.ROW_SIZE]
                    
                    sid = int.from_bytes(sid_b, byteorder='little')
                    val = int.from_bytes(val_b, byteorder='little')

                    if val > threshold:
                        dump.write(str(sid) + ',' + str(val) + '\n')
    
                    
                
        
