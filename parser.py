import pandas as pd
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
CT_QUERY = '%22covid-19%22%20OR%20%22sars-cov-2%22'
WHO_URL = "https://www.who.int/ictrp/COVID19-web.csv"
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "abstract", "description", "sponsor", "author",
             "studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "curatedBy", "healthCondition", "keywords",
             "studyDesign", "outcome", "eligibilityCriteria", "isBasedOn", "relatedTo", "studyLocation", "armGroup"]


"""
Main function to convert a record from NCT schema to outbreak:ClinicalTrial schema.
Lots of revisions of names, coercing to objects/lists, etc.
"""
def getUSTrial(api_url, col_names):
    resp = requests.get(api_url)
    if resp.status_code == 200:
        raw_data = resp.json()
        # So the Clinical Trials.gov API *really* likes nested functions
        studies = raw_data["FullStudiesResponse"]["FullStudies"]
        flat_studies = [study["Study"] for study in studies]
        df = pd.DataFrame(flattenJson(flat_studies))

        # Convert to outbreak.info Clinical Trial schema: https://github.com/SuLab/outbreak.info-resources/blob/master/yaml/outbreak.json
        # Mapping file: https://github.com/flaneuse/clinical-trials/blob/master/schema_mapping.csv
        df["@type"] = "ClinicalTrial"
        df["_id"] = df["IdentificationModule"].apply(
            lambda x: x["NCTId"])  # ES index ID
        df["identifier"] = df["IdentificationModule"].apply(
            lambda x: x["NCTId"])
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
        df["studyLocation"] = df.apply(getLocations, axis=1)

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
            if(row[col] == row[col]):
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
    if(len(criteria) > 3):
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
    if(row == row):
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
    if("DesignInfo" in design.keys()):
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
    if("statusExpanded" in status.keys()):
        obj["statusExpanded"] = binarize(status["ExpandedAccessInfo"]["HasExpandedAccess"])
    if("WhyStopped" in status.keys()):
        obj["whyStopped"] = status["WhyStopped"]
    if("EnrollmentInfo" in design.keys()):
        obj["enrollmentCount"] = int(design["EnrollmentInfo"]["EnrollmentCount"])
        obj["enrollmentType"] = design["EnrollmentInfo"]["EnrollmentType"].lower()
    return(obj)


def getEvents(status):
    arr = []
    if("StartDateStruct" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "start", "studyEventDate": status["StartDateStruct"]["StartDate"], "studyEventDateType": status["StartDateStruct"]["StartDateType"].lower()})
    if("PrimaryCompletionDateStruct" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "primary completion", "studyEventDate": status["PrimaryCompletionDateStruct"][
               "PrimaryCompletionDate"], "studyEventDateType": status["PrimaryCompletionDateStruct"]["PrimaryCompletionDateType"].lower()})
    if("CompletionDateStruct" in status.keys()):
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
    if("ContactsLocationsModule" in row.keys()):
        if(row["ContactsLocationsModule"] == row["ContactsLocationsModule"]):
            if("CentralContactList" in row["ContactsLocationsModule"].keys()):
                contacts = row["ContactsLocationsModule"]["CentralContactList"]["CentralContact"]
                for contact in contacts:
                    obj = {}
                    obj["@type"] = "Person"
                    obj["name"] = contact["CentralContactName"]
                    obj["role"] = contact["CentralContactRole"]
                authors.append(obj)
            if("OverallOfficialList" in row["ContactsLocationsModule"].keys()):
                contacts = row["ContactsLocationsModule"]["OverallOfficialList"]["OverallOfficial"]
                for contact in contacts:
                    obj = {}
                    obj["@type"] = "Person"
                    obj["name"] = contact["OverallOfficialName"]
                    obj["role"] = contact["OverallOfficialRole"]
                    if("OverallOfficialAffiliation" in contact.keys()):
                        obj["affiliation"] = contact["OverallOfficialAffiliation"]
                authors.append(obj)

    return(authors)

# isBasedOn = protocols used to generate the study.
def getBasedOn(row):
    arr = []
    if("LargeDocumentModule" in row.keys()):
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
    if("ReferencesModule" in row.keys()):
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
    if("ContactsLocationsModule" in row.keys()):
        if(row["ContactsLocationsModule"] == row["ContactsLocationsModule"]):
            if("LocationList" in row["ContactsLocationsModule"].keys()):
                locations = row["ContactsLocationsModule"]["LocationList"]["Location"]
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
                        iObj = {"@type": "Intervention"}
                        for item in intervention_list:
                            if (f"{item['InterventionType']}: {item['InterventionName']}" == intervention_name):
                                iObj["category"] = item["InterventionType"].lower()
                                iObj["name"] = item["InterventionName"].lower()
                                iObj["description"] = item["InterventionDescription"]
                        iArr.append(iObj)
                    obj["intervention"] = iArr


                arr.append(obj)
    return(arr)


"""
Main function to execute the API calls, since they're limited to 100 full records at a time
"""
def getUSTrials(query, col_names, json_output=True):
    # Run one query to get the IDs of all the studies.
    # Can't loop through numbers of studies à la pagination, since the API returns things in an inconsistent order
    id_query = f"https://clinicaltrials.gov/api/query/study_fields?expr={query}&max_rnk=1000&fields=NCTId&fmt=json"
    resp = requests.get(id_query)
    if resp.status_code == 200:
        raw_data = resp.json()
        num_results = raw_data["StudyFieldsResponse"]["NStudiesFound"]
        ids = [item["NCTId"] for item in raw_data["StudyFieldsResponse"]["StudyFields"]]
        flat_ids = [item for sublist in ids for item in sublist]
        results = pd.DataFrame()
        i = 0
        while i < ceil(num_results / 100):
            print(f"Executing query {i+1} of {ceil(num_results / 100)}")
            query_ids = " OR ".join(flat_ids[i * 100:(i+1)*100])
            url = f"https://clinicaltrials.gov/api/query/full_studies?expr=({query_ids})&min_rnk=1&max_rnk=100&fmt=json"
            df = getUSTrial(url, col_names)
            results = pd.concat([results, df], ignore_index=True)
            i += 1
        # Double check that the numbers all agree
        filtered = results[results._id.isin(flat_ids)]

        if(len(flat_ids) != num_results):
            print(f"\nWARNING: number of IDs queried don't equal the number of results. {num_results} expected, but {len(flat_ids)} ids queried.\n")
        if(len(results) != len(filtered)):
            extra = results[~results._id.isin(flat_ids)]
            print(f"\nWARNING: ids removed because they weren't in the initial query to get the ID list. Presumably, this record contains a COVID id somewhere in one of its other fields but is not a COVID-19 clinical trial.")
            print(extra._id)
        if(sum(filtered.duplicated(subset="_id"))):
            dupes = filtered[filtered.duplicated(subset="_id")]
            print(f"\nERROR: {sum(filtered.duplicated(subset='_id'))} duplicate IDs found:")
            print(dupes._id)

        if(json_output):
            output = filtered[col_names].to_json(orient="records")
        else:
            output = filtered[col_names]
        return(output)
# df = getUSTrial("https://clinicaltrials.gov/api/query/full_studies?expr=(NCT04356560%20OR%20NCT04330261%20OR%20NCT04361396%20OR%20NCT04345679%20OR%20NCT04360811%20OR%20NCT04333862%20OR%20NCT04347278%20OR%20NCT04347850%20OR%20NCT04303299%20OR%20NCT04342637%20OR%20NCT04339322%20OR%20NCT04323787%20OR%20NCT04323800%20OR%20NCT04355897%20OR%20NCT04352764%20OR%20NCT04343781%20OR%20NCT04334876%20OR%20NCT04361422%20OR%20NCT04349202)&fmt=json&min_rnk=1&max_rnk=100", COL_NAMES)
df = getUSTrials(CT_QUERY, COL_NAMES, False)
df.sample(1).iloc[0]["studyEvent"]

"""
WHO Specific functions
"""
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
    df["identifierSource"] = df["Source Register"]
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
    df["author"] = None
    df["studyDesign"] = None
    df["armGroup"] = None
    df["outcome"] = None


    return(df)
    # return(df[col_names])
who = getWHOTrials(WHO_URL, COL_NAMES)

# who[who.dateModified=="2020-04-14"][["identifier", "studyStatus"]]
#
who.sample(1).iloc[0]["eligibilityCriteria"]
"Inclusion criteria: 1. Patients aged 18 or older, and meet the diagnostic criteria of Diagnosis and Treatment Scheme of Novel Coronavirus Infected Pneumonia published by the National Health Commission. Criteria for diagnosis (meet all the following criteria): \r<br>(1) With epidemiological history;\r<br>(2) Clinical manifestations (meet any 2 of the following): fever, normal or decreased white blood cell count or lymphopenia in the early stage of onset, and Chest radiology in the early stage shows multiple small patchy shadowing and interstitial changes which is especially significant in periphery pulmonary. Furthermore, it develops into bilateral multiple ground-glass opacity and infiltrating shadowing. Pulmonary consolidation occurs in severe cases. Pleural effusion is rare;\r<br>(3) Confirmed case (suspected case obtained one of the following etiologic evidences): a positive result to real-time reverse-transcriptase PCR for respiratory specimen or blood specimen, or Genetic sequencing result of virus in respiratory or blood specimens are highly homologous to SARS-CoV-2; \r<br>2. The person is treated with de-isolation and meets hospital discharge criteria according to the 'Diagnosis and treatment of novel coronavirus pneumonia (trial edition 5)'. However, the respiratory nucleic acid turned positive and there were changes in lung imaging;\r<br>3. Gastrointestinal anatomy and function allowed and use safely, without nausea, vomiting and other gastrointestinal symptoms.".replace("Inclusion criteria", "")


x ="""
<br>        Inclusion Criteria:
<br>
<br>          -  In sputum, throat swab, lower respiratory tract secretion, blood and other samples,
<br>             the nucleic acid of the novel coronavirus was positive, or the sequencing of the virus
<br>             gene was highly homologous with the known novel coronavirus
<br>
<br>          -  Age is between 18-80 years old, the weight is more than 30kg, and there is no limit
<br>             for men and women
<br>
<br>          -  The following conditions were met: creatinine = 110 umol / L, creatinine clearance
<br>             rate (EGFR) = 60 ml / min / 1.73m2, AST and ALT = 5 √ó ULN, TBIL = 2 √ó ULN;
<br>
<br>          -  The subjects should fully understand the purpose, nature, method and possible reaction
<br>             of the study, voluntarily participate in the study and sign the informed consent.
<br>
<br>        Exclusion Criteria:
<br>
<br>          -  Have a clear history of lopinavir or ritonavir or arbidol allergy
<br>
<br>          -  Severe nausea, vomiting, diarrhea and other clinical manifestations affect the oral or
<br>             absorption of the drugs
<br>
<br>          -  At the same time, take drugs that may interact with lopinavir or ritonavir or arbidol
<br>
<br>          -  Patients with serious underlying diseases, including but not limited to heart disease
<br>             (including history of angina pectoris or coronary heart disease or myocardial
<br>             infarction, atrioventricular block), lung, kidney, liver malfunction and mental
<br>             diseases that cannot be treated together
<br>
<br>          -  ancreatitis or hemophilia
<br>
<br>          -  Pregnant and lactating women
<br>
<br>          -  Suspected or confirmed history of alcohol and drug abuse
<br>
<br>          -  Participated in other drug trials in the past month
<br>
<br>          -  The researchers judged that patients were not suitable for the study
<br>      """
x.split("Exclusion Criteria")
