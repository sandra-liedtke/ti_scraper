print('''
########################################################################################################################
      
\tThis script adds a date as firstSeen for each of the indicator entries in XSOAR that has been created by the 
\tTI Scraper. 
\tThis script can run immediately after the new indicators have been created. The TI Scraper cannot add a firstSeen 
\tDate when creating the entry, hence need to update it afterwards.
\n\tThe configuration file is the same as used for the retrieve_article_links.py.

\t(c) 2023 Sandra Liedtke.
                                                                                                          
########################################################################################################################
''')
import json
import ssl
import demisto_client
import demisto_client.demisto_api
from demisto_client.demisto_api.rest import ApiException


# get config
with open('../../config/articles_config.json', 'r') as config_file:
    CONFIG = json.load(config_file)

# api instance
api_instance = demisto_client.configure(base_url=CONFIG['archiving']['CortexXSOARAPIConfig']['host'], debug=False, verify_ssl=ssl.CERT_NONE, api_key=CONFIG['archiving']['CortexXSOARAPIConfig']['api_key'])

# for each archivedData entry
for indicator_name in CONFIG['archiving']['archivedData']:
    try: 
        print("Checking " + indicator_name + " in Cortex XSOAR")
        # search current record in Cortex
        indicator_filter = demisto_client.demisto_api.IndicatorFilter()
        indicator_filter.query = 'value:"' + indicator_name + '"'
        found_indicator = api_instance.indicators_search(indicator_filter=indicator_filter)
        if found_indicator.total == 1:
            # indicator exists -> update it
            print("Found indicator " + indicator_name + " in Cortex. Updating with current datetime values...")
            ioc_object = demisto_client.demisto_api.IocObject(found_indicator.ioc_objects[0])
            # Mapping of existing values
            ioc_object.custom_fields = found_indicator.ioc_objects[0]['CustomFields'] 
            ioc_object.calculated_time = found_indicator.ioc_objects[0]['calculatedTime']
            # correct firstSeen: should be same as the timestamp automatically set when the record was created
            ioc_object.first_seen = found_indicator.ioc_objects[0]['timestamp']
            ioc_object.first_seen_entry_id = found_indicator.ioc_objects[0]['firstSeenEntryID']
            ioc_object.id = found_indicator.ioc_objects[0]['id']
            ioc_object.indicator_type = found_indicator.ioc_objects[0]['indicator_type']
            ioc_object.last_seen = found_indicator.ioc_objects[0]['lastSeen']
            ioc_object.last_seen_entry_id = found_indicator.ioc_objects[0]['lastSeenEntryID']
            ioc_object.modified = found_indicator.ioc_objects[0]['modified']
            ioc_object.score = found_indicator.ioc_objects[0]['score']
            ioc_object.sort_values = found_indicator.ioc_objects[0]['sortValues']
            ioc_object.timestamp = found_indicator.ioc_objects[0]['timestamp']
            ioc_object.value = found_indicator.ioc_objects[0]['value']
            ioc_object.version = found_indicator.ioc_objects[0]['version']
            # the actual API-Request
            try:
                api_response = api_instance.indicators_edit(ioc_object=ioc_object)
            except ApiException as e:
                print("Error while writing " + indicator_name + " to Cortex XSOAR")
                print(e)
        else:
            # entry is either not available in Cortex or it exists more than once
            print("Skipping indicator with name " + indicator_name + "...")
    # catch exceptions
    except ApiException as e:
        print(e)
        print("Skipping XSOAR Archiving for " + indicator_name)
