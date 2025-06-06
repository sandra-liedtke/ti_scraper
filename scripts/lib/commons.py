import feedparser
from email.mime.text import MIMEText
import json
import os
import platform
import sys
from time import strftime
import requests
from datetime import datetime, timedelta
from stem.control import Controller
import getpass
import smtplib, ssl


# get os to define the path separator to be used
OPERATING_SYS = platform.system()
if OPERATING_SYS == "Windows":
    separator = "\\"
else:
    separator = "/"


# select correct config file based on executed script
APP_NAME = sys.argv[0].split(separator)[len(sys.argv[0].split(separator))-1]
if APP_NAME == 'retrieve_articles.py':
    config_file_name = '../config/articles_config.json'
elif APP_NAME == 'keyword_search.py':
    config_file_name = '../config/keywords_config.json'
elif APP_NAME == 'count_hits.py':
    config_file_name = '../config/counts_config.json'
elif APP_NAME == 'get_contents.py':
    config_file_name = '../config/contents_config.json'
else:
    print("Unknown app with name " + APP_NAME + ". Forgot to define the config file for it?")
    print("Cancelling...")
    exit()

# read config file
with open(config_file_name, 'r') as config_file:
    CONFIG = json.load(config_file)

#define header for webpage request
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    }

# get current date and add it to the result file name
TODAY = datetime.today().date()
# define destination file name depending whether a folder name is given
if CONFIG['resultfile']['folder']:
    DEST_FOLDER = '../' + CONFIG['resultfile']['folder'] + '/'
    DEST_FILE_NAME = DEST_FOLDER + str(TODAY) + '_' + strftime('%H%M%S', datetime.now().timetuple()) + '_' + CONFIG['resultfile']['filename']
else:
    DEST_FILE_NAME = str(TODAY) + '_' + strftime('%H%M%S', datetime.now().timetuple()) + '_' + CONFIG['resultfile']['filename']

# delta records can only be extracted if a subfolder is given and existing
LATEST_CONTENT = ''
EXISTING_FILES = []
try:
    if CONFIG['getDeltaRecords'] and os.path.exists(DEST_FOLDER):
        EXISTING_FILES = [os.path.join(DEST_FOLDER, file) for file in os.listdir(DEST_FOLDER)]
        for file in EXISTING_FILES:
            # open each file and read entries
            with open(file, 'r', encoding='utf-8') as latest_file:
                LATEST_CONTENT += latest_file.read()
except:
    'continue without delta setting'


# read url setting from config
def get_urls():
    urls = CONFIG['websiteconfig']['webpages']
    return urls


# read rss feeds from config
def get_rss_feeds():
    feeds = CONFIG['websiteconfig']['rss_feeds']
    return feeds


# get webpage content
def get_webpage(urls):
    pages = []
    # Check if a controller should be used
    if CONFIG['controllerPort'] == 0:
        for webpage in urls:
            try:
                response = requests.get(webpage, headers=header)
                pages.append(response)
            except Exception as e:
                print(e)
                print('Error accessing webpages')
        print('Responses: ', pages)
    else:
        # use controller
        with Controller.from_port(port=CONFIG['controllerPort']) as controller:
            controller.authenticate()
            # loop through list of urls and get webpage contents
            for webpage in urls:
                try:
                    response = requests.get(webpage, headers=header)
                    pages.append(response)
                except Exception as e:
                    print(e)
                    print('Error accessing webpages')
        print('Responses: ', pages)
    return pages


# get rss feeds
def get_rss(urls):
    # load RSS
    feed_contents = []
    for feed_url in urls:
        try:
            feed = feedparser.parse(feed_url)
            # parse RSS Tree
            for item in feed.entries:
                record = item["link"] + "|" + item["title"]
                feed_contents.append(record)
        except Exception as e:
            print(e)
            print('Error accessing webpages')
    return feed_contents


# write result file
def write_file(articles):
    # check if result file folder is there
    if CONFIG['resultfile']['folder'] and not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)
    if str(articles) == '':
        articles = str(CONFIG['mailconfig']['placeholder'])
    try:
        # create result file
        with open(DEST_FILE_NAME, 'w', encoding="utf-8") as resultfile:
            resultfile.write(str(articles))
    except Exception as e:
        print(e)
        print('Error writing result file')


# check delta
def keep_delta(record):
    # check if current record is in existing file
    if record.replace('\n', '') in LATEST_CONTENT.replace('\n', ''):
        # clear record if it already exists in any file
        record = ''
    return record


# send mail
def send_mail(articles, message_type):
    # use encrypted connection to the mailserver
    port = 465 
    # prompt for password of sending mail account - do not display password on console
    sender_mail = str(CONFIG['mailconfig']['senderMailAddress'])
    password = getpass.getpass("Enter password for sending mail account: ")
    # get receiver mail address and subject from config file
    receiver = str(CONFIG['mailconfig']['destinationMailAddress'])
    subject = str(CONFIG['mailconfig']['mailSubject'])
    # Create SSL context
    context = ssl.create_default_context()
    # send articles if available, else send the placeholder text defined in the config
    if not str(articles) == '':
        message = MIMEText(articles, message_type)
    else:
        message = MIMEText(str(CONFIG['mailconfig']['placeholder']))

    try:
        # connect to the mailserver and send mail
        with smtplib.SMTP_SSL(CONFIG['mailconfig']['mailServer'], port, context=context) as server:
            server.login(sender_mail, password)
            message["Subject"] = subject
            message["From"] = sender_mail
            message["To"] = receiver
            server.sendmail(sender_mail, receiver, str(message))
            server.quit()
    except Exception as e:
        # try disconnect
        try:
            server.quit()
        except:
            'disconnected'
        print('Error sending mail. Error message: ' + str(e))
        retry = input('Retry connection and sending mail [y/n]? ')
        # try again or skip
        if retry.upper() in ["Y", "YES"]:
            send_mail(articles, message_type)
        else:
            print("Skipping mailing function")
        

# check if there are any files older than the days specified in config and if so, delete them based on user input
def delete_old_files():
    obsolete_files = []
    if OPERATING_SYS == 'Windows':
        [obsolete_files.append(file) for file in EXISTING_FILES if datetime.fromtimestamp(os.path.getctime(file)).date() < (TODAY - timedelta(days=CONFIG['timeDelta4Delete']))]
    else:
        [obsolete_files.append(file) for file in EXISTING_FILES if datetime.fromtimestamp(os.path.getmtime(file)).date() < (TODAY - timedelta(days=CONFIG['timeDelta4Delete']))]
    if obsolete_files:
        delete_files = input("Found files older than " + str(CONFIG['timeDelta4Delete']) + " days. Delete them now [y/n]? ")
        if delete_files.upper() in ["Y", "YES"]:
            for f in obsolete_files:
                os.remove(f)