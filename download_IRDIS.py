#%%
import os
import re

def list_files(path):
    """
    Print the names of all files in path and its subdirectories.
    """
    list_of_files = []
    for root, _, files in os.walk(path):
        for file in files:
            list_of_files.append(file)
    return list_of_files

dir_left  = 'E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_LEFT/'
dir_right = 'E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_RIGHT/'

files_left  = list_files(dir_left)
files_right = list_files(dir_right)

#%%
download_script_left  = 'E:/ESO/Data/SPHERE/IRDIS_RAW/sphere_dl_script_left.sh'
download_script_right = 'E:/ESO/Data/SPHERE/IRDIS_RAW/sphere_dl_script_right.sh'

def files_to_download(download_script):
    with open(download_script, 'r') as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line.startswith('wget')] # list of entries that start with wget

def extract_filename(entries):
    # regular expression pattern to extract file name and download link
    pattern = r'\"(.*?)\".*\"(http.*?)\"'

    filenames = []
    folders   = []
    links     = []

    # loop through entries and extract file name and download link
    for entry in entries:
        result = re.search(pattern, entry)
        if result:
            file_path = result.group(1)
            link = result.group(2)

            filenames.append(os.path.basename(file_path))
            folders.append(os.path.dirname(file_path).split('/')[-1])
            links.append(link)

    return filenames, folders, links

#%%
filenames_right, folders_right, links_right = extract_filename(files_to_download(download_script_right))
filenames_left,  folders_left,  links_left  = extract_filename(files_to_download(download_script_left))

# ids_download_r = []
# for i,file in enumerate(filenames_right):
#     if file not in files_right:
#         ids_download_r.append(i)

# ids_download_l = []
# for i,file in enumerate(filenames_left):
#     if file not in files_left:
#         ids_download_l.append(i)


# %%
from pathlib import Path
import requests

root_r = Path('E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_RIGHT/')
root_l = Path('E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_LEFT/')

def download_missing_files(root, filenames, folders, links):
    for id in range(len(filenames)):
        folder = folders[id]
        link = links[id]
        filename = filenames[id]

        path_check = root.joinpath(folder).joinpath(filename)
        if not os.path.exists(path_check):
            if not os.path.exists(root.joinpath(folder)):
                print('Creating folder', folder)
                os.mkdir(root.joinpath(folder))
            print('Downloading file', filename)

            # Download the file
            response = requests.get(link, stream=True)
            with open(str(path_check), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)


download_missing_files(root_r, filenames_right, folders_right, links_right)
download_missing_files(root_l, filenames_left,  folders_left,  links_left)
