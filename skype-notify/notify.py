# report Skype unread messages with notify-send

import sqlite3
import subprocess
import argparse
import time
import signal
import sys
import glob
import os

parser = argparse.ArgumentParser(description='Desktop notifications for Skype unread messages')
parser.add_argument('-d', help='Skype database file (~/.Skype/[account]/main.db)')
parser.add_argument('-t', type=int, default=2, help='Check interval in seconds')
args = parser.parse_args()

if args.d:
    if (not os.path.exists(args.d)):
        print "Skype database file not found in " + args.d
        exit(1)
    db_path = args.d
else:
    db_paths = glob.glob("/home/*/.Skype/*/main.db")
    if len(db_paths) == 0:
        print "Skype database file not found (in /home/*/.Skype/*/main.db)"
        exit(1)
    db_path = db_paths[0]

print "Listening on " + db_paths[0] + " (Ctrl+C for exit)"

db = sqlite3.connect(db_path)

def signal_handler(signal, frame):
    db.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:
    res = db.execute("SELECT COUNT(*) FROM messages WHERE consumption_status=2")
    count = res.fetchone()[0]
    if (count > 0):
        msg = ""
        res = db.execute("SELECT author, COUNT(*) FROM messages WHERE consumption_status=2 GROUP BY author")
        for row in res:
            msg = msg + "{0}: {1}\n".format(row[1], row[0])
        subprocess.call(['notify-send', "Skype: {0} unread messages\n".format(count), msg])
    time.sleep(args.t)
