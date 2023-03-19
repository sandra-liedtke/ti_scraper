# Extensibility

Some of the scripts of the TI Scaper are currently not run on a regular basis as they are not needed most of the time. They have been developed in advance, because **when** they are needed, they are probably needed **immediately** without having the time to develop them then. However, not all scenarios are covered and it might be necessary to create a new script in short time for an individual case that was not considered so far. </br>
Therefore the available scripts of the TI Scraper can be easily extended as the code of the files in the scripts/lib folder is used by all of the scripts and therefore has been optimized and tested already. This also means that changes done in the commons.py or regex.py affect many or all of the scripts. Of course you can also extend the scripts any time for any scenario, even if there is no time pressure.

To extend the existing scripts, follow the below steps:

> 1. Identify the script which comes closest to what you want to achieve with the new script and copy it. Paste it in the scripts folder and rename it
> 2. In the config folder, copy, paste and rename the related *_config.json
> 3. In scripts/lib/commons.py go the the if statement starting in line 22 and copy and paste one of the `elif`-Statements. Change the `APP_NAME` to the name of the new python script and the `config_file_name` to the new config.json.</br>
  Elif-statement to copy: </br>
>  ```python
elif APP_NAME == 'NEW_SCRIPT_NAME.py':
    config_file_name = '../config/NEW_CONFIG_JSON_NAME.json'
```
> 4. Open the newly created script and config and modify them accordingly. There are per default only two functions that may require modification while all others are called in the `main()` function from lib folder
>   - In `main()` function, check which other functions should be called. Also check the `print()` statements, especially the script start print
>   - In `clean_webpages()`, check which content should be extracted from the called websites
>   - In `format_result()`, define the format of the output. Based on the formatting here, you may also define the best file format to be created like .txt or .csv. The file ending itself is then defined in the config file, `resultfile` section