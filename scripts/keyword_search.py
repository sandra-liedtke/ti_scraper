from lib.commons import *
from lib.regex_patterns import *
from lib.profiling import *
from lib.aliases import *
from lib.summarizer import *


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
                # if the headline could not be retrieved, generate it from URL
                if headline == "":
                    if not cleaned_result.startswith('http'):
                        headline = cleaned_result.strip("/").replace('-', ' ').replace('.html', '').title()
                    else:
                        headline = cleaned_result.strip("/").split("/")[len(cleaned_result.strip("/").split("/"))-1].replace('-', ' ').replace('.html', '').title()
                # add cleaned and filtered entry to result if it is not yet there
                if not cleaned_result in str(articles):
                    articles.append(cleaned_result.strip() + "|" + headline)
        except Exception as e:
            print(e)
            print('Error cleaning webpage content for webpage ', str(listentry.url))
            continue
    return articles


def format_result(all_articles):
    result_str = ""
    # remove leftovers
    try:
        articles = []
        for rss_url in CONFIG['websiteconfig']['rss_feeds']:
            rss_page = rss_url.rsplit(".", 2)[0]
            for x in all_articles:
                if x.startswith(rss_page):
                    # remove unnecessary extracted entries from rss feed which do not contain any of the keywords
                    if any(keyword.upper() in x.upper() for keyword in CONFIG['websiteconfig']['keywords']):
                        articles.append(x)
        for url in CONFIG['websiteconfig']['webpages']:
            page = url.rsplit(".", 1)[0]
            for x in all_articles:
                if x.startswith(page):
                    # remove unnecessary extracted entries from the webpage which do not contain any of the keywords
                    if any(keyword.upper() in x.upper() for keyword in CONFIG['websiteconfig']['keywords']):
                        articles.append(x)
    except Exception as e:
        print(e)
        print('Error cleaning result ', str(all_articles))
        exit()
    # concatenate list entries to result string
    for entry in articles:
        # build and format record for each article to be added to the result
        new_record = keep_delta(entry.split("|")[1] + '\n' + entry.split("|")[0] +  '\n\n' )
        result_str += new_record
    return result_str


def main():
    print('\n')
    print('++++++++++++++++++++++++++++++++++++++++ KEYWORDS SEARCH SCRIPT START ++++++++++++++++++++++++++++++++++++++++')
    # get urls from config.json
    print('Getting URLS from config')
    url_list = get_urls()
    # getting rss feeds from config.json
    print('Getting RSS Feeds from config.json')
    feeds = get_rss_feeds()
    # call webpages
    print('Calling webpages as given in config.json')
    websites = get_webpage(url_list)
    # getting feed items from RSS Feeds
    print("Cleaning RSS feed items")
    articles = get_rss(feeds)
    # clean webpage content and format result
    print('Cleaning webpage contents')
    articles += clean_webpages(websites)
    result = format_result(articles)
    # write file and/or send as mail depending on config
    if CONFIG['resultfile']['createFile']:
        print('Writing result file')
        write_file(result)
    if CONFIG['mailconfig']['sendMail']:
        print('Preparing mail')
        # get and send summaries if specified in config
        if CONFIG['mailconfig']['sendSummary']:
            webpage_contents = parse_websites(result.split("\n\n"))
            result_summary = summarize(webpage_contents)
            send_mail(result_summary, "html")
        else:
            send_mail(result, "")
    if CONFIG['profileRecords']:
        print('Updating profile records')
        profiling_records(result)
        # Checking if aliases should be updated
        if CONFIG['profiling']['profile2cortex']:
            alias_update = input("Want to update the cortex_aliases.config file [y/n]? ")
            if alias_update.upper() in ["Y", "YES"]:
                update_aliases()
    # Checking for older files which will not be needed anymore
    delete_old_files()
    print('+++++++++++++++++++++++++++++++++++++++++++++++++ SCRIPT END +++++++++++++++++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    main()