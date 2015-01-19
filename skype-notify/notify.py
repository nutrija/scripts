# Desktop notification for Skype unread messages

import sqlite3
import subprocess
import argparse
import threading

parser = argparse.ArgumentParser(description='Desktop notifications for Skype unread messages')
parser.add_argument('database', help='Skype database file (~/.Skype/[account]/main.db)')
parser.add_argument('-t', type=int, default=15, help='Check interval in seconds')
args = parser.parse_args()

def skype_notify():
    threading.Timer(args.t, skype_notify).start()
    db = sqlite3.connect(args.database)
    res = db.execute("SELECT COUNT(*) FROM messages WHERE consumption_status=2")
    count = res.fetchone()[0]
    if (count > 0):
        msg = ""
        res = db.execute("SELECT author, COUNT(*) FROM messages WHERE consumption_status=2 GROUP BY author")
        for row in res:
            msg = msg + "{0}: {1}\n".format(row[1], row[0])
        subprocess.call(['notify-send', "Skype: {0} unread messages\n".format(count), msg])
    db.close()

skype_notify()
