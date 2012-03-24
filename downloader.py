#!/usr/bin/env python

import BeautifulSoup
import urllib2
import urllib
import re
import sys
import database_manager
import sqlite3

USER_AGENT = ("Mozilla/5.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4")
        
HEADERS = { 'User-Agent': USER_AGENT }

AVERAGE_RE = re.compile(" (?P<avg>\d(?:\.\d\d?)?)/7 average")

VOTES_RE = re.compile("ratings-breakdown\?photo_id=\d+>(?P<votes>\d+)")

DATE_RE = re.compile("Uploaded&nbsp;Date</th>\s*<td>(?P<date>\d\d\d\d-\d\d-\d\d)",re.MULTILINE)

TAGS_RE = re.compile("/gallery/tag-search/search\?query_string=.+?\">(?P<tags>.*?)</a>")

USER_RE = re.compile("member-photos\?user_id=(?P<user>\d+)")

URL_FORMAT = "http://photo.net/photodb/photo?photo_id=%s"

OUTPUT_FOLDER = './photoNet2/'

# method that downolad photo and return meta_data
def get_photo(photo_id, folder=OUTPUT_FOLDER):
    url = URL_FORMAT % photo_id 
    req = urllib2.Request(url, None, HEADERS)
    page_content = urllib2.urlopen(req).read()
    soup = BeautifulSoup.BeautifulSoup(page_content)
    
    # parse source code to retrieve meta_data
    try:
        avg = AVERAGE_RE.search(page_content).group('avg')
        votes = VOTES_RE.search(page_content).group('votes')
        date = DATE_RE.search(page_content).group('date')
        user = USER_RE.search(page_content).group('user')
        tags = TAGS_RE.findall(page_content)
        # delete doublons
        s = len(tags)
        for i in range(0,s/2):
            i = tags.pop(0)
        list_tags = ", ".join(tags)
        #download the photo
        for tag in soup.findAll("meta"):
            if tag.get("property") == "og:image":
                urllib.urlretrieve(tag['content'],"%s%s.jpg" % (folder, photo_id))
        return (photo_id, user, list_tags, date, votes, avg)
    except:
        return None
        
def main():
    # arguments when launching the program (start_id, end_id) to search the photos
    start_id = 0
    end_id = 0
    if (len(sys.argv) > 2):
        start_id = int(sys.argv[1])
        end_id = int(sys.argv[2])
        # connect to DB
        db = database_manager.DatabaseManager()
        db.connect()

       # search photos in range given and download them
        for id in range (start_id, end_id):
            insert_values = get_photo(id)
            # insert values in DB if id not already in database
            try:
                if insert_values != None:
                    print insert_values
                    db.insert(insert_values)
            except sqlite3.IntegrityError:
                print "photo " + id + " is already in the database"

        # print the database in the terminal
        #db.print_db()

        # close database
        db.close
    else:
        print "You have to enter two arguments when launching the programm: start_id and end_id"
    
    

if __name__ == "__main__":
    main()