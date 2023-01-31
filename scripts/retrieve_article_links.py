
from bs4 import BeautifulSoup
import re
from lib.commons import *


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
            website_content = website_content.find_all('a')
            # clean a-tags
            for entry in website_content:
                cleaned_result = entry.get('href')
                # remove unnecessary extracted entries
                if not any(stopword.upper() in cleaned_result.upper() for stopword in CONFIG['websiteconfig']['stopwords']):
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
        # special handling: record is only added if either the key is not contained or the key AND value are both contained
        # loop through specialhandling dictionary
        for key, value in CONFIG['websiteconfig']['specialHandling'].items():
            # if the entry contains the key, but does not start with the repective value, exit the loop and process the next entry
            if key in entry and not entry.startswith(value):
                break
        # if the loop has not yet been stopped due to special handling
        else:
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
    # Checking for older files which will not be needed anymore
    delete_old_files()
    print('+++++++++++++++++++++++++++++++++++ SCRIPT END +++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    main()