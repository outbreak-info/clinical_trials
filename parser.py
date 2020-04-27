import pandas as pd
import xlrd
import urllib
import requests
from math import ceil
import re

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
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "abstract", "description", "org", "sponsor", "author",
             "studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "curatedBy", "healthCondition", "keywords",
             "studyDesign", "outcome", "eligibilityCriteria", "isBasedOn", "relatedTo", "studyLocation", "armGroup"]


"""
Main function to convert a record from NCT schema to outbreak:ClinicalTrial schema.
Lots of revisions of names, coercing to objects/lists, etc.
"""
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
        df["_id"] = df["IdentificationModule"].apply(
            lambda x: x["NCTId"])  # ES index ID
        df["identifier"] = df["IdentificationModule"].apply(
            lambda x: x["NCTId"])
        df["org"] = df["IdentificationModule"].apply(
            lambda x: x["Organization"]["OrgClass"])
        df["url"] = df["IdentificationModule"].apply(
            lambda x: f"https://clinicaltrials.gov/ct2/show/{x['NCTId']}")
        df["identifierSource"] = "ClinicalTrials.gov"
        df["name"] = df["IdentificationModule"].apply(
            lambda x: x["OfficialTitle"])
        df["alternateName"] = df["IdentificationModule"].apply(
            lambda x: listify(x, ["Acronym", "BriefTitle"]))
        df["abstract"] = df["DescriptionModule"].apply(
            lambda x: x["BriefSummary"])
        df["description"] = df["DescriptionModule"].apply(
            lambda x: getIfExists(x, "DetailedDescription"))
        df["sponsor"] = df["SponsorCollaboratorsModule"].apply(getSponsor)
        df["studyStatus"] = df.apply(getStatus, axis=1)
        df["studyEvent"] = df["StatusModule"].apply(getEvents)
        df["hasResults"] = df["StatusModule"].apply(
            lambda x: "ResultsFirstSubmitDate" in x.keys())
        df["dateCreated"] = df["StatusModule"].apply(
            lambda x: formatDate(x["StudyFirstSubmitDate"]))
        df["dateModified"] = df["StatusModule"].apply(lambda x: formatDate(
            x["LastUpdatePostDateStruct"]["LastUpdatePostDate"]))
        df["datePublished"] = df["StatusModule"].apply(
            lambda x: formatDate(x["StudyFirstPostDateStruct"]["StudyFirstPostDate"]))
        df["curatedBy"] = df["MiscInfoModule"].apply(getCurator)
        df["author"] = df.apply(getAuthors, axis=1)
        df["healthCondition"] = df["ConditionsModule"].apply(
            lambda x: x["ConditionList"]["Condition"])
        df["keywords"] = df["ConditionsModule"].apply(getKeywords)
        df["studyDesign"] = df["DesignModule"].apply(getDesign)
        df["armGroup"] = df["ArmsInterventionsModule"].apply(getArms)
        df["outcome"] = df["OutcomesModule"].apply(getOutcome)
        df["eligibilityCriteria"] = df["EligibilityModule"].apply(getEligibility)
        df["isBasedOn"] = df.apply(getBasedOn, axis=1)
        df["relatedTo"] = df.apply(getRelated, axis=1)
        df["studyLocation"] = df["ContactsLocationsModule"].apply(getLocations)

        return(df)

# Gneeric helper functions
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
            arr.append(row[col])
        except:
            pass
    return(arr)

# Specific functions to create objects for a property.
def getEligibility(row):
    obj = {}
    obj["@type"] = "Eligibility"

    criteria = row["EligibilityCriteria"].split("\n\n")
    if(criteria[0] == "Inclusion Criteria:"):
        obj["inclusionCriteria"] = criteria[1].split("\n")
    if(len(criteria) > 2):
        if(criteria[2] == "Exclusion Criteria:"):
            obj["exclusionCriteria"] = criteria[3].split("\n")
    if("MinimumAge" in row.keys()):
        obj["minimumAge"] = row["MinimumAge"].lower()
    if("MaximumAge" in row.keys()):
        obj["maximumAge"] = row["MaximumAge"].lower()
    if("Gender" in row.keys()):
        obj["gender"] = row["Gender"].lower()
    if("HealthyVolunteers" in row.keys()):
        obj["healthyVolunteers"] = binarize(row["HealthyVolunteers"])
    if("StdAgeList" in row.keys()):
        obj["stdAge"] = list(map(lambda x: x.lower(), row["StdAgeList"]["StdAge"]))

    return([obj])

def getOutcome(row):
    arr = []
    for outcome in row["PrimaryOutcomeList"]["PrimaryOutcome"]:
        arr.append({"@type": "Outcome", "outcomeMeasure": outcome["PrimaryOutcomeMeasure"], "outcomeTimeFrame": outcome["PrimaryOutcomeTimeFrame"], "outcomeType": "primary"})
    if("SecondaryOutcomeList" in row.keys()):
        for outcome in row["SecondaryOutcomeList"]["SecondaryOutcome"]:
            arr.append({"@type": "Outcome", "outcomeMeasure": outcome["SecondaryOutcomeMeasure"], "outcomeTimeFrame": outcome["SecondaryOutcomeTimeFrame"], "outcomeType": "secondary"})
    return(arr)

def getCurator(row):
    obj = {}
    obj["@type"] = "Organization"
    obj["name"] = "ClinicalTrials.gov"
    obj["url"] = "https://clinicaltrials.gov/ct2/results?cond=COVID-19"
    obj["versionDate"] = formatDate(row["VersionHolder"])
    return(obj)


def getKeywords(conditions):
    if("KeywordList" in conditions.keys()):
        return(conditions["KeywordList"]["Keyword"])


def getDesign(design):
    obj = {}
    design_info = design["DesignInfo"]
    obj["@type"] = "StudyDesign"
    obj["studyType"] = design["StudyType"].lower()
    if("DesignAllocation" in design_info.keys()):
        obj["designAllocation"] = design_info["DesignAllocation"].lower()
    if("DesignInterventionModel" in design_info.keys()):
        obj["designModel"] = design_info["DesignInterventionModel"].lower()
    if("DesignObservationalModelList" in design_info.keys()):
        obj["designModel"] = list(map(lambda x: x.lower(
        ), design_info["DesignObservationalModelList"]["DesignObservationalModel"]))
    if("DesignTimePerspectiveList" in design_info.keys()):
        obj["designTimePerspective"] = list(map(lambda x: x.lower(
        ), design_info["DesignTimePerspectiveList"]["DesignTimePerspective"]))
    if("DesignPrimaryPurpose" in design_info.keys()):
        obj["designPrimaryPurpose"] = design_info["DesignPrimaryPurpose"].lower()
    if("DesignMaskingInfo" in design_info.keys()):
        if ("DesignedWhoMasked" in design_info["DesignMaskingInfo"].keys()):
            obj["designWhoMasked"] = design_info["DesignMaskingInfo"]["designWhoMaskedList"]["DesignWhoMasked"].lower()
    if("PhaseList" in design.keys()):
        obj["phase"] = design["PhaseList"]["Phase"]
    return([obj])


def getSponsor(sponsor):
    arr = []
    obj = {}
    obj["@type"] = "Organization"
    obj["name"] = sponsor["LeadSponsor"]["LeadSponsorName"]
    obj["class"] = sponsor["LeadSponsor"]["LeadSponsorClass"].lower()
    obj["role"] = "lead sponsor"
    arr.append(obj)
    if("CollaboratorList" in sponsor.keys()):
        collaborators = sponsor["CollaboratorList"]["Collaborator"]
        for collaborator in collaborators:
            arr.append({"@type": "Organization", "name": collaborator["CollaboratorName"], "class": collaborator["CollaboratorClass"].lower(), "role": "collaborator"})
    return(arr)


def getStatus(row):
    status = row["StatusModule"]
    design = row["DesignModule"]
    obj = {}
    obj["@type"] = "StudyStatus"
    obj["status"] = status["OverallStatus"].lower()
    obj["statusDate"] = status["StatusVerifiedDate"]
    obj["statusExpanded"] = binarize(
        status["ExpandedAccessInfo"]["HasExpandedAccess"])
    if("WhyStopped" in status.keys()):
        obj["whyStopped"] = status["WhyStopped"]
    obj["enrollmentCount"] = int(design["EnrollmentInfo"]["EnrollmentCount"])
    obj["enrollmentType"] = design["EnrollmentInfo"]["EnrollmentType"].lower()
    return(obj)


def getEvents(status):
    arr = []
    arr.append({"@type": "StudyEvent", "studyEventType": "start",
                "studyEventDate": status["StartDateStruct"]["StartDate"], "studyEventDateType": status["StartDateStruct"]["StartDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "primary completion", "studyEventDate": status["PrimaryCompletionDateStruct"][
               "PrimaryCompletionDate"], "studyEventDateType": status["PrimaryCompletionDateStruct"]["PrimaryCompletionDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "completion", "studyEventDate": status["CompletionDateStruct"][
               "CompletionDate"], "studyEventDateType": status["CompletionDateStruct"]["CompletionDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "first posting to clinicaltrials.gov",
                "studyEventDate": status["StudyFirstPostDateStruct"]["StudyFirstPostDate"], "studyEventDateType": status["StudyFirstPostDateStruct"]["StudyFirstPostDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "last posting to clinicaltrials.gov",
                "studyEventDate": status["LastUpdatePostDateStruct"]["LastUpdatePostDate"], "studyEventDateType": status["LastUpdatePostDateStruct"]["LastUpdatePostDateType"].lower()})
    if("ResultsFirstPostDateStruct" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first posting of results to clinicaltrials.gov",
                    "studyEventDate": status["ResultsFirstPostDateStruct"]["ResultsFirstPostDate"], "studyEventDateType": status["ResultsFirstPostDateStruct"]["ResultsFirstPostDateType"].lower()})
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission",
                "studyEventDate": status["StudyFirstSubmitDate"]})
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission that met quality control criteria",
                "studyEventDate": status["StudyFirstSubmitQCDate"]})
    if("ResultsFirstSubmitDate" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results",
                    "studyEventDate": status["ResultsFirstSubmitDate"]})
    if("ResultsFirstSubmitQCDate" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results that met quality control criteria",
                    "studyEventDate": status["ResultsFirstSubmitQCDate"]})
    arr.append({"@type": "StudyEvent", "studyEventType": "last update submission",
                "studyEventDate": status["LastUpdateSubmitDate"]})
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
    if(row["ContactsLocationsModule"] == row["ContactsLocationsModule"]):
        if("CentralContactList" in row["ContactsLocationsModule"].keys()):
            contacts = row["ContactsLocationsModule"]["CentralContactList"]["CentralContact"]
            for contact in contacts:
                obj = {}
                obj["@type"] = "Person"
                obj["name"] = contact["CentralContactName"]
                obj["role"] = contact["CentralContactRole"]
        if("OverallOfficialList" in row["ContactsLocationsModule"].keys()):
            contacts = row["ContactsLocationsModule"]["OverallOfficialList"]["OverallOfficial"]
            for contact in contacts:
                obj = {}
                obj["@type"] = "Person"
                obj["name"] = contact["OverallOfficialName"]
                obj["role"] = contact["OverallOfficialRole"]
                obj["affiliation"] = contact["OverallOfficialAffiliation"]
            authors.append(obj)

    return(authors)

# isBasedOn = protocols used to generate the study.
def getBasedOn(row):
    arr = []
    # if("LargeDocList" in row["LargeDocumentModule"].keys()):
    if(row["LargeDocumentModule"] == row["LargeDocumentModule"]):
        id = row["IdentificationModule"]['NCTId']
        files = row["LargeDocumentModule"]["LargeDocList"]["LargeDoc"]
        for doc in files:
            arr.append({"@type": "Protocol", "name": doc['LargeDocFilename'], "datePublished": formatDate(doc["LargeDocDate"]), "description": f"{doc['LargeDocLabel']} for Clinical Trial {id}", "identifier": f"{id}_{doc['LargeDocFilename']}", "type": "ClinicalTrial", "url": f"https://clinicaltrials.gov/ct2/show/{id}"})
    return(arr)

# Related = related publications, etc.
# Stuff cited by the clinical trial.
def getRelated(row):
    arr = []
    if(row["ReferencesModule"] == row["ReferencesModule"]):
        if("ReferenceList" in row["ReferencesModule"].keys()):
            pubs = row["ReferencesModule"]["ReferenceList"]["Reference"]
            for pub in pubs:
                if("ReferencePMID" in pub.keys()):
                    arr.append({"@type": "Publication", "identifier": f"pmid{pub['ReferencePMID']}", "pmid": pub['ReferencePMID'], "citation": pub['ReferenceCitation']})
                else:
                    arr.append({"@type": "Publication", "citation": pub['ReferenceCitation']})
    return(arr)

def getLocations(row):
    arr = []
    if(row == row):
        if("LocationList" in row.keys()):
            locations = row["LocationList"]["Location"]
            for location in locations:
                if(("LocationState" in location.keys()) & ("LocationStatus" in location.keys())):
                    arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location["LocationCountry"], "studyLocationState": location["LocationState"], "studyLocationStatus": location["LocationStatus"].lower()})
                elif("LocationState" in location.keys()):
                    arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location["LocationCountry"], "studyLocationState": location["LocationState"]})
                elif("LocationStatus" in location.keys()):
                    arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location["LocationCountry"], "studyLocationStatus": location["LocationStatus"].lower()})
                else:
                    arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location["LocationCountry"]})
    return(arr)

# Join together arms and interventions
def getArms(row):
    arr = []
    if(row == row):
        if("ArmGroupList" in row.keys()):
            arms = row["ArmGroupList"]["ArmGroup"]
            intervention_list = []
            if("InterventionList" in row.keys()):
                intervention_list = row["InterventionList"]["Intervention"]
            for arm in arms:
                obj = {"@type": "ArmGroup"}
                if("ArmGroupLabel" in arm.keys()):
                    obj["name"] = arm["ArmGroupLabel"]
                if("ArmGroupDescription" in arm.keys()):
                    obj["description"] = arm["ArmGroupDescription"]
                if("ArmGroupType" in arm.keys()):
                    obj["role"] = arm["ArmGroupType"].lower()
                if("ArmGroupInterventionList" in arm.keys()):
                    interventions = arm["ArmGroupInterventionList"]["ArmGroupInterventionName"]
                    iArr = []
                    for intervention_name in interventions:
                        print(intervention_name)
                        iObj = {"@type": "Intervention"}
                        for item in intervention_list:
                            if (f"{item['InterventionType']}: {item['InterventionName']}" == intervention_name):
                                iObj["category"] = item["InterventionType"].lower()
                                iObj["name"] = item["InterventionName"].lower()
                                iObj["description"] = item["InterventionDescription"].lower()
                        iArr.append(iObj)
                    obj["intervention"] = iArr


                arr.append(obj)
    return(arr)

"""
Main function to execute the API calls, since they're limited to 100 full records at a time
"""
def getUSTrials(url, col_names):
    # Run one query to get the total number of studies.
    resp = requests.get(url)
    if resp.status_code == 200:
        raw_data = resp.json()
        num_results = raw_data["FullStudiesResponse"]["NStudiesFound"]
        results = pd.DataFrame()
        i = 0
        while i < ceil(num_results / 100):
            print(i)
            df = getUSTrial(url, col_names, i * 100 + 1, (i + 1) * 100)
            results = pd.concat([results, df], ignore_index=True)
            i += 1
        return(results)


df2 = getUSTrial(CT_API, COL_NAMES)
df2.hasResults.value_counts()

df2.index[df2.identifier == "NCT04341441"]
df2.iloc[38]["armGroup"]
# "LargeDocList" in df2.iloc[35]["LargeDocumentModule"].keys()

# df = getUSTrials(CT_API, COL_NAMES)
# df.StatusModule.apply(lambda x: x["WhyStopped"]).value_counts()
# df2.studyStatus.apply(lambda x: x["statusDate"]).value_counts()
# df.StatusModule.apply(lambda x: x["ExpandedAccessInfo"]["HasExpandedAccess"]).value_counts()
