import datetime
import os
from lib.commons import CONFIG
import ssl
import demisto_client
import demisto_client.demisto_api
from demisto_client.demisto_api.rest import ApiException
import json

# URL and API of the Cortex
BASE_URL = CONFIG['profiling']['CortexXSOARAPIConfig']['host']
if not BASE_URL == '':
    api_instance = demisto_client.configure(base_url=BASE_URL, debug=False, verify_ssl=ssl.CERT_NONE,
                                        api_key=CONFIG['profiling']['CortexXSOARAPIConfig']['api_key'])


def create_new_indicator(entry, name):
    # create new indicator if it could not be found - type is always threat actor, articles are added
    ioc_object = {
        "indicator": {
            "CustomFields": {"communitynotes": [{"notes": str(entry).replace('\n', ': '), "timestamp": datetime.datetime.now()}],
                             "aliases": [name],
                             },
            "indicator_type": "Threat Actor",
            "last_seen": datetime.datetime.now(),
            "value": name
        }
    }
    try:
        api_response = api_instance.indicators_create(ioc_object=ioc_object)
        print(api_response)
        print(
            "The new record has been created in the Cortex XSOAR Application. Please add further details of the record manually as the TI Scraper creates a record with very basic information only")
    except ApiException as e:
        print(e)
        print("Error while writing " + name + " to Cortex XSOAR")


# API Request to Cortex XSOAR
def send_api_request(curr_updt_value, indicator_name):
    try:
        # search current record in Cortex
        indicator_filter = demisto_client.demisto_api.IndicatorFilter()
        indicator_filter.query = CONFIG['profiling']['CortexXSOARAPIConfig'][
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
            ioc_object.custom_fields['communitynotes'].append({'notes': curr_updt_value.replace('\n', ': '), "timestamp": datetime.datetime.now()})
            # the actual API-Request
            try:
                api_response = api_instance.indicators_edit(ioc_object=ioc_object)
                print(api_response)
            except ApiException as e:
                print(e)
                print("Error while writing " + indicator_name + " to Cortex XSOAR")
        elif found_indicator.total == 0:
            # indicator does not exist -> let user chose to create it
            try:
                create_indicator = input(
                    "The requested Indicator with value " + indicator_name + " could not be found. Want to create it now [y/n]? ")
                if create_indicator.upper() == "YES" or create_indicator.upper() == "Y":
                    create_new_indicator(curr_updt_value, indicator_name)
            except Exception as e:
                print(e)
                print("Cannot update or create record " + indicator_name + " for an unknown reason")
        else:
            # If more than one indicator is found it must be handled manually
            print(
                "Found more than one indicator with filter " + indicator_filter.query + "! Please check indicators in Cortex XSOAR")
            print("Skipping update in Cortex XSOAR for " + indicator_name)
    except ApiException as e:
        print(e)
        print("Skipping XSOAR Profiling for " + indicator_name)


# add records to the respective file or Cortex entry for tracing/profiling
def profiling_records(records):
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

        aliases_to_check = CONFIG['profiling']['profileData']
        for alias in existing_aliases:
            aliases_to_check.append(str(alias))
        for entry in aliases_to_check:

            # write profile files to folder
            if CONFIG['profiling']['profile2file'] == True:
                print("Adding " + str(entry) + " to file...")
                # check if the directory folder exists
                if not os.path.exists('../' + CONFIG['profiling']['profileFolderName']):
                    os.makedirs('../' + CONFIG['profiling']['profileFolderName'])

                # profiling file does not yet exist and needs to be created
                if not os.path.exists('../' + CONFIG['profiling']['profileFolderName'] + '/' + entry + '_profile.txt'):
                    with open('../' + CONFIG['profiling']['profileFolderName'] + '/' + entry + '_profile.txt', 'w', encoding='utf-8') as profile_file:
                        for new_rec in records:
                            if entry.upper() in new_rec.upper().replace(' ', ''):
                                profile_file.write('\n\n' + new_rec)

                else:
                    # profiling file exists and needs to be updated with the new record
                    with open('../' + CONFIG['profiling']['profileFolderName'] + '/' + entry + '_profile.txt', 'a', encoding='utf-8') as profile_file:
                        for new_rec in records:
                            if entry.upper() in new_rec.upper().replace(' ', ''):
                                profile_file.write('\n\n' + new_rec)

            # Cortex XSOAR Integration
            if CONFIG['profiling']['profile2cortex'] == True:
                print("Adding records for profile " + str(entry) + " to Cortex XSOAR...")
                for new_rec in records:
                    if entry.upper() in new_rec.upper().replace(' ', '').replace('-', ''):
                        send_api_request(new_rec, entry.replace(' ', ''))