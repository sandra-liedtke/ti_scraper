from bs4 import BeautifulSoup
from lib.commons import *
from lib.regex import *


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
                # clean from html markup
            cleaned_result = re.sub(ALL_HTML, '', str(website_content))
            # clean from duplicate escape characters
            cleaned_result = re.sub(ESCAPE, '', cleaned_result)
            if not cleaned_result in str(articles):
                articles.append(cleaned_result) 
        except Exception as e:
            print('Error cleaning webpage content for webpage ', str(listentry.url), '. Error Message: ', str(e))
            continue
    return articles


def format_result(articles):
    result_str = ""
    # concatenate list entries to result string
    for entry in articles:
        # build and format record for each article to be added to the result
        new_record = keep_delta(entry + '\n\n\n\n############################################################################# NEXT RECORD #############################################################################\n\n\n\n')
        result_str += new_record
    return result_str


def main():
    print('\n')
    print('++++++++++++++++++++++++++++++++++ CONTENT SCRIPT START ++++++++++++++++++++++++++++++++++')
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