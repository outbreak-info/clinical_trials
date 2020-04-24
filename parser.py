import pandas as pd
import xlrd
import urllib
import requests
from math import ceil

"""
Parser to grab COVID-19 / SARS-Cov-2 Clinical Trials metadata.
Sources:
- ClinicalTrials.gov: based off of https://clinicaltrials.gov/ct2/results?cond=COVID-19; doing an API search on the 4 terms
- NCT data dictionary: https://clinicaltrials.gov/ct2/about-studies/glossary
- NCT "how things are represented on their website": https://clinicaltrials.gov/api/gui/ref/crosswalks
- PRS data dictionary: https://prsinfo.clinicaltrials.gov/definitions.html
- WHO data dictionary: https://www.who.int/ictrp/glossary/en/
"""
CT_API = 'https://clinicaltrials.gov/api/query/full_studies?expr=(%22covid-19%22%20OR%20%22sars-cov-2%22)&fmt=json'
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "description", "org", "sponsor", "author",
"studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "versionDate"]


def getUSTrial(url, col_names, startIdx=1, endIdx=100):
    api_url = f"{url}&min_rnk={startIdx}&max_rnk={endIdx}"
    resp = requests.get(api_url)
    if resp.status_code == 200:
        raw_data = resp.json()
        # So the Clinical Trials.gov API *really* likes nested functions
        studies = raw_data["FullStudiesResponse"]["FullStudies"]
        flat_studies = [study["Study"] for study in studies]
        df = pd.DataFrame(flattenJson(flat_studies))

        # Convert to outbreak.info Clinical Trial schema: https://github.com/SuLab/outbreak.info-resources/blob/master/yaml/outbreak.json
        # Mapping file:
        df["@type"] = "ClinicalTrial"
        df["_id"] = df["IdentificationModule"].apply(lambda x: x["NCTId"]) # ES index ID
        df["identifier"] = df["IdentificationModule"].apply(lambda x: x["NCTId"])
        df["org"] = df["IdentificationModule"].apply(lambda x: x["Organization"]["OrgClass"])
        df["url"] = df["IdentificationModule"].apply(lambda x: f"https://clinicaltrials.gov/ct2/show/{x['NCTId']}")
        df["identifierSource"] = "ClinicalTrials.gov"
        df["name"] = df["IdentificationModule"].apply(lambda x: x["OfficialTitle"])
        df["alternateName"] = df["IdentificationModule"].apply(lambda x: listify(x, ["Acronym", "BriefTitle"]))
        df["description"] = df["DescriptionModule"].apply(lambda x: x["BriefSummary"])
        df["sponsor"] = df["SponsorCollaboratorsModule"].apply(getSponsor)
        df["studyStatus"] = df["StatusModule"].apply(getStatus)
        df["studyEvent"] = df["StatusModule"].apply(getEvents)
        df["hasResults"] = df["StatusModule"].apply(lambda x: "ResultsFirstSubmitDate" in x.keys())
        df["dateCreated"] = df["StatusModule"].apply(lambda x: formatDate(x["StudyFirstSubmitDate"]))
        df["dateModified"] = df["StatusModule"].apply(lambda x: formatDate(x["LastUpdatePostDateStruct"]["LastUpdatePostDate"]))
        df["datePublished"] = df["StatusModule"].apply(lambda x: formatDate(x["StudyFirstPostDateStruct"]["StudyFirstPostDate"]))
        df["versionDate"] = df["MiscInfoModule"].apply(lambda x: formatDate(x["VersionHolder"]))
        df["author"] = df.apply(getAuthors, axis=1)

        print(df[col_names].head(3).to_json(orient="records"))

        return(df)

def formatDate(x, inputFormat="%B %d, %Y", outputFormat="%Y-%m-%d"):
    date_str = pd.datetime.strptime(x, inputFormat).strftime(outputFormat)
    return(date_str)

def binarize(val):
    if(val == val):
        if((val == "yes") | (val == "Yes") | (val == 1) | (val == "1")):
            return(True)
        if((val == "no") | (val == "No") | (val == 0) | (val == "0")):
            return(False)

def getSponsor(sponsor):
    obj = {}
    obj["@type"] = "Organization"
    obj["name"] = sponsor["LeadSponsor"]["LeadSponsorName"]
    obj["class"] = sponsor["LeadSponsor"]["LeadSponsorClass"]
    return([obj])

def getStatus(status):
    obj = {}
    obj["@type"] = "StudyStatus"
    obj["status"] = status["OverallStatus"]
    obj["statusDate"] = status["StatusVerifiedDate"]
    obj["statusExpanded"] = binarize(status["ExpandedAccessInfo"]["HasExpandedAccess"])
    return(obj)


def getEvents(status):
    arr = []
    arr.append({"@type": "StudyEvent", "studyEventType": "start", "studyEventDate": status["StartDateStruct"]["StartDate"], "studyEventDateType": status["StartDateStruct"]["StartDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "primary completion", "studyEventDate": status["PrimaryCompletionDateStruct"]["PrimaryCompletionDate"], "studyEventDateType": status["PrimaryCompletionDateStruct"]["PrimaryCompletionDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "completion", "studyEventDate": status["CompletionDateStruct"]["CompletionDate"], "studyEventDateType": status["CompletionDateStruct"]["CompletionDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "first posting to clinicaltrials.gov", "studyEventDate": status["StudyFirstPostDateStruct"]["StudyFirstPostDate"], "studyEventDateType": status["StudyFirstPostDateStruct"]["StudyFirstPostDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "last posting to clinicaltrials.gov", "studyEventDate": status["LastUpdatePostDateStruct"]["LastUpdatePostDate"], "studyEventDateType": status["LastUpdatePostDateStruct"]["LastUpdatePostDateType"].lower()})
    if("ResultsFirstPostDateStruct" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first posting of results to clinicaltrials.gov", "studyEventDate": status["ResultsFirstPostDateStruct"]["ResultsFirstPostDate"], "studyEventDateType": status["ResultsFirstPostDateStruct"]["ResultsFirstPostDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission", "studyEventDate": status["StudyFirstSubmitDate"]})
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission that met quality control criteria", "studyEventDate": status["StudyFirstSubmitQCDate"]})
    if("ResultsFirstSubmitDate" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results", "studyEventDate": status["ResultsFirstSubmitDate"]})
    if("ResultsFirstSubmitQCDate" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results that met quality control criteria", "studyEventDate": status["ResultsFirstSubmitQCDate"]})
    arr.append({"@type": "StudyEvent", "studyEventType": "last update submission", "studyEventDate": status["LastUpdateSubmitDate"]})
    return(arr)

def getAuthors(row):
    authors = []
    if(row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyType"] != "Sponsor"):
        obj = {}
        obj["@type"] = "Person"
        obj["name"] = row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyInvestigatorFullName"]
        obj["affiliation"] = row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyInvestigatorAffiliation"]
        obj["title"] = row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyInvestigatorTitle"]
        obj["role"] = row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyType"]
        authors.append(obj)

    return(authors)

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
            arr.append(row[col])
        except:
            pass
    return(arr)


def getUSTrials(url, col_names):
    # Run one query to get the total number of studies.
    resp = requests.get(url)
    if resp.status_code == 200:
        raw_data = resp.json()
        num_results = raw_data["FullStudiesResponse"]["NStudiesFound"]
        results = pd.DataFrame()
        i = 0
        while i < ceil(num_results/100):
            print(i)
            df = getUSTrial(url, col_names, i*100 + 1, (i+1)*100)
            results = pd.concat([results, df], ignore_index=True)
            i += 1
        return(results)

df2 = getUSTrial(CT_API, COL_NAMES)
df2.iloc[0]
# df = getUSTrials(CT_API, COL_NAMES)
# df.StatusModule.apply(lambda x: x["ExpandedAccessInfo"]["HasExpandedAccess"]).value_counts()
# df2.studyStatus.apply(lambda x: x["statusDate"]).value_counts()
# df.StatusModule.apply(lambda x: x["ExpandedAccessInfo"]["HasExpandedAccess"]).value_counts()
