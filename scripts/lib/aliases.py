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
    for config_profile in CONFIG['profiling']['profileData']:
        try:
            # search current record in Cortex
            indicator_filter = demisto_client.demisto_api.IndicatorFilter()
            indicator_filter.query = 'aliases:"' + config_profile + '"'
            found_indicator = api_instance.indicators_search(indicator_filter=indicator_filter)
            # write the aliases into a list
            if found_indicator.total == 1:
                print("Checking aliases for indicator " + config_profile)
                for cortex_alias in found_indicator.ioc_objects[0]['CustomFields']['aliases']:
                    if not cortex_alias.upper() == config_profile.upper():
                        if not cortex_alias.upper() in str(missing_aliases).upper():
                            missing_aliases.append(cortex_alias)
        # catch exceptions
        except ApiException as e:
            print(e)
            print("Cannot collect aliases. Aborting...")

    # create the new aliases file
    with open('../config/cortex_aliases.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(list(set(missing_aliases))))

