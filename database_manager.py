import sqlite3

class DatabaseManager:
    
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS photos (photo_id PRIMARY KEY, user_name text, tags text, upload_date text, vote text, avg text);"
        
    INSERT_QUERY = "INSERT INTO photos (photo_id, user_name, tags, upload_date, vote, avg) VALUES (?, ?, ?, ?, ?, ?);"

    conn = ''

    c = ''
  
    def connect(self):
        self.conn = sqlite3.connect('database.sqlite')
        self.c = self.conn.cursor()
        # Create table
        self.c.execute(self.CREATE_TABLE)
        self.conn.commit()
        
    def insert(self,insert_values):
        # Insert into table
        self.c.execute(self.INSERT_QUERY, insert_values)
        # Commit the changes
        self.conn.commit()

    def photo_exist(self, photo_id):
        # Check if a photo is already in the database
        self.c.execute('SELECT COUNT (*) FROM photos WHERE photo_id = %s' % photo_id)
        result = self.c.fetchone()
        count = result[0]
        print count
        if (count == 0):
            return False
        else:
            return True

    def print_db(self):
        # Select all
        self.c.execute('SELECT* FROM photos')
        for row in self.c:
            print row

    def close(self):
        # Close the cursor
        self.conn.close()

