import os
from mp_query import tmo_materials
from mp_vasp import get_vasp_files


if __name__ == '__main__':
    API_KEY = 'PdW5vD8eTQ1unzyw'
    DRIVER_PATH = './chromedriver'
    DOWNLOAD_PATH = '/Users/schuylerkrawczuk/Downloads/'

    results = tmo_materials(n_most_stable=1, rows=[4], n_elements=3, api_key=API_KEY)
    zipfiles, failed = get_vasp_files(results, download_path=DOWNLOAD_PATH, driver_path=DRIVER_PATH)

    for zipfile in zipfiles:
        os.system('open ' + zipfile)  # mass-opening crashes python

    print(failed)
