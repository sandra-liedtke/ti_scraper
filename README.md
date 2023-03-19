# TI Scraper

*- English Version Below -*

### Beschreibung

Dieses Repository enthält eine Sammlung an Skripten, die für die Verwendung im Rahmen von Cyber Threat Intelligence entwickelt wurden. Prinzipiell können die Skripte aber auch für andere Themen verwendet werden, wenn die URLs und/oder Schlüsselwörter in den Konfigurationsdateien geändert werden. 
Die folgenden Skripte sind hierfür verfügbar:
 - **retrieve_article_links.py:** verwendet die Konfigurationen aus articles_config.json, um aus einer Sammlung von Webseiten die neuesten Artikel zu extrahieren, in eine Datei zu schreiben und/oder per Mail zu versenden. Es werden alle Überschriften (sofern verfügbar) und URLs zu den Artikeln ins Ergebnis geschrieben, die keines der Stopwords enthalten. Das Skript ist dafür vorgesehen, aus Fachzeitschriften die neuesten Beiträge zusammenzustellen und erfüllt damit den gleichen Zweck wie ein selbst zusammengestellter Newsletter
 - **keyword_search.py:** verwendet die Konfigurationen aus keywords_config.json, um aus einer Sammlung von Webseiten lediglich die Artikel zu extrahieren, die eines oder mehrere der definierten Keywords enthalten. Das Ergebnis (Überschriften sofern verfügbar und URLs zu den Artikeln) kann in eine Textdatei geschrieben und/oder per Mail versendet werden. Das Skript kann eingesetzt werden, um aus aktuellen Nachrichten- und Pressemeldungen die Beiträge zu extrahieren, die für die Threat Intelligence zusätzlich relevant sind
 - **count_hits.py:** verwendet die Konfigurationen aus counts_config.json, um aus einer Liste von URLs auszuzählen, wie oft ein bestimmter Name oder ein bestimmtes Wort in den Ergebnissen gefunden wird. Es wird nur gezählt, auf wie vielen unterschiedlichen Seiten ein Wort auftaucht, nicht wie oft es auf ein und der selben Seite gefunden wird. Das Skript eignet sich insbesondere, um zu testen ob es öffentliche Mitteilungen über einen Sicherheitsvorfall bei einem (oder mehreren) bestimmten Unternehmen gibt. Der Code ist dahingehend optimiert, eine CSV-Datei anzulegen, die eine Tabelle mit drei Spalten enthält. In der ersten werden die Namen aus dem `hit`-Setting in alphabetischer Reihenfolge ausgegeben, in der zweiten Spalte ist die Anzahl der Treffer enthalten und in der dritten Spalte ist der Kontext, also die URL und die letzten 35 Zeichen vor dem Namen sowie die nächsten 35 Zeichen danach, enthalten
 - **get_contents.py:** verwendet die Konfigurationen aus contents_config.json, um den Inhalt der Webseiten in eine Textdatei zu schreiben. Es wird der komplette Text-Inhalt der Seite aus dem `body`- oder `main`-Tag in die Datei geschrieben, ohne HTML-Tags, JavaScript-Funktionen und Bilder. Header und Footer werden nicht extrahiert. Das Skript ist dazu vorgesehen, insbesondere aus Blog-Webseiten Text-Inhalte zu extrahieren und in der Datei abzulegen. Dadurch kann festgestellt werden, ob sich eine Seite seit dem letzten Aufruf geändert hat ohne die Seite im Browser zu öffnen

Beispiele für die Ergebnisdateien der mit der Standardkonfiguration ausgeführten Skripte befinden sich im Unterverzeichnis /assets/examples des Repositorys.

WICHTIG: Die Skripte verwenden Konfigurationsdateien, die eine schnelle und einfache Anpassung ermöglichen. Bevor die Skripte das erste mal ausgeführt werden, sollten die Konfigurationen überprüft und ggf. individuell geändert werden.</br>
Eine weitere Möglichkeit, die Skripte anzupassen und zu erweitern, ist in der Datei *Extensibility (en).md* beschrieben.

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

Diese Arbeit unterliegt den Bestimmungen einer
[Creative Commons Namensnennung 4.0 International-Lizenz][cc-by].

© 2023 Sandra Liedtke.

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by/4.0/deed.de
[cc-by-image]: https://licensebuttons.net/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

### Konfigurationsmöglichkeiten

Einige Konfigurationen sollten eventuell geändert werden, bevor das zugehörige Skript gestartet wird:
 - Um die Webseiten zu ändern, die durchsucht werden sollen, können in der `webpages`-Sektion Links hinzugefügt oder gelöscht werden
 - In articles_config können `stopwords` definiert werden, sodass Einträge, die diese Stopwords enthalten, nicht ins Ergebnis geschrieben werden
 - keywords_config enthält keine Stopword-Sektion, dafür können im `keywords`-Teil Schlüsselworte definiert werden, nach welchen gesucht werden soll. Nur Einträge, die diese Schlüsselworte enthalten werden ins Ergebnis geschrieben
 - In counts_config werden die Namen, deren Treffer gezählt werden sollen, in `hit` angegeben. Die Funktionsweise ist vergleichbar mit der Schlüsselwortsuche
 - Einige Webseiten haben viele Referenzlinks, die automatisch mit ins Ergebnis geschrieben werden, aber eigentlich nicht gebraucht werden. Dafür kann in der `specialHandling`-Sektion in articles_config definiert werden, unter welchen Umständen Links für diese Webseiten ins Ergebnis geschrieben werden sollen nach der Logik *"Entweder der Key ist nicht in der URL enthalten, oder die URL fängt mit dem Value an"*
 - `getDeltaRecords` definiert, ob alle Einträge der jeweiligen Webseiten ins Ergebnis geschrieben werden sollen oder nur diejenigen, die noch nicht in vorherigen Dateien auftauchen
     - HINWEIS: Das Delta-Update funktioniert nur, wenn ein Unterordner für die Ergebnisdateien angegeben wird. Es ist nicht verfügbar für count_hits
 - In `timeDelta4Delete` kann definiert werden, welche Dateien aufgehoben werden sollen. Die Löschfunktion sammelt alle Dateien ein, die älter sind als das Datum, das anhand des Zeitdeltas (in Tagen) errechnet wird. Nach Bestätigung auf der Kommandozeile werden die Dateien dann gelöscht.
 - In `controllerPort` kann definiert werden, welchen Quellport der Controller verwenden soll, welcher auf die Webseiten zugreift. Der Wert 0 legt fest, dass kein Controller verwendet werden soll.
     - HINWEIS: Der Controller wird lediglich für onion-Seiten benötigt und sollte daher **ausschließlich** für diese verwendet werden
 - In der `resultfile`-Sektion kann definiert werden, ob eine Datei mit den Ergebnissen erzeugt werden soll, wo diese gespeichert werden und wie sie heißen soll
     - HINWEIS: Wenn ein Ordnername angegeben wird, der noch nicht existiert, erzeugt das SKript den Ordner
 - In der counts_config können in `tableHeaders` die Überschriften für die auszugebende Tabelle definiert werden
 - Im `mailconfig`-Abschnitt kann angegeben werden, ob Mails gesendet werden sollen. In dem Fall muss auch ein SMTP-Server angegeben werden, von welchem aus die Mails versendet werden
 - Das Feld `destinationMailAddress` enthält die Empänger-Mailadresse
 - Die sendende Mail-Addresse, die sich am SMTP-Server authentifiziert, wird in `senderMailAddress` angegeben. Es ist empfehlenswert, hierfür eine komplett eigene Mail-Adresse zu erstellen anstatt einen existierenden Account zu verwenden, der auch für andere Dinge verwendet wird
     - HINWEIS: Das Passwort wird auf der Kommandozeile abgefragt während das Programm läuft und sollte **niemals** im Code oder in der Konfiguration gespeichert werden
 - In `mailSubject` kann dann noch der Betreff angegeben werden und in `placeholder` ein Text, der in der Mail enthalten ist, wenn es keine neuen Artikel gibt. Der Text aus `placeholder` wird auch in die Datei geschrieben, wenn es keine neuen Artikel gibt

### System-Anforderungen

 - Die Skripte wurden auf Windows und Linux getestet
 - Python 3.9 oder höher
 - Python Libraries, die ggf. separat installiert werden müssen:
     - beautifulsoup4
     - requests
     - stem
 - Wenn der Controller verwendet wird, muss der Computer sich mit dem TOR-Netzwerk verbinden können
 - Ein E-Mail Account, um die Ergebnisse per Mail versenden zu können und ein weiterer Account (oder eine Alias-Adresse), der die Mails empfängt (kann auch der gleiche sein)
 - Notepad++ um die Text-Dateien zu öffnen
 - Excel oder Libre Calc, um die CSV-Dateien öffnen zu können


## English Version

### Description

This repository contains a collection of scripts which have been developed for the usage in the context of cyber threat intelligence. However, the scripts may be used for other topics as well if the URLs and/or the keywords in the configuration files are changed. 
The following scripts are available:
 - **retrieve_article_links.py:** uses the configurations from articles_config.json to extract the newest articles from a collection of webpages, write them into a file and/or send them via mail. It will take all headlines (if available) and URLs of the articles, which do not contain any of the stopwords defined. The script is intended to be used for the collection of the latest entries from journals and therefore works as a customizable newsletter
 - **keyword_search.py:** uses the configurations from keywords_config.json to extract those articles from a collection of websites, which contain one or more of the keywords defined. The result (headlines if available and URLs of the articles) can be written into a text file and/or be sent via mail. The script can be used to collect the latest posts from news media, which may be additionally relevant for the threat intelligence
 - **count_hits.py:** uses the configurations from counts_config.json to count from a list of URLs how often a certain name or word is found in the results. It only counts on how many different pages the word is found, not how often it is found on the same webpage. The script is especially useful to check if there are public announcements about a security incident for one (or more) specific company. The code is optimized for creating a csv file containing a table with three columns. The first column contains the names from the `hit` setting in alphabethical order, the second one contains the count of the hits and the third contains the context, meaning the URL and the last 35 characters before the name as well as the next 35 characters after it
 - **get_contents.py:** uses the configurations from contents_config.json to write the contents of a webpage into a text file. The entire text content of the `body` or `main` tags are written to the file without the HTML tags, JavaScript functions and images. Header and footer are not extracted. The script can be used to extract the contents of a webpage, especially of blog websites. This way can be determined if a webpage`s content has changed since the last call without opening it in the browser

Examples for the result files of the scripts run with the default configuration can be found in the repository sub-directory /assets/examples.

IMPORTANT: Each of the scripts uses a configuration file which allows a fast and easy customization. Before the scripts are executed for the first time, the configuration settings should be checked and adjusted if necessary. </br>
Further options to adjust and extend the scripts are described in the file *Extensibility (en).md*.

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

© 2023 Sandra Liedtke.

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

### Configuration Options

There are some configurations that may be modified before running the related script:
 - To change the websites to be scraped, just add different links in the `webpages` section and/or remove existing links
 - In articles_config can be some `stopwords` defined to remove all entries which contain these stopwords
 - keywords_config does not contain a stopword section, but in the `keywords` part can be search words defined. Only entries containing these keywords will be kept in the result
 - In counts_config the names for which the hits should be count are given in `hit`. The functionality is comparable with the keyword search
 - Some websites may have many reference links embedded, which would be added to the result, but are actually not needed. For this the `specialHandling` section in articles_config defines under which circumstances those URLs should be added to the result following the logic *"Either the key is not contained in the URL, or the URL starts as given in the value"*
 - `getDeltaRecords` defines whether all entries currently displayed on the respective webpage should be kept or only those that are not yet listed in existing result files
     - HINT: The Delta-Update only works if a subfolder is given, where the result files are stored. It is not available for count_hits
 - `timeDelta4Delete` defines which files should be kept. The delete function collects all files which are older than the date calculated based on the time delta (in days). After confirmation on the command line, the files will be deleted.
 - In `controllerPort` can be defined which source port to use for the controller accessing the webpages. Value 0 defines that no controller should be used
     - HINT: The controller is only needed for scraping onion sites and hence, should be used **exclusively** for those
 - In the `resultfile` section can be defined whether a result file should be created, where it should be stored and how it should be named
     - HINT: If you give a folder name that is not yet existing, the script will create that respective folder
 - In counts_config can be table headers defined
 - In the `mailconfig` section can be defined whether mails should be sent. If so, also a SMTP-Server needs to be given, from which mails will be sent
 - The field `destinationMailAddress` contains the receiver's mail address
 - The sending mail address, which is also used to authenticate at the SMTP-Server, is given in `senderMailAddress`. Recommendation is to create a completely new mail account just for this purpose instead of using an existing address which is also used elsewhere
     - HINT: The password for the mail account is entered on the command line and should **never** be stored in the code or the configuration
 - In `mailSubject` can be the subject of the mail defined and in `placeholder` a text that will be contained in the mail body if there are no articles. The `placeholder` text is also written to the result file if there are no articles

### System Requirements

 - The scripts have been tested on Windows and Linux
 - Python 3.9 or higher
 - Python libraries which might need separate installation: 
     - beautifulsoup4
     - requests
     - stem
 - If the controller is used, the computer must be able to connect to the TOR-Network
 - A mail account for sending the result via mail and a mail account or alias-address receiving the result (may also be the same)
 - Notepad++ to open the resulting text files
 - Excel or Libre Calc to open the csv files