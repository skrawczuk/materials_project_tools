import pandas as pd
import signal
from selenium import webdriver


def timeout_handler(signum, frame):
    raise RuntimeError


def get_vasp_files(results: pd.DataFrame, driver_path='./chromedriver'):
    """
    Downloads zip files from materials project given query dataframe using selenium (browser automation)

    Parameters
    ----------
    results : data frame
        resulting data frame from a database query. Should at least contain 'material_id' column
    driver_path : str
        path to chrome driver in local directory
    Returns
    -------
    zipfiles : list[str]
        list of file paths to downloaded zipfiles
    failed : list[str]
        list of material IDs where download failed
    """

    zipfiles = []
    failed = []
    driver = webdriver.Chrome(driver_path)
    signal.signal(signal.SIGALRM, timeout_handler)

    for i, mol in results.iterrows():
        signal.alarm(10)

        mat_id = mol['material_id']
        try:
            url = 'https://materialsproject.org/materials/' + mat_id
            driver.get(url)

            while len(driver.find_elements_by_xpath("//*[contains(text(),'" + 'File Formats' + "')]")) < 1:
                pass
            dropdown_menu = driver.find_elements_by_xpath("//*[contains(text(),'" + 'File Formats' + "')]")[0]
            dropdown_menu.click()

            while len(driver.find_elements_by_xpath("//*[contains(text(),'" + 'VASP' + "')]")) < 2:
                pass
            vasp_button = driver.find_elements_by_xpath("//*[contains(text(),'" + 'VASP' + "')]")[1]
            vasp_button.click()

            download_button = driver.find_elements_by_xpath("//*[contains(text(),'" + '1 file(s)' + "')]")[0]
            download_button.click()

            zipfile = '/Users/schuylerkrawczuk/Downloads/material_{}_files.zip'.format(mat_id)
            zipfiles.append(zipfile)

        except RuntimeError:
            failed.append(mat_id)
            pass

    return zipfiles, failed
