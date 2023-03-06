from bs4 import BeautifulSoup
from lib.commons import *


def get_hits(websites):
    hits = []
    for listentry in websites:
        try:
            website_content = BeautifulSoup(listentry.content, 'html.parser')
            website_content = website_content.prettify()
            # for each name in the config check add if it was found or not
            for hit in CONFIG['websiteconfig']['hit']:
                found = 0
                webpage_url = '-'
                extract = '-'
                # if the record was found
                if hit in website_content:
                    found = 1
                    webpage_url = listentry.url
                    start_Idx = website_content.index(hit) - 35
                    end_Idx = website_content.index(hit) + 35
                    extract = '...' + website_content[start_Idx:end_Idx].replace('\n', '').replace('\t', '').replace('\r', '') + '...'
                hits.append(hit + '|' + str(found) + '|' + webpage_url+ ': ' + extract) 
        except Exception as e:
            print('Error preparing webpage content for webpage ', str(listentry.url), '. Error Message: ', str(e))
    return hits


def format_result(hit_counts):
    result_str = ''
    separator = ';'
    # get headers
    for header in CONFIG['resultfile']['tableHeaders']:
        result_str += header + separator 
    result_str += '\n'
    # sort prepared list
    hit_counts.sort()
    for entry in hit_counts:
        # split entry and update record in result_str if already there
        entry = entry.split('|')
        if entry[0] in result_str:
            old_result_record = result_str.split(entry[0])[1]
            old_result_record = old_result_record.split(separator)
            # update count
            count = int(old_result_record[1]) + int(entry[1])
            # concatenate context if needed
            if entry[2] == '-, -':
                context = old_result_record[2]  
            elif old_result_record[2] == '-: -':
                context = entry[2]
            else:
                context = old_result_record[2]  + ',\t\t' + entry[2]
            new_record = entry[0] + separator + str(count) + separator + context
            result_str = result_str.replace(entry[0] + separator + old_result_record[1] + separator + old_result_record[2] , new_record)
        # add entry to result as it is not yet there
        else:
            new_record = str(entry[0]) + separator + str(entry[1]) + separator + str(entry[2])
            result_str += '\n' + new_record 
    return result_str


def main():
    print('\n')
    print('++++++++++++++++++++++++++++++++++ COUNTING HITS SCRIPT START ++++++++++++++++++++++++++++++++++')
    # get urls from config.json
    print('Getting URLS from config')
    url_list = get_urls()
    # call webpages
    print('Calling webpages as given in config.json')
    websites = get_webpage(url_list)
    # clean webpage content and format result
    print('Cleaning webpage contents')
    hit_counts = get_hits(websites)
    result = format_result(hit_counts)
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