import os
from lib.commons import CONFIG


# archive records to the respective file
def archive_records(records):
    # if records are available
    if not str(records) == '':
        records = str(records).split('\n\n')
        archive = ''
        for entry in CONFIG['archivedData']:
            # check if the archival folder exists
            if not os.path.exists('../' + CONFIG['archiveFolderName']):
                os.makedirs('../' + CONFIG['archiveFolderName'])
            if not os.path.exists('../' + CONFIG['archiveFolderName'] + '/' + entry + '_archive.txt'):
                # archival file does not yet exist and needs to be created
                with open('../' + CONFIG['archiveFolderName'] + '/' + entry + '_archive.txt', 'w', encoding='utf-8') as archive_file:
                    for new_rec in records:
                        if entry in new_rec:
                            archive += '\n\n' + new_rec
                    archive_file.write(str(archive))

            else:
                # archival file exists and needs to be appended
                with open('../' + CONFIG['archiveFolderName'] + '/' + entry + '_archive.txt', 'a', encoding='utf-8') as archive_file:
                    for new_rec in records:
                        if entry in new_rec:
                            archive_file.write('\n\n' + new_rec)
