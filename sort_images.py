import sqlite3
import database_manager
import os
import sys

def main():
    # arguments when launching the program (bad_avg, good_avg) to sort the photos
    bad_avg = 0
    good_avg = 0
    if (len(sys.argv) > 2):
        db = database_manager.DatabaseManager()
        db.connect()
        avg = db.compute_avg()
        print avg
        list_id_bad = db.select_bad(bad_avg)
        list_id_good = db.select_good(good_avg)
        for id in list_id_bad:
            os.system("cp images/%s.jpg very_bad" % id)
        for id in list_id_good:
            os.system("cp images/%s.jpg very_good" % id)
    else:
        print "You have to enter two arguments when launching the programm: bad_avg and good_avg"
    
if __name__ == "__main__":
        main()