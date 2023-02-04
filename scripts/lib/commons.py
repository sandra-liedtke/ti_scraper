import os
from time import strftime
import requests
import json
from datetime import datetime, timedelta


# load config
with open('../config/config.json', 'r') as config_file:
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
        with open(file, 'r') as latest_file:
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
    # loop through list of urls and get webpage contents
    for webpage in urls:
        try: 
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
    try:
        # create result file
        with open(DEST_FILE_NAME, 'w', encoding="utf-8") as resultfile:
            resultfile.write(str(articles))
    except Exception as e:
                print('Error writing result file. Error Message: ', str(e))


def keep_delta(record):
    # check if current record is in newest existing file
    if record in LATEST_CONTENT:
        # clear record if it already exists in latest file
        record = ''
    return record


def send_mail(articles):
    # still a TODO
    return 'OK'


# check if there are any files older than the days specified and if so, delete them based on user input
def delete_old_files():
    obsolete_files = []
    [obsolete_files.append(file) for file in EXISTING_FILES if datetime.fromtimestamp(os.path.getctime(file)).date() < (TODAY - timedelta(days=CONFIG['timeDelta4Delete']))]
    if obsolete_files:
        delete_files = input("Found files older than " + str(CONFIG['timeDelta4Delete']) + " days. Delete them now (Y/n)? ")
        if delete_files.upper() in ["Y", "YES"]:
            for f in obsolete_files:
                os.remove(f)