
from bs4 import BeautifulSoup
from lib.commons import *
from lib.profiling import *
from lib.regex import *
from lib.aliases import *


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
            atags = website_content.find_all('a')
            # clean a-tags
            for entry in atags:
                cleaned_result = entry.get('href')
                headline = ""
                # find headline
                if len(re.findall(HEADLINE_HEADER, str(entry))) > 0:
                    headline = re.findall(HEADLINE_HEADER, str(entry))[0]
                elif len(re.findall(HEADLINE_H1, str(entry))) > 0:
                    hl = str(re.findall(HEADLINE_H1, str(entry)))
                    headline = hl.replace("[", "").replace("]", "")
                elif len(re.findall(HEADLINE_SPAN, str(entry))) > 0:
                    headline = re.findall(HEADLINE_SPAN, str(entry))[0]
                elif len(re.findall(HEADLINE_DIV, str(entry))) > 0:
                    headline = re.findall(HEADLINE_DIV, str(entry))[0]
                elif len(re.findall(HEADLINE_A, str(entry))) > 0:
                    headline = re.findall(HEADLINE_A, str(entry))[0]
                # if headline still has not been set before
                if headline == "":
                    if not cleaned_result.startswith('http'):
                        headline = cleaned_result.strip("/").replace('-', ' ').replace('.html', '').title()
                    else:
                        headline = cleaned_result.strip("/").split("/")[len(cleaned_result.strip("/").split("/"))-1].replace('-', ' ').replace('.html', '').title()
                # remove unnecessary extracted entries
                if not any(stopword.upper() in cleaned_result.upper() for stopword in CONFIG['websiteconfig']['stopwords']):
                    # add webpage prefix if not already contained in url 
                    if cleaned_result.strip().startswith("/"):
                        cleaned_result = str(listentry.url).replace("/fachbeitraege/", '') + cleaned_result.strip()
                    # add cleaned and filtered entry to result if it is not yet there
                    if not cleaned_result in str(articles):
                        articles.append(cleaned_result.strip() + "|" + str(headline))
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
        [articles.remove(x) for x in articles if x == "|"]
    except Exception as e:
        print('Error cleaning result ', str(articles), '. Error Message: ', str(e))
        print('Continuing processing without cleaning list...')
    # concatenate list entries to result string
    for entry in articles:
        # special handling: record is only added if either the key is not contained or the key AND value are both contained
        # loop through specialhandling dictionary
        for key, value in CONFIG['websiteconfig']['specialHandling'].items():
            # if the entry contains the key, but does not start with the repective value, exit the loop and process the next entry
            if key in entry and not entry.startswith(value):
                break
        # if the loop has not yet been stopped due to special handling
        else:
            # build and format record for each article to be added to the result
            new_record = keep_delta(entry.split("|")[1] + '\n' + entry.split("|")[0].replace('security//news/', '/news/').replace('theregister.com/security//', 'theregister.com/').replace('/blog/blog/', '/blog/').replace('darkreading.com/latest-news/','darkreading.com/')  +  '\n\n' )
            result_str += new_record
    return result_str


def main():
    print('\n')
    print('++++++++++++++++++++++++++++++++++ ARTICLE LINKS SCRIPT START ++++++++++++++++++++++++++++++++++')
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
    if CONFIG['profileRecords']:
        print('Updating profile records')
        profiling_records(result)
        # Checking if aliases should be updated
        if CONFIG['profiling']['profile2cortex']:
            alias_update = input("Want to update the cortex_aliases.config file (Y/n)? ")
            if alias_update.upper() in ["Y", "YES"]:
                update_aliases()
    # Checking for older files which will not be needed anymore
    delete_old_files()
    print('+++++++++++++++++++++++++++++++++++ SCRIPT END +++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    main()
