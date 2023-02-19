from email.mime.text import MIMEText
import json
import os
import sys
from time import strftime
import requests
from datetime import datetime, timedelta
from stem import Signal
from stem.control import Controller
import getpass
import smtplib, ssl


# select correct config file based on executed script
APP_NAME = sys.argv[0].split('\\')[len(sys.argv[0].split('\\'))-1]
match APP_NAME:
    case 'retrieve_article_links.py':
        config_file_name = '../config/articles_config.json'
    case 'keyword_search.py':
        config_file_name = '../config/keywords_config.json'
with open(config_file_name, 'r') as config_file:
    CONFIG = json.load(config_file)


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
if CONFIG['getDeltaRecords'] and os.path.exists(DEST_FOLDER):
    EXISTING_FILES = [os.path.join(DEST_FOLDER, file) for file in os.listdir(DEST_FOLDER)]
    for file in EXISTING_FILES:
        # open each file and read entries
        with open(file, 'r', encoding='utf-8') as latest_file:
            LATEST_CONTENT += latest_file.read()


# read url setting from config
def get_urls():
    urls = CONFIG['websiteconfig']['webpages']
    return urls


def get_webpage(urls):
    pages = []
    # define client and prepare header
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    headers = {'User-Agent': user_agent}
    # Check if a controller should be used
    if CONFIG['controllerPort'] == 0:
        for webpage in urls:
            try: 
                response = requests.get(webpage, headers=headers)
                pages.append(response)
            except Exception as e:
                print('Error accessing webpages. Error Message: ', str(e))
        print('Responses: ', pages)
    else:
        # use controller
        with Controller.from_port(port=CONFIG['controllerPort']) as controller:
            controller.authenticate()
            # loop through list of urls and get webpage contents
            for webpage in urls:
                try: 
                    controller.signal(Signal.NEWNYM)
                    response = requests.get(webpage, headers=headers)
                    pages.append(response)
                except Exception as e:
                    print('Error accessing webpages. Error Message: ', str(e))
        print('Responses: ', pages)
    return pages


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
                print('Error writing result file. Error Message: ', str(e))


def keep_delta(record):
    # check if current record is in existing file
    if record.replace('\n', '') in LATEST_CONTENT.replace('\n', ''):
        # clear record if it already exists in any file
        record = ''
    return record


def send_mail(articles):
    # SSL
    port = 465 
    # prompt for password of sending mail account - do not show password on console
    sender_mail = str(CONFIG['mailconfig']['senderMailAddress'])
    password = getpass.getpass("Enter password for sending mail account: ")
    receiver = str(CONFIG['mailconfig']['destinationMailAddress'])
    subject = str(CONFIG['mailconfig']['mailSubject'])
    # Create SSL context
    context = ssl.create_default_context()
    if not str(articles) == '':
        message = MIMEText(articles)
    else:
        message = MIMEText(str(CONFIG['mailconfig']['placeholder']))
    try: 
        with smtplib.SMTP_SSL(CONFIG['mailconfig']['mailServer'], port, context=context) as server:
            server.login(sender_mail, password)
            # build mail and send it
            message["Subject"] = subject
            message["From"] = sender_mail
            message["To"] = receiver
            server.sendmail(sender_mail, receiver, str(message))
    except Exception as e:
        print('Error sending mail. Error message: ' + str(e))
        

# check if there are any files older than the days specified and if so, delete them based on user input
def delete_old_files():
    obsolete_files = []
    [obsolete_files.append(file) for file in EXISTING_FILES if datetime.fromtimestamp(os.path.getctime(file)).date() < (TODAY - timedelta(days=CONFIG['timeDelta4Delete']))]
    if obsolete_files:
        delete_files = input("Found files older than " + str(CONFIG['timeDelta4Delete']) + " days. Delete them now (Y/n)? ")
        if delete_files.upper() in ["Y", "YES"]:
            for f in obsolete_files:
                os.remove(f)