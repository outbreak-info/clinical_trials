import pandas as pd
import requests
from math import ceil
import re


"""
Parser to grab COVID-19 / SARS-Cov-2 Clinical Trials metadata from the WHO's trial registry.
Sources:
- WHO data: https://www.who.int/ictrp/COVID19-web.csv
- WHO data dictionary: https://www.who.int/ictrp/glossary/en/
- WHO sources:
    - Australian New Zealand Clinical Trials Registry (ANZCTR)
    - Brazilian Clinical Trials Registry (ReBec)
    - Chinese Clinical Trial Register (ChiCTR)
    - Clinical Research Information Service (CRiS), Republic of Korea
    - ClinicalTrials.gov
    - Clinical Trials Registry - India (CTRI)
    - Cuban Public Registry of Clinical Trials (RPCEC)
    - EU Clinical Trials Register (EU-CTR)
    - German Clinical Trials Register (DRKS)
    - Iranian Registry of Clinical Trials (IRCT)
    - ISRCTN
    - Japan Primary Registries Network (JPRN)
    - Pan African Clinical Trial Registry (PACTR)
    - Peruvian Clinical Trials Registry (REPEC)
    - Sri Lanka Clinical Trials Registry (SLCTR)
    - Thai Clinical Trials Register (TCTR)
    - The Netherlands National Trial Register (NTR)
"""

WHO_URL = "https://www.who.int/ictrp/COVID19-web.csv"
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "abstract", "description", "sponsor", "author",
             "studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "curatedBy", "healthCondition", "keywords",
             "studyDesign", "outcome", "eligibilityCriteria", "isBasedOn", "relatedTo", "studyLocation", "armGroup"]

# Generic helper functions
def formatDate(x, inputFormat="%B %d, %Y", outputFormat="%Y-%m-%d"):
    date_str = pd.datetime.strptime(x, inputFormat).strftime(outputFormat)
    return(date_str)


def binarize(val):
    if(val == val):
        if((val == "yes") | (val == "Yes") | (val == 1) | (val == "1")):
            return(True)
        if((val == "no") | (val == "No") | (val == 0) | (val == "0")):
            return(False)


def getIfExists(row, variable):
    if(variable in row.keys()):
        return(row[variable])

def flattenJson(arr):
    flat_list = []

    for study in arr:
        obj = {}
        for key in study:
            for innerKey in study[key]:
                obj[innerKey] = study[key][innerKey]
        flat_list.append(obj)
    return(flat_list)


def listify(row, col_names):
    arr = []
    for col in col_names:
        try:
            if(row[col] == row[col]):
                arr.append(row[col])
        except:
            pass
    return(arr)

"""
WHO Specific functions
"""
# from https://www.who.int/ictrp/search/data_providers/en/
# and https://www.who.int/ictrp/network/primary/en/
# all ids converted to uppercase to account for weirdness in data entry
def convertSource(source):
    source_dict = {
    "ANZCTR": "Australian New Zealand Clinical Trials Registry",
    "REBEC": "Brazilian Clinical Trials Registry",
    "CHICTR": "Chinese Clinical Trial Register",
    "CRIS": "Clinical Research Information Service, Republic of Korea",
    "CTRI": "Clinical Trials Registry - India",
    "NCT": "ClinicalTrials.gov",
    "RPCEC": "Cuban Public Registry of Clinical Trials",
    "EU-CTR": "EU Clinical Trials Register",
    "DRKS": "German Clinical Trials Register",
    "IRCT": "Iranian Registry of Clinical Trials",
    "JPRN": "Japan Primary Registries Network",
    "PACTR": "Pan African Clinical Trial Registry",
    "REPEC": "Peruvian Clinical Trials Registry",
    "SLCTR": "Sri Lanka Clinical Trials Registry",
    "TCTR": "Thai Clinical Trials Register",
    "LBCTR": "Lebanon Clinical Trials Registry",
    "NTR": "Netherlands Trial Register"}
    try:
        return(source_dict[source.upper()])
    except:
        return(source)

def splitCountries(countryString):
    if(countryString == countryString):
        ctries = countryString.split(";")
        return([{"@type": "Place", "studyLocationCountry": country} for country in ctries])
        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location["LocationCountry"]})

def splitCondition(conditionString):
    conditions = [text.split(";") for text in conditionString.split("<br>")]
    flat_list = [item.strip() for sublist in conditions for item in sublist]
    return([item for item in flat_list if item != ""])

def getWHOStatus(row):
    obj = {"@type": "StudyStatus"}
    if(row["Recruitment Status"] == row["Recruitment Status"]):
        obj["status"] = row["Recruitment Status"].lower()
    obj["statusDate"] = row.dateModified

    if(row["Target size"] == row["Target size"]):
        armTargets = [text.split(":") for text in row["Target size"].split(";")]
        targets = []
        for target in armTargets:
            if(len(target) == 2):
                targets.append(int(target[1]))
            else:
                try:
                    targets.append(int(target[0]))
                except:
                    pass
                    # print(f"cannot convert string {target[0]} to an integer")
        enrollmentTarget = sum(targets)

        if(enrollmentTarget > 0):
            obj["enrollmentCount"] = enrollmentTarget
            obj["enrollmentType"] = "anticipated"
    return(obj)

def getWHOEvents(row):
    arr = []
    if(row["Date enrollement"] == row["Date enrollement"]):
        arr.append({"@type": "StudyEvent", "studyEventType": "start", "studyEventDate": row["Date enrollement"], "studyEventDateType": "actual"})
    if(row["results date completed"] == row["results date completed"]):
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results", "studyEventDate": row["results date completed"], "studyEventDateType": "actual"})
    if(row["results date posted"] == row["results date posted"]):
        arr.append({"@type": "StudyEvent", "studyEventType": "first posting of results", "studyEventDate": row["results date posted"], "studyEventDateType": "actual"})
    return(arr)

def getWHOEligibility(row):
    obj = {}
    obj["@type"] = "Eligibility"
    if(row["Inclusion Criteria"] == row["Inclusion Criteria"]):
        criteria = row["Inclusion Criteria"].split("Exclusion Criteria:")
        obj["inclusionCriteria"] = [criteria[0].replace("Inclusion criteria:", "").replace("Inclusion Criteria:", "").strip()]
        if(len(criteria) == 2):
            obj["exclusionCriteria"] = [criteria[1].strip()]
        else:
            obj["exclusionCriteria"] = []
    if(row["Exclusion Criteria"] == row["Exclusion Criteria"]):
        obj["exclusionCriteria"].append(row["Exclusion Criteria"].replace("Exclusion criteria:", "").replace("Exclusion Criteria:", "").strip())
    if(row["Inclusion agemin"] == row["Inclusion agemin"]):
        obj["minimumAge"] = row["Inclusion agemin"].lower()
    if(row["Inclusion agemax"] == row["Inclusion agemax"]):
        obj["maximumAge"] = row["Inclusion agemax"].lower()
    if(row["Inclusion gender"] == row["Inclusion gender"]):
        obj["gender"] = row["Inclusion gender"].lower()
    return([obj])

def getWHOAuthors(row):
    arr = []
    affiliation = row["Contact Affiliation"]
    if((row["Contact Firstname"] == row["Contact Firstname"]) & (row["Contact Lastname"] == row["Contact Lastname"])):
        obj = {}
        obj["@type"] = "Person"
        obj["name"] = f"{row['Contact Firstname']} {row['Contact Lastname']}"
        if(affiliation == affiliation):
            obj["affiliation"] = [affiliation]
        return([obj])
    elif(row["Contact Firstname"] == row["Contact Firstname"]):
        # Assuming one affiliation for all authors?
        author_list = re.split(";|\?|,|;", row["Contact Firstname"])
        for author in author_list:
            if(affiliation == affiliation):
                arr.append({"@type": "Person", "name": author.strip(), "affiliation": [affiliation]})
            else:
                arr.append({"@type": "Person", "name": author.strip()})
        return(arr)
    elif(row["Contact Lastname"] == row["Contact Lastname"]):
        # Assuming one affiliation for all authors?
        author_list = re.split(";|\?|,|;", row["Contact Lastname"])
        for author in author_list:
            if(affiliation == affiliation):
                arr.append({"@type": "Person", "name": author.strip(), "affiliation": [affiliation]})
            else:
                arr.append({"@type": "Person", "name": author.strip()})
        return(arr)

def getOutcome(outcome_string):
    if(outcome_string == outcome_string):
        outcomes = outcome_string.split(";")
        return([{"@type": "Outcome", "outcomeMeasure": outcome, "outcomeType": "primary"} for outcome in outcomes if outcome != ""])

"""
Main function to grab the WHO records for clinical trials.
"""
def getWHOTrials(url, col_names):
    raw = pd.read_csv(WHO_URL, dtype={"Date registration3": str})
    # Remove the data from ClinicalTrials.gov
    df = raw.loc[raw["Source Register"] != "ClinicalTrials.gov",:]
    df = df.copy()

    df["@type"] = "ClinicalTrial"
    df["_id"] = df.TrialID
    df["identifier"] = df.TrialID
    df["url"] = df["web address"]
    df["identifierSource"] = df["Source Register"].apply(convertSource)
    df["name"] = df["Scientific title"]
    df["alternateName"] = df.apply(
        lambda x: listify(x, ["Acronym", "Public title"]), axis=1)
    df["abstract"] = None
    df["description"] = None
    df["isBasedOn"] = None
    df["relatedTo"] = None
    df["keywords"] = None
    df["sponsor"] = df["Primary sponsor"].apply(lambda x: [{"@type": "Organization", "name": x, "role": "lead sponsor"}])
    df["hasResults"] = df["results yes no"].apply(binarize)
    df["dateCreated"] = df["Date registration3"].apply(lambda x: formatDate(x, "%Y%m%d"))
    df["dateModified"] = df["Last Refreshed on"].apply(lambda x: formatDate(x, "%d %B %Y"))
    df["datePublished"] = None
    df["curatedBy"] = df["Export date"].apply(lambda x: {"@type": "Organization", "name": "WHO International Clinical Trials Registry Platform", "url": "https://www.who.int/ictrp/en/", "versionDate": formatDate(x, "%m/%d/%Y %H:%M:%S %p")})
    df["studyLocation"] = df.Countries.apply(splitCountries)
    df["healthCondition"] = df.Condition.apply(splitCondition)
    df["studyStatus"] = df.apply(getWHOStatus, axis = 1)
    df["studyEvent"] = df.apply(getWHOEvents, axis = 1)
    df["eligibilityCriteria"] = df.apply(getWHOEligibility, axis = 1)
    df["author"] = df.apply(getWHOAuthors, axis=1)
    df["studyDesign"] = None
    df["armGroup"] = None
    df["outcome"] = df["Primary outcome"].apply(getOutcome)


    return(df)
    # return(df[col_names])
who = getWHOTrials(WHO_URL, COL_NAMES)

# who[who.dateModified=="2020-04-14"][["identifier", "studyStatus"]]
who.sample(1).iloc[0]["outcome"]
