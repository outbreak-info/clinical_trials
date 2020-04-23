import pandas as pd
import xlrd
import urllib

DATA_URL = "https://bit.ly/3axnfup"
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "versionDate", "name", "alternateName", "funder"]

def formatExcelDate(x, format="%Y-%m-%d"):
    dt = pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(format)
    return(dt)

def listify(row, col_names):
    arr = []
    for col in col_names:
        if(row[col] == row[col]):
            arr.append(row[col])
    return(arr)


def getUminTrials(url, col_names):
    # Import the UMIN COVID-19 Clinical Trials registry list as .xls; required encoding is latin-1
    file_name, headers = urllib.request.urlretrieve(DATA_URL)
    data = xlrd.open_workbook(file_name, encoding_override='latin_1')
    # Make sure dates are read in as strings, then parsed into python date objects later and formatted back to a string
    df = pd.read_excel(data, dtype={"Last Refreshed on": str})

    # Convert to outbreak.info Clinical Trial schema: https://github.com/SuLab/outbreak.info-resources/blob/master/yaml/outbreak.json
    # Mapping file:
    df["@type"] = "ClinicalTrial"
    df["_id"] = df.TrialID # ES index id
    df["identifier"] = df.TrialID
    df["identifierSource"] = df["Source Register"]
    df["versionDate"] = df["Last Refreshed on"].apply(lambda x: formatExcelDate(x))
    df["name"] = df["Scientific title"]
    df["alternateName"] = df.apply(lambda x: listify(x, ["Acronym", "Public title"]), axis=1)

    print(df[col_names].head(3).to_json(orient="records"))

    return(df)

# def convertExcelDate(date):
x = getUminTrials(DATA_URL, COL_NAMES)

print(x.loc[0, COL_NAMES])
x.loc[0, "alternateName"]
