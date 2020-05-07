import pandas as pd
import requests
from math import ceil
import re
import collections
import json

"""
Parser to grab COVID-19 / SARS-Cov-2 Clinical Trials metadata.
Sources:
- ClinicalTrials.gov: based off of https://clinicaltrials.gov/ct2/results?cond=COVID-19; doing an API search on the 4 terms
- NCT data dictionary: https://clinicaltrials.gov/ct2/about-studies/glossary
- NCT "how things are represented on their website": https://clinicaltrials.gov/api/gui/ref/crosswalks
- PRS data dictionary: https://prsinfo.clinicaltrials.gov/definitions.html
"""
CT_QUERY = '%22covid-19%22%20OR%20%22sars-cov-2%22'
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "abstract", "description", "sponsor", "author",
             "studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "curatedBy", "healthCondition", "keywords",
             "studyDesign", "outcome", "eligibilityCriteria", "isBasedOn", "relatedTo", "studyLocation", "armGroup", "interventions"]


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
        df["interventions"] = df["ArmsInterventionsModule"].apply(
            getInterventions)
        df["outcome"] = df["OutcomesModule"].apply(getOutcome)
        df["eligibilityCriteria"] = df["EligibilityModule"].apply(
            getEligibility)
        df["isBasedOn"] = df.apply(getBasedOn, axis=1)
        df["relatedTo"] = df.apply(getRelated, axis=1)
        df["studyLocation"] = df.apply(getLocations, axis=1)

        return(df)

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


def flattenList(l):
    return([item for sublist in l for item in sublist])

# from https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

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
        obj["stdAge"] = list(
            map(lambda x: x.lower(), row["StdAgeList"]["StdAge"]))

    return([obj])


def getOutcome(row):
    arr = []
    if(row == row):
        for outcome in row["PrimaryOutcomeList"]["PrimaryOutcome"]:
            arr.append({"@type": "Outcome", "outcomeMeasure": outcome["PrimaryOutcomeMeasure"],
                        "outcomeTimeFrame": outcome["PrimaryOutcomeTimeFrame"], "outcomeType": "primary"})
        if("SecondaryOutcomeList" in row.keys()):
            for outcome in row["SecondaryOutcomeList"]["SecondaryOutcome"]:
                arr.append({"@type": "Outcome", "outcomeMeasure": outcome["SecondaryOutcomeMeasure"],
                            "outcomeTimeFrame": outcome["SecondaryOutcomeTimeFrame"], "outcomeType": "secondary"})
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
        keywords = [keyword.split(",")
                    for keyword in conditions["KeywordList"]["Keyword"]]
        return(flattenList(keywords))


def getPhaseNumber(phase):
    if(phase.lower() == "early phase 1"):
        return([0,1])
    if(phase.lower() == "phase 1"):
        return(1)
    if(phase.lower() == "phase 2"):
        return(2)
    if(phase.lower() == "phase 3"):
        return(3)
    if(phase.lower() == "phase 4"):
        return(4)
    return(None)

def getDesign(design):
    obj = {}
    if("DesignInfo" in design.keys()):
        design_info = design["DesignInfo"]
        obj["@type"] = "StudyDesign"
        obj["studyType"] = design["StudyType"].lower()
        models = []
        if("DesignAllocation" in design_info.keys()):
            obj["designAllocation"] = design_info["DesignAllocation"].lower()
        if("DesignInterventionModel" in design_info.keys()):
            models.append(design_info["DesignInterventionModel"].lower())
        if("DesignObservationalModelList" in design_info.keys()):
            models.extend(list(map(lambda x: x.lower(
            ), design_info["DesignObservationalModelList"]["DesignObservationalModel"])))
        if("DesignTimePerspectiveList" in design_info.keys()):
            models.extend(list(map(lambda x: x.lower(
            ), design_info["DesignTimePerspectiveList"]["DesignTimePerspective"])))
        obj["designModel"] = models
        if("DesignPrimaryPurpose" in design_info.keys()):
            obj["designPrimaryPurpose"] = design_info["DesignPrimaryPurpose"].lower()
        if("DesignMaskingInfo" in design_info.keys()):
            if ("DesignedWhoMasked" in design_info["DesignMaskingInfo"].keys()):
                obj["designWhoMasked"] = design_info["DesignMaskingInfo"]["designWhoMaskedList"]["DesignWhoMasked"].lower()
        if("PhaseList" in design.keys()):
            obj["phase"] = [phase.lower()
                            for phase in design["PhaseList"]["Phase"]]
            phases = [getPhaseNumber(
                phase) for phase in design["PhaseList"]["Phase"]]
            obj["phaseNumber"] = list(flatten(phases))
        return(obj)

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
            arr.append({"@type": "Organization", "name": collaborator["CollaboratorName"],
                        "class": collaborator["CollaboratorClass"].lower(), "role": "collaborator"})
    return(arr)


def getStatus(row):
    status = row["StatusModule"]
    design = row["DesignModule"]
    obj = {}
    obj["@type"] = "StudyStatus"
    obj["status"] = status["OverallStatus"].lower()
    obj["statusDate"] = status["StatusVerifiedDate"]
    if("statusExpanded" in status.keys()):
        obj["statusExpanded"] = binarize(
            status["ExpandedAccessInfo"]["HasExpandedAccess"])
    if("WhyStopped" in status.keys()):
        obj["whyStopped"] = status["WhyStopped"]
    if("EnrollmentInfo" in design.keys()):
        obj["enrollmentCount"] = int(
            design["EnrollmentInfo"]["EnrollmentCount"])
        obj["enrollmentType"] = design["EnrollmentInfo"]["EnrollmentType"].lower()
    return(obj)


def getEvents(status):
    arr = []
    if("StartDateStruct" in status.keys()):
        arr.append({"@type": "StudyEvent", "studyEventType": "start",
                    "studyEventDate": status["StartDateStruct"]["StartDate"], "studyEventDateType": status["StartDateStruct"]["StartDateType"].lower()})
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
        obj["affiliation"] = [row["SponsorCollaboratorsModule"]
                              ["ResponsibleParty"]["ResponsiblePartyInvestigatorAffiliation"]]
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
                        obj["affiliation"] = [
                            contact["OverallOfficialAffiliation"]]
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
                arr.append({"@type": "Protocol", "name": doc['LargeDocFilename'], "datePublished": formatDate(
                    doc["LargeDocDate"]), "description": f"{doc['LargeDocLabel']} for Clinical Trial {id}", "identifier": f"{id}_{doc['LargeDocFilename']}", "type": "ClinicalTrial", "url": f"https://clinicaltrials.gov/ct2/show/{id}"})
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
                        arr.append({"@type": "Publication", "identifier": f"pmid{pub['ReferencePMID']}", "pmid": pub['ReferencePMID'],
                                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pub['ReferencePMID']}", "citation": pub['ReferenceCitation']})
                    else:
                        arr.append({"@type": "Publication",
                                    "citation": pub['ReferenceCitation']})
            return(arr)


def getLocations(row):
    arr = []
    if("ContactsLocationsModule" in row.keys()):
        if(row["ContactsLocationsModule"] == row["ContactsLocationsModule"]):
            if("LocationList" in row["ContactsLocationsModule"].keys()):
                locations = row["ContactsLocationsModule"]["LocationList"]["Location"]
                for location in locations:
                    if(("LocationState" in location.keys()) & ("LocationStatus" in location.keys())):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": location[
                                   "LocationCountry"], "studyLocationState": location["LocationState"], "studyLocationStatus": location["LocationStatus"].lower()})
                    elif("LocationState" in location.keys()):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"],
                                    "studyLocationCountry": location["LocationCountry"], "studyLocationState": location["LocationState"]})
                    elif("LocationStatus" in location.keys()):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"],
                                    "studyLocationCountry": location["LocationCountry"], "studyLocationStatus": location["LocationStatus"].lower()})
                    else:
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location[
                                   "LocationCity"], "studyLocationCountry": location["LocationCountry"]})
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
                                iObj["name"] = item["InterventionName"]
                                if("InterventionDescription" in item.keys()):
                                    iObj["description"] = item["InterventionDescription"]
                        iArr.append(iObj)
                    obj["intervention"] = iArr

                arr.append(obj)
    return(arr)

def getInterventions(row):
    arr = []
    if(row == row):
        if("InterventionList" in row.keys()):
            intervention_list = row["InterventionList"]["Intervention"]
            for item in intervention_list:
                iObj = {"@type": "Intervention"}
                iObj["category"] = item["InterventionType"].lower()
                if("InterventionName" in item.keys()):
                    iObj["name"] = item["InterventionName"]
                if("InterventionDescription" in item.keys()):
                    iObj["description"] = item["InterventionDescription"]
                arr.append(iObj)
    return(arr)

"""
Helper function to get all the COVID-19-related NCT IDs.
Since the ID fetch is limited to 1000 at a time, continuing to call till get no results found.
Also, the NCT API doesn't seem to have explicit pagination, which means that the results returned are stoichastic.
To try to mitigate this behavior, doing calls along a window to try to grab all the IDs.
"""
def getIDSingle(query, minIdx):
    id_query = f"https://clinicaltrials.gov/api/query/study_fields?expr={query}&min_rnk={int(minIdx*1000+1)}&max_rnk={int(minIdx*1000+1000)}&fields=NCTId&fmt=json"
    resp = requests.get(id_query)
    if resp.status_code == 200:
        raw_data = resp.json()
        num_results = raw_data["StudyFieldsResponse"]["NStudiesFound"]
        if(raw_data["StudyFieldsResponse"]["NStudiesReturned"] > 0):
            ids = [item["NCTId"]
                   for item in raw_data["StudyFieldsResponse"]["StudyFields"]]
            flat_ids = [item for sublist in ids for item in sublist]
            return({"ids": flat_ids, "total": num_results})
        else:
            return(None)

def getIDs(query):
    i = 0
    hasMoreResults = True
    ids = []
    while (hasMoreResults):
        print(f"Getting IDs: call {int(i*2 + 1)}")
        id_list = getIDSingle(query, i)
        if(id_list is None):
            hasMoreResults = False
        else:
            i+= 0.5
            ids = ids + id_list["ids"]
            num_results = id_list["total"]
    unique_ids = pd.np.unique(ids)
    return({"ids": unique_ids, "total": num_results})

"""
Main function to execute the API calls, since they're limited to 100 full records at a time
"""
def getUSTrials(query, col_names, json_output=True):
    num_per_query = 100
    # Run one query to get the IDs of all the studies.
    # Can't loop through numbers of studies à la pagination, since the API returns things in an inconsistent order
    id_dict = getIDs(query)
    num_results = id_dict["total"]
    ids = id_dict["ids"]
    results = pd.DataFrame()
    i = 0
    while i < ceil(num_results / num_per_query):
        print(f"Executing query {i+1} of {ceil(num_results / num_per_query)}")
        query_ids = " OR ".join(ids[i * num_per_query:(i + 1) * num_per_query])
        url = f"https://clinicaltrials.gov/api/query/full_studies?expr=({query_ids})&min_rnk=1&max_rnk=100&fmt=json"
        df = getUSTrial(url, col_names)
        results = pd.concat([results, df], ignore_index=True)
        i += 1
    # Double check that the numbers all agree
    filtered = results[results._id.isin(ids)]

    if(len(filtered) != num_results):
        print(
            f"\nWARNING: number of IDs queried don't equal the number of results. {num_results} expected, but {len(filtered)} records found.\n")
    if(len(results) != len(filtered)):
        extra = results[~results._id.isin(ids)]
        print(f"\nWARNING: ids removed because they weren't in the initial query to get the ID list. Presumably, this record contains a COVID id somewhere in one of its other fields but is not a COVID-19 clinical trial.")
        print(extra._id)
    if(sum(filtered.duplicated(subset="_id"))):
        dupes = filtered[filtered.duplicated(subset="_id")]
        print(
            f"\nERROR: {sum(filtered.duplicated(subset='_id'))} duplicate IDs found:")
        print(dupes._id)

    if(json_output):
        output = filtered[col_names].to_json(orient="records")
    else:
        output = filtered[col_names]
    return(output)


# df = getUSTrial("https://clinicaltrials.gov/api/query/full_studies?expr=(NCT04356560%20OR%20NCT04330261%20OR%20NCT04361396%20OR%20NCT04345679%20OR%20NCT04360811%20OR%20NCT04333862%20OR%20NCT04347278%20OR%20NCT04347850%20OR%20NCT04303299%20OR%20NCT04342637%20OR%20NCT04339322%20OR%20NCT04323787%20OR%20NCT04323800%20OR%20NCT04355897%20OR%20NCT04352764%20OR%20NCT04343781%20OR%20NCT04334876%20OR%20NCT04361422%20OR%20NCT04349202)&fmt=json&min_rnk=1&max_rnk=100", COL_NAMES)

def load_annotations():
    for i,doc in getUSTrials(CT_QUERY, COL_NAMES, True):
        if i == 0:
            print("******PARSER")
            print(type(doc))
            print(doc)
        yield json.loads(doc.decode("utf-8"))
# df.sample(5).to_json("/Users/laurahughes/GitHub/umin-clinical-trials/outputs/NCT_parsed_sample.json", orient="records")
