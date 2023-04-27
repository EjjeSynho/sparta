#%%
%load_ext autoreload
%autoreload 2

from plot_sparta_data_2 import retrieve_ESO_files, decompress_files, plot_sparta_data_2
from pathlib import Path
from tqdm import tqdm
import datetime
import os
import re

#%% ------------------- Get the list of all the required nights -------------------
IRDIS_folders_L = Path('E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_LEFT')
IRDIS_folders_R = Path('E:/ESO/Data/SPHERE/IRDIS_RAW/SPHERE_DC_DATA_RIGHT')

def count_nights(IRDIS_folders):
    timestamps = []
    datetime_format = f'%Y-%m-%dT%H.%M.%S.%f'
    regex = r"(\d{4}-\d{2}-\d{2}T\d{2}\.\d{2}\.\d{2}\.\d{3})"

    # Get all timestamps in the IRDIS dataset
    for folder in os.listdir(IRDIS_folders):
        timestamps += [datetime.datetime.strptime(re.search(regex, file).group(1), datetime_format) for file in os.listdir(os.path.join(IRDIS_folders, folder))]

    print('Total number of files in the', str(IRDIS_folders)+':', len(timestamps))
    # Add one day to the timestamps to make sure we get all the data
    timestamps = timestamps + \
                [stamp - datetime.timedelta(days=1) for stamp in timestamps] + \
                [stamp + datetime.timedelta(days=1) for stamp in timestamps]

    nights = list(set([stamp.strftime("%Y-%m-%d") for stamp in timestamps]))
    nights.sort()
    return nights

nights = list(set(count_nights(IRDIS_folders_L) + count_nights(IRDIS_folders_R)))

print('Total number of nights to download: ', len(nights))

#%% Get the list of the missing nights
missing_nights = []
for night in nights:
    if not os.path.exists('E:/ESO/Data/SPHERE/SPARTA_RAW_compressed/'+night):
        missing_nights.append(night)

print('Total number of missing nights: ', str(len(missing_nights))+'/'+str(len(nights)))
nights = missing_nights

#%% ------------------- Download the raw ESO files from the archive -------------------
compressed_folder = Path('E:/ESO/Data/SPHERE/SPARTA_RAW_compressed/')
for night in nights:
    retrieve_ESO_files('akuznets', night=night, files=None, prog_id=None, local_path=compressed_folder, verbose=True)

#%% ------------------- Decompress the raw downloaded ESO files -------------------
decompressed_folder = Path('E:/ESO/Data/SPHERE/SPARTA_RAW/')
decompress_files(compressed_folder, decompressed_folder)

#%% ------------------- Convert the decompressed headers into the readable telemetry -------------------
decompressed_folder = Path('E:/ESO/Data/SPHERE/SPARTA_RAW')
telemetry_output = Path('E:/ESO/Data/SPHERE/DTTS')

for night in tqdm(os.listdir(decompressed_folder)):
    print(night)
    path_input = os.path.join(decompressed_folder, night)

    if not os.path.exists(telemetry_output.joinpath(night)):
        decompressed_files = [os.path.join(path_input, f) for f in os.listdir(path_input)]
        plot_sparta_data_2(telemetry_output.joinpath(night), decompressed_files, plot=False, verbose=True)


#%% ------------------- Delete empty folders -------------------
# Delete empty folders
for night in os.listdir(telemetry_output):
    if len(os.listdir(os.path.join(telemetry_output, night))) == 0:
        os.rmdir(os.path.join(telemetry_output, night))
        print('Removed:', night)

# %%
