import pandas as pd
import xlrd
import urllib

DATA_URL = "https://bit.ly/3axnfup"
COL_NAMES = ["@type"]

def getUminTrials(url, col_names):
    # Import the UMIN COVID-19 Clinical Trials registry list as .xls; required encoding is latin-1
    file_name, headers = urllib.request.urlretrieve(DATA_URL)
    data = xlrd.open_workbook(file_name, encoding_override='latin_1')
    df = pd.read_excel(data)

    # Convert to outbreak.info Clinical Trial schema: https://github.com/SuLab/outbreak.info-resources/blob/master/yaml/outbreak.json
    # Mapping file: 
    df["@type"] = "ClinicalTrial"

    return(df[col_names].to_json(orient="records"))

getUminTrials(DATA_URL, COL_NAMES)
