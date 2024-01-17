import json
import ssl
import demisto_client.demisto_api
from demisto_client.demisto_api.rest import ApiException
from lib.commons import CONFIG


def update_aliases():

    # api instance
    api_instance = demisto_client.configure(base_url=CONFIG['profiling']['CortexXSOARAPIConfig']['host'], debug=False,
                                            verify_ssl=ssl.CERT_NONE,
                                            api_key=CONFIG['profiling']['CortexXSOARAPIConfig']['api_key'])

    # list collecting the aliases
    missing_aliases = []
    # for each profileData entry
    for indicator_name in CONFIG['profiling']['profileData']:
        try:
            # search current record in Cortex
            indicator_filter = demisto_client.demisto_api.IndicatorFilter()
            indicator_filter.query = 'aliases:"' + indicator_name + '"'
            found_indicator = api_instance.indicators_search(indicator_filter=indicator_filter)
            # write those aliases into a list which are not equal to the entry in the config
            if found_indicator.total > 0:
                print("Checking aliases for indicator " + indicator_name)
                for alias in found_indicator.ioc_objects[0]['CustomFields']['aliases']:
                    if alias not in CONFIG['profiling']['profileData'] and alias not in missing_aliases:
                        missing_aliases.append(alias)
        # catch exceptions
        except ApiException as e:
            print(e)
            print("Cannot collect aliases. Aborting...")

    # remove those which are available in config with different case letters
    for collected_alias in missing_aliases:
        for indicator in CONFIG['profiling']['profileData']:
            if collected_alias.upper() == indicator.upper():
                missing_aliases.remove(collected_alias)

    # create the file
    with open('../config/cortex_aliases.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(missing_aliases))

