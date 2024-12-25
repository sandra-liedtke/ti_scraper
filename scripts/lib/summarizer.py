import re
from bs4 import BeautifulSoup
from lib.commons import *
from lib.regex import ALL_HTML, ESCAPE
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from lib.commons import get_webpage


# Clean webpages from HTML
def parse_websites(webpages):
    print("Parsing webpages and getting article texts")
    webpage_texts = []
    for webpage_entry in webpages:
        if not str(webpage_entry) == "":
            # use only the URL
            url = []
            url.append(webpage_entry.split("\n")[1])
            if not url[0].startswith("http"):
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
    summaries = ""
    for text in original_texts:
        try:
            # split headline, original text and URL at the separator
            split_entry = text.split("|")
            headline = split_entry[0]
            text = split_entry[1]
            url = split_entry[2]
            # setting stopwords based on top level domain of the url
            if url.rsplit(".", 1)[1].startswith("de"):
                stop_words = set(stopwords.words("german"))
            else:
                stop_words = set(stopwords.words("english"))
            # tokenize words
            words = word_tokenize(text)
            # frequency table with the scores of the words in each sentence
            freq_table = {}
            for word in words:
                word = word.lower()
                if word in stop_words:
                    continue
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1
            # get the score of the sentences
            sentences = sent_tokenize(text)
            sentence_value = {}
            for sentence in sentences:
                for word, freq in freq_table.items():
                    if word in sentence.lower():
                        if sentence in sentence_value:
                            sentence_value[sentence] += freq
                        else:
                            sentence_value[sentence] = freq

            # summarize values
            sum_values = 0
            for sentence in sentence_value:
                sum_values += sentence_value[sentence]

            # use average value of the sentences to create summary
            average = int(sum_values / len(sentence_value))
            summarized_text = ''
            for sentence in sentences:
                # define which sentences should be part of the summary - set last part (1.x * average) lower for more details and higher for less details
                if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
                    summarized_text += " " + sentence
            if not summarized_text in str(summaries):
                summaries += headline + ":\n" + (str(summarized_text)) + "\nFROM: " + url + "\n\n"
        except Exception as e:
                print('Error Summarizing. Skipping summary of current entry.')
    # return all summaries when finished
    return summaries