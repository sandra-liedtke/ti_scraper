# TI Scraper

*English Version Below*

Dieses Repository enthält ein Script, das verwendet werden kann, um die neuesten Artikel zu IT-Sicherheit in einer Datei zu sammeln und/oder per Mail zu verschicken. Das Script kann auch für andere Themen verwendet werden, wenn die URLs in der Konfigurationsdatei getauscht werden.

Einige Konfigurationen sollten eventuell geändert werden, bevor das Script gestartet wird:
 - Um die Webseiten zu ändern, die durchsucht werden sollen, können in der webpages-Sektion Links hinzugefügt oder gelöscht werden
 - Es können Stopwords definiert werden, sodass Einträge, die diese Stopwords enthalten, nicht ins Ergebnis geschrieben werden
 - Einige Webseiten haben viele Referenzlinks, die automatisch mit ins Ergebnis geschrieben werden, aber eigentlich nicht gebraucht werden. Dafür kann in der specialHandling-Sektion definiert werden, unter welchen Umständen Links für diese Webseiten ins Ergebnis geschrieben werden sollen nach der Logik *"Entweder der Key ist nicht in der URL enthalten, oder die URL fängt mit dem Value an"*
 - getDeltaRecords definiert, ob alle Einträge der jeweiligen Webseiten ins Ergebnis geschrieben werden sollen oder nur diejenigen, die noch nicht in vorherigen Dateien auftauchen
     - HINWEIS: Das Delta-Update funktioniert nur, wenn ein Unterordner für die Ergebnisdateien angegeben wird
 - In timeDelta4Delete kann definiert werden, welche Dateien aufgehoben werden sollen. Die Löschfunktion sammelt alle Dateien ein, die älter sind als das Datum, das anhand des Zeitdeltas (in Tagen) errechnet wird. Nach Bestätigung auf der Kommandozeile werden die Dateien dann gelöscht.
 - In controllerPort kann definiert werden, auf welchen Port der Controller gesetzt werden soll, welcher auf die Webseiten zugreift. Der Wert 0 legt fest, dass kein Controller verwendet werden soll.
 - In der resultfile-Sektion kann definiert werden, ob eine Datei mit den Ergebnissen erzeugt werden soll, wo diese gespeichert werden und wie sie heißen soll
     - HINWEIS: Wenn ein Ordnername angegeben wird, der noch nicht existiert, erzeugt das Script den Ordner
 - Im mailconfig-Abschnitt kann angegeben werden, ob Mails gesendet werden sollen. In dem Fall muss auch ein SMTP-Server angegeben werden, von welchem aus die Mails versendet werden
 - Das Feld destinationMailAddress enthält die Empänger-Mailadresse
 - Die sendende Mail-Addresse, die sich am SMTP-Server authentifiziert, wird in senderMailAddress angegeben. Es ist empfehlenswert, hierfür eine komplett eigene Mail-Adresse zu erstellen anstatt einen existierenden Account zu verwenden, der auch für andere Dinge verwendet wird
     - HINWEIS: Das Passwort wird auf der Kommandozeile abgefragt während das Programm läuft und sollte **niemals** im Code oder in der Konfiguration gespeichert werden
 - In mailSubject kann dann noch der Betreff angegeben werden und in placeholder ein Text, der in der Mail enthalten ist, wenn es keine neuen Artikel gibt

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

Diese Arbeit unterliegt den Bestimmungen einer
[Creative Commons Namensnennung 4.0 International-Lizenz][cc-by].

© 2023 Sandra Liedtke.

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by/4.0/deed.de
[cc-by-image]: https://licensebuttons.net/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg


## English Version:

This repository contains a script that can be used to collect the latest news on cyber security in a file and/or send them via mail, but can also be used for other topics.

There are some configurations that may be modified before running the script:
 - To change the websites to be scraped, just add different links in the webpages section and/or remove existing links
 - There can be some stopwords defined, to remove some entries which contain these stopwords
 - Some websites may have many reference links embedded, which would be added to the result, but are actually not needed. For this the specialHandling section defines under which circumstances those URLs should be added to the result following the logic *"Either the key is not contained in the URL, or the URL starts as given in the value"*
 - getDeltaRecords defines whether all entries currently displayed on the respective webpage should be kept or only those that are not yet listed in existing result files
     - HINT: The Delta-Update only works if a subfolder is given, where the result files are stored
 - timeDelta4Delete defines which files should be kept. The delete function collects all files which are older than the date calculated based on the time delta (in days). After confimration on the command line, the files will be deleted.
 - In controllerPort can be defined which port to use for the controller accessing the webpages. Value 0 defines that no controller should be used.
 - In the resultfile section can be defined whether a result file should be created, where it should be stored and how it should be named
     - HINT: If you give a folder name that is not yet existing, the script will create that respective folder
 - In the mailconfig section can be defined whether mails should be sent. If so, also a SMTP-Server needs to be given, from which mails will be sent
 - The field destinationMailAddress contains the receiver's mail address
 - The sending mail address, which is also used to authenticate at the SMTP-Server, is given in senderMailAddress. Recommendation is to create a completely new mail address just for this purpose instead of using an existing address which is also used elsewhere
     - HINT: The password for the mail account is entered on the command line and should **never** be stored in the code or the configuration
 - In mailSubject can be the subject of the mail defined and in placeholder a text that will be contained in the mail body if there are no articles

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

© 2023 Sandra Liedtke.

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
