from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import re
from bs4 import BeautifulSoup
from lib.commons import *
from lib.regex_patterns import ALL_HTML, ESCAPE
from lib.commons import get_webpage


# Clean webpages from HTML
def parse_websites(webpages):
    print("Parsing webpages and getting article texts")
    webpage_texts = []
    for webpage_entry in webpages:
        # do not try to summarize empty records
        if not str(webpage_entry) == "":
            # use only the URL
            url = []
            url.append(webpage_entry.split("\n")[1])
            if not url[0].startswith("http"):
                continue
            if url[0].rsplit(".", 1)[0] in str(CONFIG['websiteconfig']['rss_feeds']):
                continue
            try:
                # call webpage
                webpage = get_webpage(url)
                webpage = webpage[0]
                # parse webpage content
                website_content = BeautifulSoup(webpage.content, 'html.parser')
                # only page which requires the article tag - retrieving p tags does not give the required result
                if "bleepingcomputer" in str(url[0]):
                    website_content = website_content.find('article')
                # find the text of the article for all other pages
                elif website_content.find('p'):
                    website_content = website_content.find_all('p')
                # only fallback - the article text should be organized in p tags
                elif website_content.find('main'):
                    website_content = website_content.find('main')
                else:
                    website_content = website_content.find('body')

                # remove HTML tags
                orig_text = re.sub(ALL_HTML, '', str(website_content))
                # clean from duplicate escape characters
                orig_text = re.sub(ESCAPE, '', orig_text)

                # collect the texts of the articles
                if not orig_text in str(webpage_texts):
                    webpage_texts.append(webpage_entry.split("\n")[0] + "|" + orig_text + "|" + str(webpage_entry.split("\n")[1]))
            except Exception as e:
                print('Error cleaning webpage content for webpage ', str(webpage.url), '. Error Message: ', str(e))
                continue
    return webpage_texts


# summarizing the texts
def summarize(original_texts):
    print("Summarizing webpages...")
    summaries = '''\
    <html>
    <head></head>
    <body>
    '''
    for text in original_texts:
        try:
            # split headline, original text and URL at the separator
            split_entry = text.split("|")
            headline = split_entry[0]
            text = split_entry[1]
            url = split_entry[2]
            # setting the language based on top level domain of the url
            if url.rsplit(".", 1)[1].startswith("de"):
                LANGUAGE = "german"
            else:
                LANGUAGE = "english"
            SENTENCES_COUNT = 5

            parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)
            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)
            # the final summary
            summarized_text = ''
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                summarized_text += " " + str(sentence).replace('<Sentence:', '').replace('>', '')
            if not str(summarized_text) in str(summaries):
                summaries += '<h3>' + headline + ':</h3><p>' + (str(summarized_text)) + '<br>FROM: <a href="' + url + '">' + url + '</a></p><br>'
        except Exception as e:
            print(e)
            print('Error Summarizing. Skipping summary of current entry.')
    # return all summaries when finished
    summaries += '''
    </body>
    </html>
    '''
    return summaries