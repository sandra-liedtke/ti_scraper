# Integration of Profiling Data into Palo Alto Cortex® XSOAR

The articles related to the `profileData` setting - those articles containing the mentioned names in the title or the link - can either be collected in text files or they can be integrated into Cortex XSOAR. For this only the base url to the hosted Cortex XSOAR must be given in the `CortexXSOARAPIConfig - host` setting. In the `api_key`, the key to be used for authorization must be given. It can be generated in Cortex XSOAR in *Settings - Integrations - API Keys*.<br/>
To fully use the REST API of XSOAR, the application should have the *Core REST API* instance enabled. This can be done in *Settings - Integrations - Instances*.

![Necessary Integration Instances](/assets/images/XSOAR/rest_api.png "Necessary Integration Instances")

If articles related to a new name should be collected from now on, it must only be added to the `profileData`. Once the TI Scraper finds an article for profiling but does not find the entry in Cortex XSOAR, it will offer to create a very basic record with only the indicator value, type and the articles added as community notes. It will always create the record as a "Threat Actor" type, however, this setting can still be changed manually once the record is created. In most cases there is a necessity to also add further details (like threat actor classification, malware type, VirusTotal links, ...) manually directly in the Cortex XSOAR application.

![Terminal Text for newly created record](/assets/images/XSOAR/terminal_new_record.png "Terminal Text for newly created record")

![Newly Created Record in Cortex XSOAR](/assets/images/XSOAR/new_record.png "Newly created record in PA Cortex XSOAR")

The Terminal will also print the response of the API-Request. <br/>
The article entries are added to the newly created or already existing XSOAR-Record into the "Community Notes" as a new note for each article.

![Records of the APT entry](/assets/images/XSOAR/added_records.png "Records of the APT entry in PA Cortex XSOAR")

The *Value* of the new record will always be the name given in the `profiling - profileData` setting. The same will also be written to the "Aliases" custom field. As there might be several aliases for the same record (many threat actors or malware are tracked under different names), the [aliases.py](/scripts/lib/aliases.py) script extracts all aliases from Cortex which are not available in the config file and writes them into a newly created json file named *cortex_aliases.json* in the config folder. The next time the TI Scraper is executed, it will also check for the aliases if any of them appears in the articles and if so, it will add that record to the profile in Cortex.
If the names given as `profileData` should be written into a different field, the code must be changed in the [profiling.py](/scripts/lib/profiling.py) file, line 18. However, a `value` for the Cortex XSOAR record **must** be given, otherwise the record will still be created, but is actually not useable. So it is recommended to - instead delete the line - just add the new field where the `profileData` entries should be written to. <br/>
The filter to find the record once it exists can be set in the config in `profiling - CortexXSOARAPIConfig - search_field`. The values of the field name given here must match the entries from `profileData` to generate the search query.<br/>
The [cortex_helper Repository](https://github.com/sandra-liedtke/cortex_helper) contains additional scripts that can be run separately to batch-update the records in Cortex XSOAR after their creation. Scripts from there can be easily integrated with the TI Scraper as a subfolder of the [scripts](/scripts/) directory.<br/><br/>
Further information on the Palo Alto Cortex XSOAR Application can be found on the [Palo Alto website](https://www.paloaltonetworks.com/resources/datasheets/cortex-xsoar-overview). Technical details on the API integration can be found in the [docu](https://docs.paloaltonetworks.com/develop/api#sort=relevancy&layout=card&numberOfResults=25).