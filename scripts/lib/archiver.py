import datetime
import os
from lib.commons import CONFIG
import ssl
import demisto_client
import demisto_client.demisto_api
from demisto_client.demisto_api.rest import ApiException
import json

BASE_URL = CONFIG['archiving']['CortexXSOARAPIConfig']['host']
api_instance = demisto_client.configure(base_url=BASE_URL, debug=False, verify_ssl=ssl.CERT_NONE,
                                        api_key=CONFIG['archiving']['CortexXSOARAPIConfig']['api_key'])

def create_new_indicator(entry, name):
    ioc_object = {
        "indicator": {
            "CustomFields": {"communitynotes": [{"notes": str(entry).replace('\n', ': ')}],
                             "aliases": [name],
                             },
            "indicator_type": "Threat Actor",
            "last_seen": datetime.datetime.now(),
            "value": name
        }
    }
    api_response = api_instance.indicators_create(ioc_object=ioc_object)
    print(api_response)
    print(
        "The new record has been created in the Cortex XSOAR Application. Please add further details of the record manually as the TI Scraper creates a record with very basic information only")


# API Request to Cortex XSOAR
def send_api_request(curr_updt_value, indicator_name):
    try:
        # search current record in Cortex
        indicator_filter = demisto_client.demisto_api.IndicatorFilter()
        indicator_filter.query = CONFIG['archiving']['CortexXSOARAPIConfig'][
                                     'search_field'] + ':"' + indicator_name + '"'
        found_indicator = api_instance.indicators_search(indicator_filter=indicator_filter)
        if found_indicator.total == 1:
            # indicator exists -> update it
            ioc_object = demisto_client.demisto_api.IocObject(found_indicator.ioc_objects[0])
            # Mapping of existing values
            ioc_object.custom_fields = found_indicator.ioc_objects[0]['CustomFields']
            ioc_object.calculated_time = found_indicator.ioc_objects[0]['calculatedTime']
            ioc_object.first_seen = found_indicator.ioc_objects[0]['firstSeen']
            ioc_object.first_seen_entry_id = found_indicator.ioc_objects[0]['firstSeenEntryID']
            ioc_object.id = found_indicator.ioc_objects[0]['id']
            ioc_object.indicator_type = found_indicator.ioc_objects[0]['indicator_type']
            ioc_object.last_seen = datetime.datetime.now()
            ioc_object.last_seen_entry_id = found_indicator.ioc_objects[0]['lastSeenEntryID']
            ioc_object.modified = found_indicator.ioc_objects[0]['modified']
            ioc_object.score = found_indicator.ioc_objects[0]['score']
            ioc_object.sort_values = found_indicator.ioc_objects[0]['sortValues']
            ioc_object.timestamp = found_indicator.ioc_objects[0]['timestamp']
            ioc_object.value = found_indicator.ioc_objects[0]['value']
            ioc_object.version = found_indicator.ioc_objects[0]['version']
            # enter the current article as a new Community Note
            ioc_object.custom_fields['communitynotes'].append({'notes': curr_updt_value.replace('\n', ': ')})
            # the actual API-Request
            try:
                api_response = api_instance.indicators_edit(ioc_object=ioc_object)
                print(api_response)
            except ApiException as e:
                print("Error while writing " + indicator_name + " to Cortex XSOAR")
                print(e)
        elif found_indicator.total == 0:
            # indicator does not exist -> let user chose to create it
            try:
                create_indicator = input(
                    "The requested Indicator with value " + indicator_name + " could not be found. Want to create it now (Yes,No)? ")
                if create_indicator.upper() == "YES" or create_indicator.upper() == "Y":
                    create_new_indicator(curr_updt_value, indicator_name)
            except Exception as ex:
                print("Cannot update or create record " + indicator_name + " for an unknown reason")
                print(ex)
        else:
            # If more than one indicator is found it must be handled manually
            print(
                "Found more than one indicator with filter " + indicator_filter.query + "! Please check indicators in Cortex XSOAR")
            print("Skipping update in Cortex XSOAR for " + indicator_name)
    except ApiException as e:
        print(e)
        print("Skipping XSOAR Archiving for " + indicator_name)


# archive records to the respective file
def archive_records(records):
    # if records are available
    if not str(records) == '':
        records = str(records).split('\n\n')
        archive = ''
        if not os.path.exists('../config/cortex_aliases.json'):
            print(
                "Could not find file cortex_aliases.json in config directory. Continuing with values from config file only...")
            existing_aliases = []
        else:
            with open('../config/cortex_aliases.json', 'r') as alias_file:
                existing_aliases = json.load(alias_file)

        aliases_to_check = CONFIG['archiving']['archivedData']
        for alias in existing_aliases:
            aliases_to_check.append(str(alias))
        for entry in aliases_to_check:
            # write archiving files in folder
            if CONFIG['archiving']['archive2file'] == True:
                print("Archiving " + str(entry) + " to file...")
                # check if the archival folder exists
                if not os.path.exists('../' + CONFIG['archiving']['archiveFolderName']):
                    os.makedirs('../' + CONFIG['archiving']['archiveFolderName'])
                if not os.path.exists('../' + CONFIG['archiving']['archiveFolderName'] + '/' + entry + '_archive.txt'):
                    # archival file does not yet exist and needs to be created
                    with open('../' + CONFIG['archiving']['archiveFolderName'] + '/' + entry + '_archive.txt', 'w',
                              encoding='utf-8') as archive_file:
                        for new_rec in records:
                            if entry.upper() in new_rec.upper().replace(' ', ''):
                                archive_file.write('\n\n' + new_rec)
                else:
                    # archival file exists and needs to be appended
                    with open('../' + CONFIG['archiving']['archiveFolderName'] + '/' + entry + '_archive.txt', 'a',
                              encoding='utf-8') as archive_file:
                        for new_rec in records:
                            if entry.upper() in new_rec.upper().replace(' ', ''):
                                archive_file.write('\n\n' + new_rec)
            # Cortex XSOAR Integration
            if CONFIG['archiving']['archive2cortex'] == True:
                print("Archiving " + str(entry) + " to Cortex XSOAR...")
                for new_rec in records:
                    if entry.upper() in new_rec.upper().replace(' ', ''):
                        send_api_request(new_rec, entry.replace(' ', ''))
