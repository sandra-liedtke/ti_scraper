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



WICHTIG: Die Skripte verwenden Konfigurationsdateien, die eine schnelle und einfache Anpassung ermöglichen. Bevor die Skripte das erste mal ausgeführt werden, sollten die [Konfigurationen (eng)](Configurations(en).md) überprüft und ggf. individuell geändert werden.</br>
Eine weitere Möglichkeit, die Skripte anzupassen und zu erweitern, ist in der Datei [Extensibility (en)](Extensibility(en).md) beschrieben.

Diese Arbeit unterliegt den Bestimmungen einer MIT-Lizenz.<br/>
© 2023 Sandra Liedtke.

### System-Anforderungen

 - Die Skripte wurden auf Windows und Linux getestet
 - Python 3.9 oder höher
 - Python Libraries, die ggf. separat installiert werden müssen:
     - beautifulsoup4
     - requests
     - stem
     - demisto-py (oder aus [Github](https://github.com/demisto/demisto-py))
     - tzlocal
     - sumy
     - numpy
     - feedparser
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



IMPORTANT: Each of the scripts uses a configuration file which allows a fast and easy customization. Before the scripts are executed for the first time, the [configuration settings](Configurations(en).md) should be reviewed and adjusted where necessary. </br>
Further options to adjust and extend the scripts are described in the file [Extensibility (en)](Extensibility(en).md).

This work is licensed under an MIT License.<br/>
© 2023 Sandra Liedtke.

### System Requirements

 - The scripts have been tested on Windows and Linux
 - Python 3.9 or higher
 - Python libraries which might need separate installation: 
     - beautifulsoup4
     - requests
     - stem
     - demisto-py (or from [Github](https://github.com/demisto/demisto-py))
     - tzlocal
     - sumy
     - numpy
     - feedparser
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
