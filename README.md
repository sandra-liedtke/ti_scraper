# ti_scraper

Dieses Repository enthält ein Script, das verwendet werden kann, um die neuesten Artikel zu IT-Sicherheit in einer Datei zu sammeln und/oder per Mail zu verschicken. Das Script kann auch für andere Themen verwendet werden, wenn die URLs in der Konfigurationsdatei getauscht werden.

Einige Konfigurationen sollten eventuell geändert werden, bevor das Script gestartet wird:
 - Um die Webseiten zu ändern, die durchsucht werden sollen, können in der webpages-Sektion Links hinzugefügt oder gelöscht werden
 - Es können Stopwords definiert werden, sodass Einträge, die diese Stopwords enthalten, nicht ins Ergebnis geschrieben werden
 - getDeltaRecords definiert, ob alle Einträge der jeweiligen Webseiten ins Ergebnis geschrieben werden sollen oder nur diejenigen, die noch nicht in vorherigen Dateien auftauchen
     - HINWEIS: Das Delta-Update funktioniert nur, wenn ein Unterordner für die Ergebnisdateien angegeben wird
 - In der resultfile-Sektion kann definiert werden, ob eine Datei mit den Ergebnissen erzeugt werden soll, wo diese gespeichert werden und wie sie heißen soll
     - HINWEIS: Wenn ein Ordnername engegeben wird, der noch nicht existiert, erzeugt das Script den Ordner
 - Die weiteren Konfigurationen betreffen den Mailversand

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

Diese Arbeit unterliegt den Bestimmungen einer
[Creative Commons Namensnennung 4.0 International-Lizenz][cc-by].

© 2023 Sandra Liedtke

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by/4.0/deed.de
[cc-by-image]: https://licensebuttons.net/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg


## English Version:

This repository contains a script that can be used to collect the latest news on cyber security in a file and/or send them via mail, but can also be used for other topics.

There are some configurations that may be modified before running the script:
 - To change the websites to be scraped, just add different links in the webpages section and/or remove existing links
 - There can be some stopwords defined, to remove some entries which contain these stopwords
 - getDeltaRecords defines whether all entries currently displayed on the respective webpage should be kept or only those that are not yet listed in existing result files
     - HINT: The Delta-Update only works if a subfolder is given, where the result files are stored
 - In the resultfile section can be defined whether a result file should be created, where it should be stored and how it should be named
     - HINT: If you give a folder name that is not yet existing, the script will create that respective folder
 - There are also some configurations for sending the result via mail

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

© 2023 Sandra Liedtke

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
