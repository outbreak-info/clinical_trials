import pandas as pd
import numpy as np
import requests
from math import ceil
import re
import collections
import json
import os
from datetime import date, datetime

"""
Parser to grab COVID-19 / SARS-Cov-2 Clinical Trials metadata.
Sources:
- ClinicalTrials.gov: based off of https://clinicaltrials.gov/ct2/results?cond=COVID-19; doing an API search on the 4 terms
- NCT data dictionary: https://clinicaltrials.gov/ct2/about-studies/glossary
- NCT "how things are represented on their website": https://clinicaltrials.gov/api/gui/ref/crosswalks
- PRS data dictionary: https://prsinfo.clinicaltrials.gov/definitions.html
"""
CT_QUERY = '%22covid-19%22%20OR%20%22sars-cov-2%22'
# Names derived from Natural Earth to standardize to their ISO3 code (ADM0_A3) and NAME for geo-joins: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/
COUNTRY_FILE = "https://raw.githubusercontent.com/flaneuse/clinical_trials/master/naturalearth_countries.csv"
COL_NAMES = ["@type", "_id", "identifier", "identifierSource", "url", "name", "alternateName", "abstract", "description", "funding", "author",
             "studyStatus", "studyEvent", "hasResults", "dateCreated", "datePublished", "dateModified", "curatedBy", "healthCondition", "keywords",
             "studyDesign", "outcome", "eligibilityCriteria", "isBasedOn", "relatedTo", "citedBy", "studyLocation", "armGroup", "interventions"]


"""
Main function to convert a record from NCT schema to outbreak:ClinicalTrial schema.
Lots of revisions of names, coercing to objects/lists, etc.
"""


def getUSTrial(api_url, country_dict, col_names):
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
        df["name"] = df["IdentificationModule"].apply(getTitle)
        df["alternateName"] = df["IdentificationModule"].apply(
            lambda x: listify(x, ["Acronym", "BriefTitle"]))
        df["abstract"] = df["DescriptionModule"].apply(
            lambda x: x["BriefSummary"])
        df["description"] = df["DescriptionModule"].apply(
            lambda x: getIfExists(x, "DetailedDescription"))
        df["funding"] = df["SponsorCollaboratorsModule"].apply(getFunding)
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
        df["curatedBy"] = df.apply(getCurator, axis=1)
        df["author"] = df.apply(getAuthors, axis=1)
        df["healthCondition"] = df["ConditionsModule"].apply(
            lambda x: x["ConditionList"]["Condition"])
        df["keywords"] = df["ConditionsModule"].apply(getKeywords)
        df["studyDesign"] = df["DesignModule"].apply(getDesign)
        df["armGroup"] = df.apply(getArms, axis=1)
        df["interventions"] = df.apply(getInterventions, axis=1)
        df["outcome"] = df["OutcomesModule"].apply(getOutcome)
        df["eligibilityCriteria"] = df["EligibilityModule"].apply(
            getEligibility)
        df["refs"] = df.apply(getRefs, axis=1)
        df["protocols"] = df.apply(getProtocols, axis=1)
        df["isBasedOn"] = df.apply(getBasedOn, axis=1)
        df["relatedTo"] = df.refs.apply(lambda x: x["related"])
        df["citedBy"] = df.refs.apply(lambda x: x["citedby"])
        df["studyLocation"] = df.apply(lambda x: getLocations(x, country_dict), axis=1)

        return(df)

# Generic helper functions
def formatDate(x, inputFormat="%B %d, %Y", outputFormat="%Y-%m-%d"):
    date_str = datetime.strptime(x, inputFormat).strftime(outputFormat)
    return(date_str)


def binarize(val):
    if(val == val):
        if((val == "yes") | (val == "Yes") | (val == 1) | (val == "1") | (val.lower() == "accepts healthy volunteers")):
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
def getTitle(idMod):
    if("OfficialTitle" in idMod.keys()):
        return(idMod["OfficialTitle"])
    if("BriefTitle" in idMod.keys()):
        return(idMod["BriefTitle"])

def parseCriteria(criteriaString):
    criteria = criteriaString.split("\n\n")
    criteria
    iInclusion = [n for n, l in enumerate(
        criteria) if l.lower().startswith('inclusion')]

    iExclusion = [n for n, l in enumerate(
        criteria) if l.lower().startswith('exclusion')]
    iNon = [n for n, l in enumerate(
        criteria) if l.lower().startswith('non-inclusion')]
    iExclusion = iExclusion + iNon
    iExclusion.sort()

    obj = {}
    obj = {"criteriaText": criteriaString}
    obj["inclusionCriteria"] = []
    obj["exclusionCriteria"] = []
    for i, foundIdx in enumerate(iInclusion):
        try:
            inclIndices = range(foundIdx, iExclusion[i])
        except:
            inclIndices = range(foundIdx, len(criteria))
        for j in inclIndices:
            splitIncl = criteria[j].split("\n")
            obj["inclusionCriteria"].extend(list(filter(removeInclHeader, splitIncl)))
    for i, foundIdx in enumerate(iExclusion):
        try:
            exclIndices = range(foundIdx, iInclusion[i+1])
        except:
            exclIndices = range(foundIdx, len(criteria))
        for j in exclIndices:
            splitExcl = criteria[j].split("\n")
            obj["exclusionCriteria"].extend(list(filter(removeInclHeader, splitExcl)))
    return(obj)

def removeInclHeader(x):
    return((x.lower() != "inclusion criteria:") & (x.lower() != "inclusion criteria") & (x.lower() != "exclusion criteria:") & (x.lower() != "exclusion criteria") & (x.lower() != "non-inclusion criteria:") & (x.lower() != "non-inclusion criteria"))

def getEligibility(row):
    obj = {}
    obj["@type"] = "Eligibility"

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
    if("EligibilityCriteria" in row.keys()):
        criteria = parseCriteria(row["EligibilityCriteria"])
        # combine criteria + demo criteria
        return({**criteria, **obj})
    else:
        return(obj)


def getOutcome(row):
    arr = []
    if(row == row):
        for outcome in row["PrimaryOutcomeList"]["PrimaryOutcome"]:
            obj = {"@type": "Outcome", "outcomeType": "primary"}
            if("PrimaryOutcomeMeasure" in outcome.keys()):
                obj["outcomeMeasure"] = outcome["PrimaryOutcomeMeasure"]
            if("PrimaryOutcomeTimeFrame" in outcome.keys()):
                obj["outcomeTimeFrame"] = outcome["PrimaryOutcomeTimeFrame"]
            arr.append(obj)
        if("SecondaryOutcomeList" in row.keys()):
            for outcome in row["SecondaryOutcomeList"]["SecondaryOutcome"]:
                arr.append({"@type": "Outcome", "outcomeMeasure": outcome["SecondaryOutcomeMeasure"],
                            "outcomeTimeFrame": outcome["SecondaryOutcomeTimeFrame"], "outcomeType": "secondary"})
        return(arr)


def getCurator(row):
    today = date.today().strftime("%Y-%m-%d")
    obj = {}
    obj["@type"] = "Organization"
    obj["identifier"] = "NCT"
    obj["name"] = "ClinicalTrials.gov"
    obj["url"] = row["url"]
    obj["versionDate"] = formatDate(row["MiscInfoModule"]["VersionHolder"])
    obj["curationDate"] = today
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

def getFunding(sponsor):
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
    return([{"funder": arr}])


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
        try:
            start_date = formatDate(status["StartDateStruct"]["StartDate"])
        except:
            start_date = status["StartDateStruct"]["StartDate"]
        start = {"@type": "StudyEvent", "studyEventType": "start","studyEventDate": start_date}
        if("StartDateType" in status["StartDateStruct"].keys()):
            start["studyEventDateType"] = status["StartDateStruct"]["StartDateType"].lower()
        arr.append(start)

    if("PrimaryCompletionDateStruct" in status.keys()):
        try:
            done_date = formatDate(status["PrimaryCompletionDateStruct"]["PrimaryCompletionDate"])
        except:
            done_date = status["PrimaryCompletionDateStruct"]["PrimaryCompletionDate"]
        done = {"@type": "StudyEvent", "studyEventType": "primary completion", "studyEventDate": done_date}
        if("PrimaryCompletionDateType" in status["PrimaryCompletionDateStruct"].keys()):
            done["studyEventDateType"] = status["PrimaryCompletionDateStruct"]["PrimaryCompletionDateType"].lower()
        arr.append(done)

    if("CompletionDateStruct" in status.keys()):
        try:
            done_date2 = formatDate(status["CompletionDateStruct"]["CompletionDate"])
        except:
            done_date2 = status["CompletionDateStruct"]["CompletionDate"]
        done2 = {"@type": "StudyEvent", "studyEventType": "completion", "studyEventDate": done_date2}
        if("CompletionDateType" in status["CompletionDateStruct"].keys()):
            done2["studyEventDateType"] = status["CompletionDateStruct"]["CompletionDateType"].lower()
        arr.append(done2)

    try:
        post_date = formatDate(status["StudyFirstPostDateStruct"]["StudyFirstPostDate"])
    except:
        post_date = status["StudyFirstPostDateStruct"]["StudyFirstPostDate"]
    arr.append({"@type": "StudyEvent", "studyEventType": "first posting to clinicaltrials.gov",
                "studyEventDate": post_date, "studyEventDateType": status["StudyFirstPostDateStruct"]["StudyFirstPostDateType"].lower()})

    try:
        last_post_date = formatDate(status["LastUpdatePostDateStruct"]["LastUpdatePostDate"])
    except:
        last_post_date = status["LastUpdatePostDateStruct"]["LastUpdatePostDate"]
    arr.append({"@type": "StudyEvent", "studyEventType": "last posting to clinicaltrials.gov",
                "studyEventDate": last_post_date, "studyEventDateType": status["LastUpdatePostDateStruct"]["LastUpdatePostDateType"].lower()})

    if("ResultsFirstPostDateStruct" in status.keys()):
        try:
            results_date = formatDate(status["ResultsFirstPostDateStruct"]["ResultsFirstPostDate"])
        except:
            results_date = status["ResultsFirstPostDateStruct"]["ResultsFirstPostDate"]
        results = {"@type": "StudyEvent", "studyEventType": "first posting of results to clinicaltrials.gov",
                    "studyEventDate": results_date}
        if("ResultsFirstPostDateType" in status["ResultsFirstPostDateStruct"].keys()):
            results["studyEventDateType"] = status["ResultsFirstPostDateStruct"]["ResultsFirstPostDateType"].lower()
        arr.append(results)

    try:
        submit_date = formatDate(status["StudyFirstSubmitDate"])
    except:
        submit_date = status["StudyFirstSubmitDate"]
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission",
                "studyEventDate": submit_date})

    try:
        submit_qc_date = formatDate(status["StudyFirstSubmitQCDate"])
    except:
        submit_qc_date = status["StudyFirstSubmitQCDate"]
    arr.append({"@type": "StudyEvent", "studyEventType": "first submission that met quality control criteria",
                "studyEventDate": submit_qc_date})

    if("ResultsFirstSubmitDate" in status.keys()):
        try:
            results_submit_date = formatDate(status["ResultsFirstSubmitDate"])
        except:
            results_submit_date = status["ResultsFirstSubmitDate"]
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results",
                    "studyEventDate": results_submit_date})

    if("ResultsFirstSubmitQCDate" in status.keys()):
        try:
            results_qc_date = formatDate(status["ResultsFirstSubmitQCDate"])
        except:
            results_qc_date = status["ResultsFirstSubmitQCDate"]
        arr.append({"@type": "StudyEvent", "studyEventType": "first submission of results that met quality control criteria",
                    "studyEventDate": results_qc_date})

    try:
        last_update = formatDate(status["LastUpdateSubmitDate"])
    except:
        last_update = status["LastUpdateSubmitDate"]
    arr.append({"@type": "StudyEvent", "studyEventType": "last update submission",
                "studyEventDate": last_update})
    return(arr)


def getAuthors(row):
    authors = []
    responsible_party = row.get('SponsorCollaboratorsModule', {}).get('ResponsibleParty')
    if responsible_party:
        if(responsible_party["ResponsiblePartyType"] != "Sponsor"):
            obj = {}
            obj["@type"] = "Person"
            obj["name"] = row["SponsorCollaboratorsModule"]["ResponsibleParty"]["ResponsiblePartyInvestigatorFullName"]
            obj["affiliation"] = [{"@type": "Organization", "name": row["SponsorCollaboratorsModule"]
                                  ["ResponsibleParty"]["ResponsiblePartyInvestigatorAffiliation"]}]
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
                            {"@type": "Organization", "name": contact["OverallOfficialAffiliation"]}]
                    authors.append(obj)

    return(authors)

def getProtocols(row):
    arr = []
    if("LargeDocumentModule" in row.keys()):
        if(row["LargeDocumentModule"] == row["LargeDocumentModule"]):
            id = row["IdentificationModule"]['NCTId']
            files = row["LargeDocumentModule"]["LargeDocList"]["LargeDoc"]
            for doc in files:
                if(doc['LargeDocLabel'] == "Informed Consent Form"):
                    protCat = "procedure"
                else:
                    protCat = "protocol"
                arr.append({"@type": "Protocol", "name": doc['LargeDocFilename'], "author": row["author"], "curatedBy": row["curatedBy"], "datePublished": formatDate(
                    doc["LargeDocDate"]), "description": f"{doc['LargeDocLabel']} for Clinical Trial {id}: {row['name']}", "_id": f"{id}_{doc['LargeDocFilename']}", "identifier": f"{id}_{doc['LargeDocFilename']}", "protocolCategory": protCat, "protocolSetting": "clinical", "url": f"https://clinicaltrials.gov/ct2/show/{id}"})
            return(arr)


# isBasedOn = protocols used to generate the study OR reference cited as being "background"
def getBasedOn(row):
    arr = []
    if(row.protocols is not None):
        arr.extend(row.protocols)
    arr.extend(row.refs["based"])
    if(len(arr) > 0):
        return(arr)

# Related = related publications, etc.
# Stuff cited by the clinical trial.
# ReferenceType "derived" --> `relatedTo` (link established by PubMed search of the NCT id)
# ReferenceType "result" --> `citedBy`
# ReferenceType "background" --> `isBasedOn`
def getRelated(refs):
    return(refs["related"])

def getRefs(row):
    obj = {"related": [], "based": [], "citedby": []}
    if("ReferencesModule" in row.keys()):
        if(row["ReferencesModule"] == row["ReferencesModule"]):
            if("ReferenceList" in row["ReferencesModule"].keys()):
                pubs = row["ReferencesModule"]["ReferenceList"]["Reference"]
                for pub in pubs:
                    if("ReferencePMID" in pub.keys()):
                        ref = {"@type": "Publication", "identifier": f"pmid{pub['ReferencePMID']}", "pmid": pub['ReferencePMID'],
                                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pub['ReferencePMID']}", "citation": pub['ReferenceCitation']}
                    else:
                        ref = {"@type": "Publication",
                                    "citation": pub['ReferenceCitation']}
                    if("ReferenceType" in pub.keys()):
                        if(pub["ReferenceType"].lower() == "background"):
                            obj["based"].append(ref)
                        elif(pub["ReferenceType"].lower() == "result"):
                            obj["citedby"].append(ref)
                        else:
                            obj["related"].append(ref)
                    else:
                        obj["related"].append(ref)
            if("SeeAlsoLinkList" in row["ReferencesModule"].keys()):
                pubs = row["ReferencesModule"]["SeeAlsoLinkList"]["SeeAlsoLink"]
                for pub in pubs:
                    obj["related"].append({"@type": "WebSite", "name": pub["SeeAlsoLinkLabel"], "url": pub['SeeAlsoLinkURL']})
    return(obj)


def standardizeCountry(input, ctry_dict, return_val = "country_name"):
    try:
        return(ctry_dict[input.lower()]["country_name"])
    except:
        print(f"No match found for country {input}")
        return(input)

def getLocations(row, country_dict):
    arr = []
    if("ContactsLocationsModule" in row.keys()):
        if(row["ContactsLocationsModule"] == row["ContactsLocationsModule"]):
            if("LocationList" in row["ContactsLocationsModule"].keys()):
                locations = row["ContactsLocationsModule"]["LocationList"]["Location"]
                for location in locations:
                    if(("LocationState" in location.keys()) & ("LocationStatus" in location.keys())):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"], "studyLocationCountry": standardizeCountry(location[
                                   "LocationCountry"], country_dict), "studyLocationState": location["LocationState"], "studyLocationStatus": location["LocationStatus"].lower()})
                    elif("LocationState" in location.keys()):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"],
                                    "studyLocationCountry": standardizeCountry(location["LocationCountry"], country_dict), "studyLocationState": location["LocationState"]})
                    elif("LocationStatus" in location.keys()):
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location["LocationCity"],
                                    "studyLocationCountry": standardizeCountry(location["LocationCountry"], country_dict), "studyLocationStatus": location["LocationStatus"].lower()})
                    else:
                        arr.append({"@type": "Place", "name": location["LocationFacility"], "studyLocationCity": location[
                                   "LocationCity"], "studyLocationCountry": standardizeCountry(location["LocationCountry"], country_dict)})
        return(arr)

# Join together arms and interventions
def getArms(row):
    if("ArmsInterventionsModule" in row.keys()):
        arr = []
        arms_mod = row["ArmsInterventionsModule"]
        if(arms_mod == arms_mod):
            if("ArmGroupList" in arms_mod.keys()):
                arms = arms_mod["ArmGroupList"]["ArmGroup"]
                intervention_list = []
                if("InterventionList" in arms_mod.keys()):
                    intervention_list = arms_mod["InterventionList"]["Intervention"]
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
    if("ArmsInterventionsModule" in row.keys()):
        arr = []
        arms_mod = row["ArmsInterventionsModule"]
        if(arms_mod == arms_mod):
            if("InterventionList" in arms_mod.keys()):
                intervention_list = arms_mod["InterventionList"]["Intervention"]
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
    unique_ids = np.unique(ids)
    return({"ids": unique_ids, "total": num_results})

"""
Main function to execute the API calls, since they're limited to 100 full records at a time
"""
def getUSTrials(query, country_file, col_names, json_output=True):
    num_per_query = 100

    # Natural Earth file to normalize country names.
    ctry_dict = pd.read_csv(country_file).set_index("name").to_dict(orient="index")
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
        df = getUSTrial(url, ctry_dict, col_names)
        results = pd.concat([results, df], ignore_index=True, sort=False)
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
        protocols = flattenList(filtered.loc[(filtered.protocols.notnull()), "protocols"])
        output = filtered[col_names].to_dict(orient="records")
        output = output + protocols
    else:
        output = filtered
    return(output)

# df = getUSTrials(CT_QUERY, COUNTRY_FILE, COL_NAMES, False)
# df.iloc[0]["armGroup"]

def load_annotations():
    docs = getUSTrials(CT_QUERY, COUNTRY_FILE, COL_NAMES, True)
    for doc in docs:
        yield doc
