#Configuration Options

There are some configurations that may be modified before running the related script:

 - To consider RSS feeds for scraping, the url to the respective XML-file can be added to or deleted from the `rss_feeds` section. These articles will not be considered by the summarizer
 - To change the websites to be scraped, just add different links in the `webpages` section and/or remove existing links
 - In articles_config can be some `stopwords` defined to remove all entries which contain these stopwords
 - keywords_config does not contain a stopword section, but in the `keywords` part can be search words defined. Only entries containing these keywords will be kept in the result
 - In counts_config the names for which the hits should be count are given in `hit`. The functionality is comparable to the keyword search
 - Some websites may have many reference links embedded, which would be added to the result, but are actually not needed. For this the `specialHandling` section in articles_config defines under which circumstances those URLs should be added to the result following the logic *"Either the key is not contained in the URL, or the URL starts as given in the value"*
 - `getDeltaRecords` defines whether all entries currently displayed on the respective webpage should be kept or only those that are not yet listed in existing result files
     - The Delta-Update only works if a subfolder is given, where the result files are stored. It is not available for count_hits
 - `timeDelta4Delete` defines which files should be kept. The delete function collects all files which are older than the date calculated based on the time delta (in days). After confirmation on the command line, the files will be deleted.
 - In `controllerPort` can be defined which source port to use for the TOR-controller accessing the webpages. Value 0 defines that no controller should be used
     - The controller is only needed for scraping onion sites and hence, should be used **exclusively** for those
 - In the `resultfile` section can be defined whether a result file should be created, where it should be stored and how it should be named
     - If you give a folder name that is not yet existing, the script will create that respective folder
 - In counts_config can be table headers defined
 - In the `mailconfig` section can be defined whether mails should be sent. If so, also a SMTP-Server needs to be given, from which mails will be sent
 - The `sendSummary` defines that for each article a summary should be created and added to the mail.
 - The field `destinationMailAddress` contains the receiver's mail address
 - The sending mail address, which is also used to authenticate at the SMTP-Server, is given in `senderMailAddress`. Recommendation is to create a completely new mail account just for this purpose instead of using an existing address which is also used elsewhere
     - The password for the mail account is entered on the command line and should **never** be stored in the code or the configuration
 - In `mailSubject` can be the subject of the mail defined and in `placeholder` a text that will be contained in the mail body if there are no articles. The `placeholder` text is also written to the result file if there are no articles
 - articles_config and keywords_config have additionally an option to collect records containing specific keywords and to write them into a designated profiling file, which will not be considered by the delete function. In `profileRecords` can be defined if there are records to be collected, an profiling folder can be set and in `profileData` can be specified for which names the profiling should happen. This can be used to track specific malware or threat actors. If the name consists of two words, those must be written as one word (without blanks) to be recognized within the articles. <br/> Instead of creating textfiles, the profiling can also happen in Palo Alto Cortex® XSOAR (recommended). Details regarding the setup can be found in the file [PaloAlto Cortex XSOAR Integration (en)](PaloAlto_Cortex_XSOAR-Integration(en).md)
