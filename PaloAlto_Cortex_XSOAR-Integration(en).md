# Integration of Archival Data into Palo Alto Cortex® XSOAR

The articles related to the `archivedData` setting - those articles containing the mentioned keywords in the title or the link - can either be archived in text files or they can be integrated into Cortex XSOAR. For this only the base url to the hosted Cortex XSOAR must be given in the `CortexXSOARAPIConfig - host` setting. In the api_key, the key to be used for authorization must be given. It can be generated in Cortex XSOAR in *Settings - Integrations - API Keys*.<b/r><br/>
To fully use the REST API of XSOAR, the application should have the *Core REST API* instance enabled. This can be done in *Settings - Integrations - Instances*.

![Necessary Integration Instances](/assets/images/XSOAR/rest_api.png "Necessary Integration Instances")

If a new entry should be archived from now on, it must only be added to the `archivedData`. Once the TI Scraper finds an article for archiving but does not find the entry in Cortex XSOAR, it will offer to create a very basic record with only the indicator value, type and the articles added as community notes. It will always create the record as a "Threat Actor" type, however, this value can still be changed manually once the record is created. In most cases there is a necessity to also add further details manually directly in the Cortex XSOAR application.

![Terminal Text for new created record](/assets/images/XSOAR/terminal_new_record.png "Terminal Text for new created record")

![Newly Created Record in Cortex XSOAR](/assets/images/XSOAR/new_record.png "Newly created record in PA Cortex XSOAR")

The Terminal will also print the response of the API-Request. <br/>
The article entries are added to the newly created or already existing XSOAR-Record into the "Community Notes" as a new note for each article.

![Records of the "APT" entry](/assets/images/XSOAR/added_records.png "Records of the "APT" entry in PA Cortex XSOAR")

The value of the new record will always be the name given in the `archiving - archivedData` setting. If the names given as `archivedData` should be written into a different field, the code must be changed in the [archiver.py](/scripts/lib/archiver.py) file, line 18. However, a `value` for the Cortx XSOAR record **must** be given, otherwise the record will still be created, but is actually not useable. So it is recommended to - instead delete the line - just add the new field where the `archivedData` entries should be written to. <br/>
The filter to find the record once it exists can be set in the config in `archiving - CortexXSOARAPIConfig - search_field`. The values of the field name given here must match the entries from `archivedData` to generate the search query.
Further information on the Palo Alto Cortex XSOAR Application can be found on the [Palo Alto website](https://www.paloaltonetworks.com/resources/datasheets/cortex-xsoar-overview). Technical details on the API integration can be found in the [docu](https://docs.paloaltonetworks.com/develop/api#sort=relevancy&layout=card&numberOfResults=25).