# TI Scraper

*- English Version Below -*

### Beschreibung

Dieses Repository enthält eine Sammlung an Skripten, die für die Verwendung im Rahmen von Cyber Threat Intelligence entwickelt wurden. Prinzipiell können die Skripte aber auch für andere Themen verwendet werden, wenn die URLs und/oder Schlüsselwörter in den Konfigurationsdateien geändert werden. </br>
Ziel war die Erstellung einer möglichst konfigurierbaren und individuell anpassbaren Skriptsammlung, die ohne Änderungen am Code an aktuelle Entwicklungen und individuelle Anforderungen angepasst werden kann. Zudem kann die Sammlung mit wenig Aufwand um weitere Skripte erweitert werden. Das Repository unterliegt einer ständigen Weiterentwicklung, d.h. es kommen von Zeit zu Zeit weitere Skripte und Funktionen hinzu. Die folgenden Skripte sind bisher verfügbar:
 - **retrieve_articles.py:** verwendet die Konfigurationen aus articles_config.json, um aus einer Sammlung von Webseiten die neuesten Artikel zu extrahieren, in eine Datei zu schreiben und/oder per Mail zu versenden. Es werden alle Überschriften (sofern extrahierbar) und URLs zu den Artikeln ins Ergebnis geschrieben, die keines der Stopwords enthalten. Es kann auch konfiguriert werden, dass eine Zusammenfassung für jeden Artikel mitgesendet werden soll. Das Skript ist dafür vorgesehen, aus den definierten Fachzeitschriften die neuesten Beiträge zusammenzustellen und erfüllt damit den gleichen Zweck wie ein selbst zusammengestellter Newsletter
 - **keyword_search.py:** verwendet die Konfigurationen aus keywords_config.json, um aus einer Sammlung von Webseiten lediglich die Artikel zu extrahieren, die eines oder mehrere der definierten Keywords enthalten. Das Ergebnis (Überschriften sofern extrahierbar und URLs zu den Artikeln) kann in eine Textdatei geschrieben und/oder per Mail versendet werden. Das Skript kann eingesetzt werden, um aus aktuellen Nachrichten- und Pressemeldungen die Beiträge zu extrahieren, die für die Threat Intelligence zusätzlich relevant sind
 - **count_hits.py:** verwendet die Konfigurationen aus counts_config.json, um aus einer Liste von URLs auszuzählen, wie oft ein bestimmter Name oder ein bestimmtes Wort in den Ergebnissen gefunden wird. Es wird nur gezählt, auf wie vielen unterschiedlichen Seiten ein Wort auftaucht, nicht wie oft es auf ein und der selben Seite gefunden wird. Das Skript eignet sich insbesondere, um zu testen, ob es öffentliche Mitteilungen über einen Sicherheitsvorfall bei einem (oder mehreren) bestimmten Unternehmen gibt. Es ist primär dafür vorgesehen, auf onion-Seiten proaktiv nach Informationen zu Data Leaks oder erfolgten Angriffen auf das eigene Unternehmen, Kunden oder Geschäftspartner zu suchen. <br/> Der Code ist dahingehend optimiert, eine CSV-Datei anzulegen, die eine Tabelle mit drei Spalten enthält. In der ersten werden die Namen aus dem `hit`-Setting in alphabetischer Reihenfolge ausgegeben, in der zweiten Spalte ist die Anzahl der Treffer enthalten und in der dritten Spalte ist der Kontext, also die URL und die letzten 35 Zeichen vor dem Namen sowie die nächsten 35 Zeichen danach, enthalten. Im Idealfall enthält die zweite Spalte eine Null ("0") und die dritte ist leer
 - **get_contents.py:** verwendet die Konfigurationen aus contents_config.json, um den Inhalt der Webseiten in eine Textdatei zu schreiben. Es wird der komplette Text-Inhalt der Seite aus dem `body`- oder `main`-Tag in die Datei geschrieben, ohne HTML-Tags, JavaScript-Funktionen und Bilder. Header und Footer werden nicht extrahiert. Das Skript ist dazu vorgesehen, insbesondere aus Blog-Webseiten Text-Inhalte zu extrahieren und in der Datei abzulegen. Dadurch kann festgestellt werden, ob sich eine Seite seit dem letzten Aufruf geändert hat ohne die Seite im Browser zu öffnen. Insbesondere für onion-Seiten kann dies ein Anwendungsfall sein

Beispiele für die Ergebnisdateien der mit der Standardkonfiguration ausgeführten Skripte befinden sich im Unterverzeichnis [Examples](/assets/examples) des Repositorys. Das Demo-Video zeigt die Ausführung des [retrieve_articles.py](/scripts/retrieve_articles.py) mit integriertem Profiling in der PaloAlto Cortex XSOAR.</br>


https://github.com/sandra-liedtke/ti_scraper/assets/60545571/ad395406-6c77-4d23-b473-cf2a0d154096



WICHTIG: Die Skripte verwenden Konfigurationsdateien, die eine schnelle und einfache Anpassung ermöglichen. Bevor die Skripte das erste mal ausgeführt werden, sollten die Konfigurationen überprüft und ggf. individuell geändert werden.</br>
Eine weitere Möglichkeit, die Skripte anzupassen und zu erweitern, ist in der Datei [Extensibility (en)](Extensibility(en).md) beschrieben.

Diese Arbeit unterliegt den Bestimmungen einer MIT-Lizenz.<br/>
© 2023 Sandra Liedtke.

### Konfigurationsmöglichkeiten

Einige Konfigurationen sollten eventuell geändert werden, bevor das zugehörige Skript gestartet wird:
 - Um die Webseiten zu ändern, die durchsucht werden sollen, können in der `webpages`-Sektion Links hinzugefügt oder gelöscht werden
 - In articles_config können `stopwords` definiert werden, sodass Einträge, die diese Stopwords enthalten, nicht ins Ergebnis geschrieben werden
 - keywords_config enthält keine Stopword-Sektion, dafür können im `keywords`-Teil Schlüsselworte definiert werden, nach welchen gesucht werden soll. Nur Einträge, die diese Schlüsselworte enthalten werden ins Ergebnis geschrieben
 - In counts_config werden die Namen, deren Treffer gezählt werden sollen, in `hit` angegeben. Die Funktionsweise ist vergleichbar mit der Schlüsselwortsuche
 - Einige Webseiten haben viele Referenzlinks, die automatisch mit ins Ergebnis geschrieben werden, aber eigentlich nicht gebraucht werden. Dafür kann in der `specialHandling`-Sektion in articles_config definiert werden, unter welchen Umständen Links für diese Webseiten ins Ergebnis geschrieben werden sollen nach der Logik *"Entweder der Key ist nicht in der URL enthalten, oder die URL fängt mit dem Value an"*
 - `getDeltaRecords` definiert, ob alle Einträge der jeweiligen Webseiten ins Ergebnis geschrieben werden sollen oder nur diejenigen, die noch nicht in vorherigen Dateien auftauchen
     - Das Delta-Update funktioniert nur, wenn ein Unterordner für die Ergebnisdateien angegeben wird. Es ist nicht verfügbar für count_hits
 - In `timeDelta4Delete` kann definiert werden, welche Dateien aufgehoben werden sollen. Die Löschfunktion sammelt alle Dateien ein, die älter sind als das Datum, das anhand des Zeitdeltas (in Tagen) errechnet wird. Nach Bestätigung auf der Kommandozeile werden die Dateien dann gelöscht.
 - In `controllerPort` kann definiert werden, welchen Quellport der TOR-Controller verwenden soll, welcher auf die Webseiten zugreift. Der Wert 0 legt fest, dass kein Controller verwendet werden soll.
     - Der Controller wird lediglich für onion-Seiten benötigt und sollte daher **ausschließlich** für diese verwendet werden
 - In der `resultfile`-Sektion kann definiert werden, ob eine Datei mit den Ergebnissen erzeugt werden soll, wo diese gespeichert werden und wie sie heißen soll
     - Wenn ein Ordnername angegeben wird, der noch nicht existiert, erzeugt das Skript den Ordner
 - In der counts_config können in `tableHeaders` die Überschriften für die auszugebende Tabelle definiert werden
 - Im `mailconfig`-Abschnitt kann angegeben werden, ob Mails gesendet werden sollen. In dem Fall muss auch ein SMTP-Server angegeben werden, von welchem aus die Mails versendet werden
 - Mit `sendSummary` kann festgelegt werden, dass auch eine Zusammenfassung für jeden Artikel erstellt und mit der Mail mitgesendet werden soll.
 - Das Feld `destinationMailAddress` enthält die Empänger-Mailadresse
 - Die sendende Mail-Addresse, die sich am SMTP-Server authentifiziert, wird in `senderMailAddress` angegeben. Es ist empfehlenswert, hierfür eine komplett eigene Mail-Adresse zu erstellen anstatt einen existierenden Account zu verwenden, der auch für andere Dinge verwendet wird
     - Das Passwort wird auf der Kommandozeile abgefragt während das Programm läuft und sollte **niemals** im Code oder in der Konfiguration gespeichert werden
 - In `mailSubject` kann dann noch der Betreff angegeben werden und in `placeholder` ein Text, der in der Mail enthalten ist, wenn es keine neuen Artikel gibt. Der Text aus `placeholder` wird auch in die Datei geschrieben, wenn es keine neuen Artikel gibt
 - articles_config und keywords_config enthalten zusätzlich noch die Option, Einträge für bestimmte Namen zu sammeln und sie in eine eigene Profiling-Datei zu schreiben, die nicht gelöscht wird. In `profileRecords` kann festgelegt werden, ob Artikel, die entsprechende Namen enthalten, gesammelt werden sollen, es kann ein Ordner für die Dateien angegeben werden und in `profileData` kann festgelegt werden, für welche Namen das Profiling stattfinden soll. Dadurch können Artikel zu bestimmter Malware oder definierten Akteuren getrackt werden. Wenn der Name aus zwei Wörtern besteht, müssen diese zusammengeschrieben werden (ohne Leerzeichen), damit sie in den Artikeln erkannt werden. <br/>Anstatt in Textdateien kann das Profiling auch in Palo Alto Cortex® XSOAR stattfinden (empfohlen). Die Details dazu sind in der Datei [PaloAlto Cortex XSOAR Integration (en)](PaloAlto_Cortex_XSOAR-Integration(en).md) hinterlegt

### System-Anforderungen

 - Die Skripte wurden auf Windows und Linux getestet
 - Python 3.9 oder höher
 - Python Libraries, die ggf. separat installiert werden müssen:
     - beautifulsoup4
     - requests
     - stem
     - demisto-py (oder aus [Github](https://github.com/demisto/demisto-py))
     - tzlocal
 - Wenn der Controller verwendet wird, muss der Computer sich mit dem TOR-Netzwerk verbinden können
 - Ein E-Mail Account, um die Ergebnisse per Mail versenden zu können und ein weiterer Account (oder eine Alias-Adresse), der die Mails empfängt (kann auch der gleiche sein)
 - Notepad++ oder vergleichbares um die Text-Dateien zu öffnen
 - Excel oder Libre Calc, um die CSV-Dateien öffnen zu können

 ### Quellen

 Aus den folgenden Quellen werden mit der Standardkonfiguration Artikel/Inhalte gezogen:
 - https://www.bleepingcomputer.com
 - https://www.darkreading.com
 - https://thehackernews.com
 - https://www.infosecurity-magazine.com
 - https://www.security-insider.de
 - https://www.heise.de
 - https://www.n-tv.de
 - https://www.tagesschau.de
 - https://www.cnbc.com
 - https://krebsonsecurity.com


## English Version

### Description

This repository contains a collection of scripts which have been developed for the usage in the context of cyber threat intelligence. However, the scripts may be used for other topics as well if the URLs and/or the keywords in the configuration files are changed. </br>
The purpose was the creation of a configurable and individually adjustable collection of scripts, which can be matched to current conditions and individual requirements without the need to change the code. Furthermore the collection can be extended by additional scripts with very little effort. The repository is still in development, meaning there will be more scripts and functions added to the repo from time to time. The following scripts are available as of now:
 - **retrieve_articles.py:** uses the configurations from articles_config.json to extract the newest articles from a collection of webpages, write them into a file and/or send them via mail. It will take all headlines (if available) and URLs of the articles, which do not contain any of the stopwords defined. There is also a configuration to add a summary for each article. The script is intended to be used for the collection of the latest entries from the defined journals and therefore works as a customizable newsletter
 - **keyword_search.py:** uses the configurations from keywords_config.json to extract those articles from a collection of websites, which contain one or more of the keywords defined. The result (headlines if available and URLs of the articles) can be written into a text file and/or be sent via mail. The script can be used to collect the latest posts from news media, which may be additionally relevant for threat intelligence
 - **count_hits.py:** uses the configurations from counts_config.json to count from a list of URLs how often a certain name or word is found in the results. It only counts on how many different pages the word is found, not how often it is found on the same webpage. The script is especially useful to check if there are public announcements about a security incident for one (or more) specific company. Its primary usage is to proactively check onion sites for information regarding data leaks or attacks on the own company, clients or partners.<br/>The code is optimized for creating a csv file containing a table with three columns. The first column contains the names from the `hit` setting in alphabethical order, the second one contains the count of the hits and the third contains the context, meaning the URL and the last 35 characters before the name as well as the next 35 characters after it. Ideally the second column contains a zero ("0") and the third should be empty
 - **get_contents.py:** uses the configurations from contents_config.json to write the contents of a webpage into a text file. The entire text content of the `body` or `main` tags are written to the file without the HTML tags, JavaScript functions and images. Header and footer are not extracted. The script can be used to extract the contents of a webpage, especially of blog websites. This way can be determined if a webpage`s content has changed since the last call without opening it in the browser. This can be a use case especially for onion sites

Examples for the result files of the scripts run with the default configuration can be found in the repository sub-directory [Examples](/assets/examples). The demo video shows the execution of [retrieve_articles.py](/scripts/retrieve_articles.py) with integrated profiling in the PaloAlto Cortex XSOAR.</br>


https://github.com/sandra-liedtke/ti_scraper/assets/60545571/eea9f576-4fb1-4873-8682-dbd121d00957



IMPORTANT: Each of the scripts uses a configuration file which allows a fast and easy customization. Before the scripts are executed for the first time, the configuration settings should be reviewed and adjusted where necessary. </br>
Further options to adjust and extend the scripts are described in the file [Extensibility (en)](Extensibility(en).md).

This work is licensed under an MIT License.<br/>
© 2023 Sandra Liedtke.

### Configuration Options

There are some configurations that may be modified before running the related script:
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
 
### System Requirements

 - The scripts have been tested on Windows and Linux
 - Python 3.9 or higher
 - Python libraries which might need separate installation: 
     - beautifulsoup4
     - requests
     - stem
     - demisto-py (or from [Github](https://github.com/demisto/demisto-py))
     - tzlocal
 - If the controller is used, the computer must be able to connect to the TOR-Network
 - A mail account for sending the result via mail and a mail account or alias-address receiving the result (may also be the same)
 - Notepad++ or similar to open the resulting text files
 - Excel or Libre Calc to open the csv files

 ### Sources

With the default configuration, articles/contents from below sources are being retrieved:
 - https://www.bleepingcomputer.com
 - https://www.darkreading.com
 - https://thehackernews.com
 - https://www.infosecurity-magazine.com
 - https://www.security-insider.de
 - https://www.heise.de
 - https://www.n-tv.de
 - https://www.tagesschau.de
 - https://www.cnbc.com
 - https://krebsonsecurity.com
