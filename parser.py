import pandas as pd
import xlrd
import urllib
import requests

DATA_URL = "https://bit.ly/3axnfup"
CT_API = 'https://clinicaltrials.gov/api/query/full_studies?expr=(%22covid-19%22%20OR%20%22sars-cov-2%22)&min_rnk=1&max_rnk=1&fmt=json'
CT_API = 'https://clinicaltrials.gov/api/query/study_fields?expr=(%22covid-19%22%20OR%20%22sars-cov-2%22)&min_rnk=1&max_rnk=1&fmt=json&fields=Acronym,NCTId'
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "versionDate", "name", "alternateName"]

resp = requests.get(CT_API)
j = resp.json()
j
studies = j["FullStudiesResponse"]["FullStudies"]
studies[0].keys()
x =[study["Study"] for study in studies]
pd.DataFrame([study["Study"] for study in studies])

pd.DataFrame([study[item] for study in x for item in study])

def flattenJson(arr):
    flat_list = []

    for study in arr:
        obj = {}
        for key in study:
            print(key)
            for innerKey in study[key]:
                obj[innerKey] = study[key][innerKey]
        flat_list.append(obj)
    return(flat_list)

z = flattenJson(x)
y = flattenJson(z)


pd.DataFrame(y).columns

pd.DataFrame(flat_list)
pd.DataFrame([item["ProtocolSection"] for item in x])

def formatExcelDate(x, format="%Y-%m-%d"):
    dt = pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(format)
    return(dt)

def listify(row, col_names):
    arr = []
    for col in col_names:
        if(row[col] == row[col]):
            arr.append(row[col])
    return(arr)


def getUSTrials(url, col_names):
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
    df["funder"] = df.apply(lambda x: organizationify()

    print(df[col_names].head(3).to_json(orient="records"))

    return(df)

# def convertExcelDate(date):
x = getUSTrials(DATA_URL, COL_NAMES)

print(x.loc[0, COL_NAMES])
x.loc[0, "alternateName"]
x.Intervention.value_counts()
