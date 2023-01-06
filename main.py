import os
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime


# load config
with open('config/config.json', 'r') as config_file:
    CONFIG = json.load(config_file)


# get current date and add it to the result file name
TODAY = datetime.now().date()
# define destination file name depending whether a folder name is given
if CONFIG['resultfile']['folder']:
    DEST_FOLDER = CONFIG['resultfile']['folder'] + '/'
    DEST_FILE_NAME = DEST_FOLDER + str(TODAY) + '_' + CONFIG['resultfile']['filename']
else:
    DEST_FILE_NAME = str(TODAY) + '_' + CONFIG['resultfile']['filename']


ATAGS = re.compile('<a.*?>')
CLEAN = re.compile('<article.*?>|<a|class=".*?"|href=|[>]|name=".*?"|title=".*?"|["]')


# delta records can only be extracted if a subfolder is given and existing
LATEST_CONTENT = ''
if CONFIG['getDeltaRecords'] and DEST_FOLDER:
        EXISTING_FILES = [os.path.join(DEST_FOLDER, file) for file in os.listdir(DEST_FOLDER)]
        for file in EXISTING_FILES:
            # open newest file and read entries
            with open(file, 'r') as latest_file:
                LATEST_CONTENT += latest_file.read()


def get_urls():
    urls = CONFIG['websiteconfig']['webpages']
    return urls


def get_webpage(urls):
    pages = []
    for webpage in urls:
        try: 
            pages.append(requests.get(webpage))
        except Exception as e:
            print('Error accessing webpages. Error Message: ', str(e))
    print('Responses: ', pages)
    return pages


def clean_webpages(websites):
    articles = []
    for listentry in websites:
        try:
            website_content = BeautifulSoup(listentry.content, 'html.parser')
            # if "main" tags are not found use "body"
            if website_content.find('main'):
                website_content = website_content.find('main')
            else:
                website_content = website_content.find('body')
            # find all a-tags
            website_content = re.findall(ATAGS, str(website_content))
            # clean a-tags
            for entry in website_content:
                cleaned_result = re.sub(CLEAN, '', entry)
                # remove unnecessary extracted entries
                if not any(stopword in cleaned_result for stopword in CONFIG['websiteconfig']['stopwords']):
                    # add webpage prefix if not already contained in url 
                    if cleaned_result.strip().startswith("/"):
                        cleaned_result = str(listentry.url).replace("/fachbeitraege/", '') + cleaned_result.strip()
                    # add cleaned and filtered entry to result
                    articles.append(cleaned_result.strip())
        except Exception as e:
            print('Error cleaning webpage content for webpage ', str(listentry.url), '. Error Message: ', str(e))
    return articles


def format_result(articles):
    result_str = ""
    # remove leftovers
    try: 
        [articles.remove(x) for x in articles if not x.startswith("http")]
        [articles.remove(x) for x in articles if x.startswith("#")]
        [articles.remove(x) for x in articles if x.startswith("-")]
        [articles.remove(x) for x in articles if x.startswith("side")]
        [articles.remove(x) for x in articles if not x]
        # remove duplicates
        cleaned_list = []    
        [cleaned_list.append(x) for x in articles if x not in cleaned_list]
    except Exception as e:
        print('Error cleaning result ', str(articles), '. Error Message: ', str(e))
        print('Continuing processing without cleaning list...')
    # concatenate list entries to result string
    for entry in cleaned_list:
        # special handling for heise links
        if 'heise' not in entry and 'infosecurity-magazine' not in entry or entry.startswith('https://www.heise.de/security//news/') or entry.startswith('https://www.infosecurity-magazine.com/news/'):
            # if last character is a / the index of the text is different
            if entry.endswith('/'):
                # build and format record for each article to be added to the result
                new_record = keep_delta(entry.split("/")[len(entry.split("/"))-2].replace('-', ' ').replace('.html', '').upper() + ': ' + str(entry) +   '\n' )
                result_str += new_record
            else:
                # build and format record for each article to be added to the result
                new_record = keep_delta(entry.split("/")[len(entry.split("/"))-1].replace('-', ' ').replace('.html', '').upper() + ': ' + str(entry).replace('/security//news/', '/security/') + '\n' )
                result_str += new_record
    return result_str


def write_file(articles):
    # check if result file folder is there
    if CONFIG['resultfile']['folder'] and not os.path.exists(DEST_FOLDER):
        os.makedirs(CONFIG['resultfile']['folder'])
    try:
        # create result file
        with open(DEST_FILE_NAME, 'w') as resultfile:
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


def main():
    print('\n')
    print('++++++++++++++++++++++++++++++++++ SCRIPT START ++++++++++++++++++++++++++++++++++')
    # get urls from config.json
    print('Getting URLS from config')
    url_list = get_urls()
    # call webpages
    print('Calling webpages as given in config.json')
    websites = get_webpage(url_list)
    # clean webpage content and format result
    print('Cleaning webpage contents')
    articles = clean_webpages(websites)
    result = format_result(articles)
    # write file and/or send as mail depending on config
    if CONFIG['resultfile']['createFile']:
        print('Writing result file')
        write_file(result)
    if CONFIG['mailconfig']['sendMail']:
        print('Sending mail')
        send_mail(result)
    print('+++++++++++++++++++++++++++++++++++ SCRIPT END +++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    main()