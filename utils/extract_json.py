import os
import pathlib
import shutil
from datetime import datetime

input_dir = '/home/chriss/Nextcloud/Hochschule_Rosenheim/Master/Masterarbeit/secret_scanner_prototyp/backend/test/git_leaks_github_logs_v2'
output_dir = '/home/chriss/Nextcloud/Hochschule_Rosenheim/Master/Masterarbeit/secret_scanner_prototyp/backend/test/output'

# scans all directories in input_dir recursively and copies them under a new name to output_dir
if __name__ == '__main__':
    for current_path, folders, files in os.walk(input_dir):
        for file in files:
            file_name = '{}__{}'.format(datetime.today().strftime('%Y-%m-%d'), file)
            print(os.path.join(current_path, file) + " --> " + file_name)
            shutil.copy(os.path.join(current_path, file), os.path.join(output_dir, file_name))

