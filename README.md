# clinical-trials
Parser to import COVID-19 NCT clinical trials from [clinicaltrials.gov](https://clinicaltrials.gov/ct2/results?cond=COVID-19) into [outbreak.info](https://outbreak.info/resources?type=ClinicalTrial)

## About the data
The clinical trials metadata is sourced from [clinicaltrials.gov](https://clinicaltrials.gov/ct2/results?cond=COVID-19) and is accessed using their API with search term ["COVID-19"](https://clinicaltrials.gov/api/query/full_studies?expr=COVID-19&fmt=json).  

Note, this is a BioThings SDK data plugin. More information about BioThings SDK data plugins and how they work with the BioThings SDK (including installation requirements, instructions, etc.) can be found at: https://docs.biothings.io/en/latest/

## Parsing
### Example [initial record](https://clinicaltrials.gov/api/query/full_studies?expr=NCT04341441&fmt=json):
```
{
  "ProtocolSection": {
    "IdentificationModule": {
      "NCTId": "NCT04341441",
      "OrgStudyIdInfo": {
        "OrgStudyId": "1410401"
      },
      "Organization": {
        "OrgFullName": "Henry Ford Health System",
        "OrgClass": "OTHER"
      },
      "BriefTitle": "Will Hydroxychloroquine Impede or Prevent COVID-19",
      "OfficialTitle": "Will Hydroxychloroquine Impede or Prevent COVID-19: WHIP COVID-19 Study",
      "Acronym": "WHIP COVID-19"
    },
    "StatusModule": {
      "StatusVerifiedDate": "April 2020",
      "OverallStatus": "Recruiting",
      "ExpandedAccessInfo": {
        "HasExpandedAccess": "No"
      },
      "StartDateStruct": {
        "StartDate": "April 7, 2020",
        "StartDateType": "Actual"
      },
      "PrimaryCompletionDateStruct": {
        "PrimaryCompletionDate": "June 30, 2020",
        "PrimaryCompletionDateType": "Anticipated"
      },
      "CompletionDateStruct": {
        "CompletionDate": "April 30, 2021",
        "CompletionDateType": "Anticipated"
      },
      "StudyFirstSubmitDate": "April 7, 2020",
      "StudyFirstSubmitQCDate": "April 7, 2020",
      "StudyFirstPostDateStruct": {
        "StudyFirstPostDate": "April 10, 2020",
        "StudyFirstPostDateType": "Actual"
      },
      "LastUpdateSubmitDate": "April 13, 2020",
      "LastUpdatePostDateStruct": {
        "LastUpdatePostDate": "April 15, 2020",
        "LastUpdatePostDateType": "Actual"
      }
    },
    "SponsorCollaboratorsModule": {
      "ResponsibleParty": {
        "ResponsiblePartyType": "Principal Investigator",
        "ResponsiblePartyInvestigatorFullName": "William W. O'Neill",
        "ResponsiblePartyInvestigatorTitle": "Director, Center for Structural Heart Disease",
        "ResponsiblePartyInvestigatorAffiliation": "Henry Ford Health System"
      },
      "LeadSponsor": {
        "LeadSponsorName": "Henry Ford Health System",
        "LeadSponsorClass": "OTHER"
      }
    },
    "OversightModule": {
      "OversightHasDMC": "Yes",
      "IsFDARegulatedDrug": "Yes",
      "IsFDARegulatedDevice": "No",
      "IsUSExport": "No"
    },
    "DescriptionModule": {
      "BriefSummary": "The primary objective of this study is to determine whether the use of daily or weekly oral hydroxychloroquine (HCQ) therapy will prevent SARS-CoV-2 infection and COVID-19 viremia and clinical COVID-19 infection healthcare workers (HCW) and first responders (FR) (EMS, Fire, Police, bus drivers) in Metro Detroit, Michigan.\n\nPreventing COVID-19 transmission to HCW, FR, and Detroit Department of Transportation (DDOT) bus drivers is a critical step in preserving the health care and first responder force, the prevention of COVID-19 transmission in health care facilities, with the potential to preserve thousands of lives in addition to sustaining health care systems and civil services both nationally and globally. If efficacious, further studies on the use of hydroxychloroquine to prevent COVID-19 in the general population could be undertaken, with a potential impact on hundreds of thousands of lives.",
      "DetailedDescription": "The study will randomize a total of 3,000 healthcare workers (HCW) and first responders (FR) within Henry Ford Hospital System, the Detroit COVID Consortium in Detroit, Michigan. The participants will be randomized in a 1:1:1 blinded comparison of daily oral HCQ, weekly oral HCQ, or placebo. A fourth comparator group of HCW and FR who are currently on standard HCQ therapy will be recruited to assess the impact of weight-based daily dosing of HCQ as compared to the randomized arms.\n\nEligible participants who are asymptomatic for pre-specified signs and symptoms suggestive of COVID-19 infection will have a whole blood specimen obtained at study entry.\n\nParticipants will be provided with weekly dosing of hydroxychloroquine (HCQ) 400 mg po q weekly, daily dosing of HCQ 200 mg po q daily following a loading dose of 400 mg day 1, or placebo. Participants will receive monitoring at each study week visit to assess for the development of COVID-19 related symptoms, COVID-19 clinical disease, and medication side effects. At week 8 or if diagnosed positive, participants will provide additional samples of whole blood and complete the final study questionnaire.\n\nData including demographic, clinical results, work duties, location of main work area and possible exposures in the community will be collected through questionnaires and electronic medical record (EMR) review. Disease-specific, immunologic, and other serologic marker data will be obtained from stored samples.\n\nFive (5) 10 ml blood tubes consisting of 4 ethylenediaminetetraacetic acid (EDTA) and 1 Shield tubes of whole blood will be collected from each participant at the baseline/enrollment, week 4 and week 8 timepoints. The samples will be collected using standard aseptic procedures and will be stored in a 4°C refrigerator or cooler until transport to the research laboratory where the samples will be processed. Samples will be processed to serum plasma or cell components. Testing for SARS-CoV 2 will be done for study entry samples. Remainder of the samples will be stored in -80°C for whole blood/serum plasma and cell samples will be stored in liquid nitrogen for future testing."
    },
    "ConditionsModule": {
      "ConditionList": {
        "Condition": [
          "COVID-19",
          "Coronavirus",
          "Coronavirus Infections",
          "SARS-CoV 2"
        ]
      },
      "KeywordList": {
        "Keyword": [
          "COVID-19",
          "Coronavirus",
          "Healthcare Workers",
          "SARS-CoV 2",
          "First Responders",
          "Emergency Medical Technicians",
          "Paramedics",
          "Firefighters",
          "Police Officers",
          "Detroit",
          "Michigan",
          "Henry Ford Hospital"
        ]
      }
    },
    "DesignModule": {
      "StudyType": "Interventional",
      "PhaseList": {
        "Phase": [
          "Phase 3"
        ]
      },
      "DesignInfo": {
        "DesignAllocation": "Randomized",
        "DesignInterventionModel": "Parallel Assignment",
        "DesignInterventionModelDescription": "This is a prospective, multi-site study designed to evaluate whether the use of hydroxychloroquine in healthcare workers (HCW) and first responders (FR) in Detroit, Michigan, can prevent the acquisition, symptoms and clinical COVID-19 infection.\n\nThe study will randomize a total of 3,000 Healthcare Workers and First Responders, age ≥18 years or older, through the Henry Ford Health System, Detroit COVID Consortium. The participants who meeting study entry criteria and are not on HCQ prior to study enrollment will be randomized in a 1:1:1 blinded comparison of daily or weekly oral hydroxychloroquine versus oral placebo for 8 weeks.\n\nA fourth non-randomized comparator group will be enrolled in the study comprising of HCW who are chronically on HCQ as part of their standard of care for their autoimmune disease(s). This will be an open enrollment group and will provide information of chronic weight-based daily therapy of HCQ effectiveness as a prophylactic/preventive strategy.",
        "DesignPrimaryPurpose": "Prevention",
        "DesignMaskingInfo": {
          "DesignMasking": "Triple",
          "DesignMaskingDescription": "Blinded randomization will be performed by the Henry Ford Hospital Public Health Sciences investigators once the participants are determined to be eligible for enrollment. Randomization will be stratified by study site and risk of exposure based on location of work and type of work.\n\nOnce enrolled, each Participant will be assigned a unique identifier (detailed in the full protocol). This number, along with the assigned site number, will constitute the Subject Identifier (Subject ID).",
          "DesignWhoMaskedList": {
            "DesignWhoMasked": [
              "Participant",
              "Care Provider",
              "Investigator"
            ]
          }
        }
      },
      "EnrollmentInfo": {
        "EnrollmentCount": "3000",
        "EnrollmentType": "Anticipated"
      }
    },
    "ArmsInterventionsModule": {
      "ArmGroupList": {
        "ArmGroup": [{
            "ArmGroupLabel": "Study Drug - Daily Dose",
            "ArmGroupType": "Active Comparator",
            "ArmGroupDescription": "The daily hydroxychloroquine treatment arm will receive a 200 mg oral dose daily following day 1 dose of 400 mg orally once. This dose represents approximately half the standard weight-based dosing recommended for management of autoimmune diseases and therefore less likely to produce side effects than standard of care.",
            "ArmGroupInterventionList": {
              "ArmGroupInterventionName": [
                "Drug: Hydroxychloroquine - Daily Dosing",
                "Diagnostic Test: Monitoring Visit - Baseline",
                "Diagnostic Test: Monitoring Visit - Week 4",
                "Diagnostic Test: Monitoring Visit - Week 8",
                "Other: Weekly Assessment"
              ]
            }
          },
          {
            "ArmGroupLabel": "Study Drug - Weekly Dose",
            "ArmGroupType": "Active Comparator",
            "ArmGroupDescription": "The once weekly randomized treatment arm will receive the proposed dose of hydroxychloroquine for prophylaxis of malaria is 6.5 mg/kg per dose (maximum of 400mg per dose) administered orally weekly on the same day of each week. This is based on the recommended dose for prophylaxis of malaria.",
            "ArmGroupInterventionList": {
              "ArmGroupInterventionName": [
                "Drug: Hydroxychloroquine - Weekly Dosing",
                "Diagnostic Test: Monitoring Visit - Baseline",
                "Diagnostic Test: Monitoring Visit - Week 4",
                "Diagnostic Test: Monitoring Visit - Week 8",
                "Other: Weekly Assessment"
              ]
            }
          },
          {
            "ArmGroupLabel": "Placebo",
            "ArmGroupType": "Active Comparator",
            "ArmGroupDescription": "All treatment groups will receive placebo pills to have the patients take 2 pills a day. The randomized placebo arm will receive placebo pills made to resemble the daily dosing of HCQ. Similarly, the once a week treatment arm will receive placebo pills for the days not on HCQ medication.",
            "ArmGroupInterventionList": {
              "ArmGroupInterventionName": [
                "Other: Placebo oral tablet",
                "Diagnostic Test: Monitoring Visit - Baseline",
                "Diagnostic Test: Monitoring Visit - Week 4",
                "Diagnostic Test: Monitoring Visit - Week 8",
                "Other: Weekly Assessment"
              ]
            }
          },
          {
            "ArmGroupLabel": "Non-Randomized Active Comparator",
            "ArmGroupType": "Active Comparator",
            "ArmGroupDescription": "A non-randomized comparator group will be enrolled in the study comprising of healthcare workers and first responders who are chronically on oral hydroxychloroquine as part of their standard of care for their autoimmune disease(s). This will be an open enrollment group and will provide information of chronic weight-based daily therapy of HCQ effectiveness as a prophylactic/preventive strategy.",
            "ArmGroupInterventionList": {
              "ArmGroupInterventionName": [
                "Diagnostic Test: Monitoring Visit - Baseline",
                "Diagnostic Test: Monitoring Visit - Week 4",
                "Diagnostic Test: Monitoring Visit - Week 8",
                "Other: Weekly Assessment"
              ]
            }
          }
        ]
      },
      "InterventionList": {
        "Intervention": [{
            "InterventionType": "Drug",
            "InterventionName": "Hydroxychloroquine - Daily Dosing",
            "InterventionDescription": "The daily hydroxychloroquine treatment arm will receive a 200 mg oral dose daily following day 1 dose of 400 mg orally once. This dose represents approximately half the standard weight-based dosing recommended for management of autoimmune diseases and therefore less likely to produce side effects than standard of care.\n\nAll treatment groups will receive placebo pills to have the patients take 2 pills a day.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Study Drug - Daily Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Study Drug - Daily",
                "Daily Oral Dosing"
              ]
            }
          },
          {
            "InterventionType": "Drug",
            "InterventionName": "Hydroxychloroquine - Weekly Dosing",
            "InterventionDescription": "The once weekly randomized treatment arm will receive the proposed dose of hydroxychloroquine for prophylaxis of malaria is 6.5 mg/kg per dose (maximum of 400 mg per dose) administered orally weekly on the same day of each week. This is based on the recommended dose for prophylaxis of malaria\n\nAll treatment groups will receive placebo pills to have the patients take 2 pills a day.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Study Drug - Weekly Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Weekly Oral Dosing"
              ]
            }
          },
          {
            "InterventionType": "Other",
            "InterventionName": "Placebo oral tablet",
            "InterventionDescription": "Participants randomized to this arm will be provided with daily dosing of oral placebo to have the patients take 2 pills a day..\n\nParticipants will receive a monitoring phone call at 4 weeks post study entry to monitor for COVID-19 symptoms and medication side effects. At week 8, participants will provide additional samples of whole blood.\n\nAdditional studies will include serology, inflammatory and other disease associated markers. Clinical data and location of main work area will be collected.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Placebo"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Placebo"
              ]
            }
          },
          {
            "InterventionType": "Diagnostic Test",
            "InterventionName": "Monitoring Visit - Baseline",
            "InterventionDescription": "Face-to-face monitoring visit to obtain monitoring questionnaires to assess for COVID-19 symptoms/diagnosis, adherence and medication side effects, and collect study blood samples. Three (3) blood specimens will be collected from each Participant using the sterile procedure as routine standard of care. A total of five (5) 10 mL tubes of whole blood will be collected at each timepoint.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Non-Randomized Active Comparator",
                "Placebo",
                "Study Drug - Daily Dose",
                "Study Drug - Weekly Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Baseline Monitoring Visit"
              ]
            }
          },
          {
            "InterventionType": "Diagnostic Test",
            "InterventionName": "Monitoring Visit - Week 4",
            "InterventionDescription": "Face-to-face monitoring visit to obtain monitoring questionnaires to assess for COVID-19 symptoms/diagnosis, adherence and medication side effects, and collect study blood samples. Three (3) blood specimens will be collected from each Participant using the sterile procedure as routine standard of care. A total of five (5) 10 mL tubes of whole blood will be collected at each timepoint.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Non-Randomized Active Comparator",
                "Placebo",
                "Study Drug - Daily Dose",
                "Study Drug - Weekly Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Week 4 - Monitoring Visit"
              ]
            }
          },
          {
            "InterventionType": "Diagnostic Test",
            "InterventionName": "Monitoring Visit - Week 8",
            "InterventionDescription": "Face-to-face monitoring visit to obtain monitoring questionnaires to assess for COVID-19 symptoms/diagnosis, adherence and medication side effects, and collect study blood samples. Three (3) blood specimens will be collected from each Participant using the sterile procedure as routine standard of care. A total of five (5) 10 mL tubes of whole blood will be collected at each timepoint.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Non-Randomized Active Comparator",
                "Placebo",
                "Study Drug - Daily Dose",
                "Study Drug - Weekly Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Week 8 - Monitoring Visit"
              ]
            }
          },
          {
            "InterventionType": "Other",
            "InterventionName": "Weekly Assessment",
            "InterventionDescription": "Participants will be asked to contact the study team if COVID-19 infection is established at any time during the study. For study weeks 1,2,3,5,6 &7, Participants will receive a monitoring questionnaire to assess for COVID-19 symptoms/diagnosis, adherence and medication side effects. These monitoring visits will be done by telephone and/or electronic encounters (virtual visits, email), whichever method the patient prefers to encourage adherence to the monitoring.",
            "InterventionArmGroupLabelList": {
              "InterventionArmGroupLabel": [
                "Non-Randomized Active Comparator",
                "Placebo",
                "Study Drug - Daily Dose",
                "Study Drug - Weekly Dose"
              ]
            },
            "InterventionOtherNameList": {
              "InterventionOtherName": [
                "Monitoring Call"
              ]
            }
          }
        ]
      }
    },
    "OutcomesModule": {
      "PrimaryOutcomeList": {
        "PrimaryOutcome": [{
          "PrimaryOutcomeMeasure": "Reduction in the number of COVID-19 infections in healthcare workers.",
          "PrimaryOutcomeDescription": "Plan statistical analyses will include the assumption that up 10% of HCW at risk will become infected if no prophylactic treatment is provided. Therefore we expect that HCQ treatment arm will provide a reduction in the number of SARS-CoV 2 infections by 30%, with an expected study retention rate of 90%, a sample size of ~1500 participants per group, will have an 80% power to detect the difference at p=0.05.",
          "PrimaryOutcomeTimeFrame": "8 Weeks"
        }]
      }
    },
    "EligibilityModule": {
      "EligibilityCriteria": "Inclusion Criteria:\n\nParticipant is willing and able to provide informed consent.\nParticipant is 18-75 years of age.\nParticipant does not have symptoms of respiratory infection, including cough, fevers (temperature >38.0C), difficulty breathing, shortness of breath, chest pains, malaise, myalgia, headaches, nausea or vomiting, or other symptoms associated with COVID-19.\nParticipant is willing to provide blood samples for the study.\nSubject agrees to all aspects of the study.\nThe participant has no known allergies or contraindications (as stated in the consent form) to the use of hydroxychloroquine (HCQ) as noted in the exclusion criteria and Pharmacy sections.\n\nExclusion Criteria:\n\nDoes not meet inclusion criteria.\nParticipant unable or unwilling to provide informed consent.\nParticipant has any of the symptoms above or screens positive for possible COVID-19 disease.\nParticipant is currently enrolled in a study to evaluate an investigational drug.\nVulnerable populations deemed inappropriate for study by the site Principal Investigator.\nThe participant has a known allergy/hypersensitivity or has a medication or co-morbidity (including history of gastric bypass, epilepsy, cardiovascular disease or renal failure) that prevents the use of HCQ (see pharmacy section).\nThe participant is a woman of childbearing age whose pregnancy status is unknown and is not willing to use 2 methods of contraception.\nThe participant is pregnant or nursing.\nThe participant was diagnosed with retinopathy prior to study entry.\nThe participant has a diagnosis of porphyria prior to study entry.\nThe participant has renal failure with a creatinine clearance of <10 ml/min, pre-dialysis or requiring dialysis.\nThe Participant has a family history of Sudden Cardiac Death.\nThe participant is currently on diuretic therapy.\nThe participant has a history of known Prolonged QT Syndrome.\nThe participant is already taking any of the following medications: Abiraterone acetate, Agalsidase, Amodiaquine, Azithromycin, Conivaptan, Dabrafenib, Dacomitinib, Dapsone (Systemic), Digoxin, Enzalutamide, Fusidic Acid (Systemic), Idelalisib, Lanthanum, Lumefantrine, Mefloquine, Mifepristone, Mitotane, Pimozide, QT-prolonging Agents, Stiripentol).",
      "HealthyVolunteers": "Accepts Healthy Volunteers",
      "Gender": "All",
      "MinimumAge": "18 Years",
      "MaximumAge": "75 Years",
      "StdAgeList": {
        "StdAge": [
          "Adult",
          "Older Adult"
        ]
      }
    },
    "ContactsLocationsModule": {
      "CentralContactList": {
        "CentralContact": [{
            "CentralContactName": "Dee Dee Wang, MD",
            "CentralContactRole": "Contact",
            "CentralContactPhone": "313-574-2651",
            "CentralContactEMail": "whipcovid19@hfhs.org"
          },
          {
            "CentralContactName": "Laurie Nightengale, MD",
            "CentralContactRole": "Contact",
            "CentralContactPhone": "313-574-2651",
            "CentralContactEMail": "whipcovid19@hfhs.org"
          }
        ]
      },
      "OverallOfficialList": {
        "OverallOfficial": [{
            "OverallOfficialName": "William W O'Neill, MD",
            "OverallOfficialAffiliation": "Henry Ford Health System",
            "OverallOfficialRole": "Principal Investigator"
          },
          {
            "OverallOfficialName": "Dee Dee Wang, MD",
            "OverallOfficialAffiliation": "Henry Ford Health System",
            "OverallOfficialRole": "Study Director"
          }
        ]
      },
      "LocationList": {
        "Location": [{
            "LocationFacility": "Henry Ford Hospital",
            "LocationStatus": "Recruiting",
            "LocationCity": "Detroit",
            "LocationState": "Michigan",
            "LocationZip": "48202",
            "LocationCountry": "United States",
            "LocationContactList": {
              "LocationContact": [{
                  "LocationContactName": "Dee Dee Wang, MD",
                  "LocationContactRole": "Contact",
                  "LocationContactPhone": "313-574-2651",
                  "LocationContactEMail": "whipcovid19@hfhs.org"
                },
                {
                  "LocationContactName": "John McKinnon, MD",
                  "LocationContactRole": "Contact",
                  "LocationContactPhone": "313-574-2651",
                  "LocationContactEMail": "whipcovid19@hfhs.org"
                }
              ]
            }
          },
          {
            "LocationFacility": "Detroit Department of Transportation (DDOT)",
            "LocationStatus": "Recruiting",
            "LocationCity": "Detroit",
            "LocationState": "Michigan",
            "LocationZip": "48226",
            "LocationCountry": "United States"
          },
          {
            "LocationFacility": "Detroit Fire Department & Detroit EMS",
            "LocationStatus": "Recruiting",
            "LocationCity": "Detroit",
            "LocationState": "Michigan",
            "LocationZip": "48226",
            "LocationCountry": "United States"
          },
          {
            "LocationFacility": "Detroit Police Department",
            "LocationStatus": "Recruiting",
            "LocationCity": "Detroit",
            "LocationState": "Michigan",
            "LocationZip": "48226",
            "LocationCountry": "United States"
          }
        ]
      }
    },
    "ReferencesModule": {
      "ReferenceList": {
        "Reference": [{
            "ReferencePMID": "32083643",
            "ReferenceType": "background",
            "ReferenceCitation": "Bai Y, Yao L, Wei T, Tian F, Jin DY, Chen L, Wang M. Presumed Asymptomatic Carrier Transmission of COVID-19. JAMA. 2020 Feb 21. doi: 10.1001/jama.2020.2565. [Epub ahead of print]"
          },
          {
            "ReferencePMID": "32061333",
            "ReferenceType": "background",
            "ReferenceCitation": "Chang, Xu H, Rebaza A, Sharma L, Dela Cruz CS. Protecting health-care workers from subclinical coronavirus infection. Lancet Respir Med. 2020 Mar;8(3):e13. doi: 10.1016/S2213-2600(20)30066-7. Epub 2020 Feb 13."
          },
          {
            "ReferencePMID": "32194981",
            "ReferenceType": "background",
            "ReferenceCitation": "Liu J, Cao R, Xu M, Wang X, Zhang H, Hu H, Li Y, Hu Z, Zhong W, Wang M. Hydroxychloroquine, a less toxic derivative of chloroquine, is effective in inhibiting SARS-CoV-2 infection in vitro. Cell Discov. 2020 Mar 18;6:16. doi: 10.1038/s41421-020-0156-0. eCollection 2020."
          },
          {
            "ReferencePMID": "16115318",
            "ReferenceType": "background",
            "ReferenceCitation": "Vincent MJ, Bergeron E, Benjannet S, Erickson BR, Rollin PE, Ksiazek TG, Seidah NG, Nichol ST. Chloroquine is a potent inhibitor of SARS coronavirus infection and spread. Virol J. 2005 Aug 22;2:69."
          },
          {
            "ReferencePMID": "21221847",
            "ReferenceType": "background",
            "ReferenceCitation": "Ben-Zvi I, Kivity S, Langevitz P, Shoenfeld Y. Hydroxychloroquine: from malaria to autoimmunity. Clin Rev Allergy Immunol. 2012 Apr;42(2):145-53. doi: 10.1007/s12016-010-8243-x. Review."
          },
          {
            "ReferencePMID": "28556555",
            "ReferenceType": "background",
            "ReferenceCitation": "Mohammad S, Clowse MEB, Eudy AM, Criscione-Schreiber LG. Examination of Hydroxychloroquine Use and Hemolytic Anemia in G6PDH-Deficient Patients. Arthritis Care Res (Hoboken). 2018 Mar;70(3):481-485. doi: 10.1002/acr.23296. Epub 2018 Feb 9."
          },
          {
            "ReferencePMID": "32205204",
            "ReferenceType": "background",
            "ReferenceCitation": "Gautret P, Lagier JC, Parola P, Hoang VT, Meddeb L, Mailhe M, Doudier B, Courjon J, Giordanengo V, Vieira VE, Dupont HT, Honoré S, Colson P, Chabrière E, La Scola B, Rolain JM, Brouqui P, Raoult D. Hydroxychloroquine and azithromycin as a treatment of COVID-19: results of an open-label non-randomized clinical trial. Int J Antimicrob Agents. 2020 Mar 20:105949. doi: 10.1016/j.ijantimicag.2020.105949. [Epub ahead of print]"
          },
          {
            "ReferencePMID": "32150618",
            "ReferenceType": "background",
            "ReferenceCitation": "Yao X, Ye F, Zhang M, Cui C, Huang B, Niu P, Liu X, Zhao L, Dong E, Song C, Zhan S, Lu R, Li H, Tan W, Liu D. In Vitro Antiviral Activity and Projection of Optimized Dosing Design of Hydroxychloroquine for the Treatment of Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2). Clin Infect Dis. 2020 Mar 9. pii: ciaa237. doi: 10.1093/cid/ciaa237. [Epub ahead of print]"
          },
          {
            "ReferencePMID": "19188392",
            "ReferenceType": "background",
            "ReferenceCitation": "Lim HS, Im JS, Cho JY, Bae KS, Klein TA, Yeom JS, Kim TS, Choi JS, Jang IJ, Park JW. Pharmacokinetics of hydroxychloroquine and its clinical implications in chemoprophylaxis against malaria caused by Plasmodium vivax. Antimicrob Agents Chemother. 2009 Apr;53(4):1468-75. doi: 10.1128/AAC.00339-08. Epub 2009 Feb 2."
          }
        ]
      },
      "SeeAlsoLinkList": {
        "SeeAlsoLink": [{
          "SeeAlsoLinkLabel": "WHIP COVID-19 study website",
          "SeeAlsoLinkURL": "https://www.henryford.com/whip-covid-19"
        }]
      }
    },
    "IPDSharingStatementModule": {
      "IPDSharing": "No"
    }
  },
  "DocumentSection": {
    "LargeDocumentModule": {
      "LargeDocList": {
        "LargeDoc": [{
          "LargeDocTypeAbbrev": "Prot",
          "LargeDocHasProtocol": "Yes",
          "LargeDocHasSAP": "No",
          "LargeDocHasICF": "No",
          "LargeDocLabel": "Study Protocol",
          "LargeDocDate": "April 6, 2020",
          "LargeDocUploadDate": "04/06/2020 16:11",
          "LargeDocFilename": "Prot_000.pdf"
        }]
      }
    }
  },
  "DerivedSection": {
    "MiscInfoModule": {
      "VersionHolder": "April 26, 2020"
    },
    "InterventionBrowseModule": {
      "InterventionMeshList": {
        "InterventionMesh": [{
          "InterventionMeshId": "D000006886",
          "InterventionMeshTerm": "Hydroxychloroquine"
        }]
      },
      "InterventionAncestorList": {
        "InterventionAncestor": [{
            "InterventionAncestorId": "D000000962",
            "InterventionAncestorTerm": "Antimalarials"
          },
          {
            "InterventionAncestorId": "D000000981",
            "InterventionAncestorTerm": "Antiprotozoal Agents"
          },
          {
            "InterventionAncestorId": "D000000977",
            "InterventionAncestorTerm": "Antiparasitic Agents"
          },
          {
            "InterventionAncestorId": "D000000890",
            "InterventionAncestorTerm": "Anti-Infective Agents"
          },
          {
            "InterventionAncestorId": "D000004791",
            "InterventionAncestorTerm": "Enzyme Inhibitors"
          },
          {
            "InterventionAncestorId": "D000045504",
            "InterventionAncestorTerm": "Molecular Mechanisms of Pharmacological Action"
          },
          {
            "InterventionAncestorId": "D000018501",
            "InterventionAncestorTerm": "Antirheumatic Agents"
          }
        ]
      },
      "InterventionBrowseLeafList": {
        "InterventionBrowseLeaf": [{
            "InterventionBrowseLeafId": "M8523",
            "InterventionBrowseLeafName": "Hydroxychloroquine",
            "InterventionBrowseLeafAsFound": "Hydroxychloroquine",
            "InterventionBrowseLeafRelevance": "high"
          },
          {
            "InterventionBrowseLeafId": "M2861",
            "InterventionBrowseLeafName": "Antimalarials",
            "InterventionBrowseLeafRelevance": "low"
          },
          {
            "InterventionBrowseLeafId": "M2879",
            "InterventionBrowseLeafName": "Antiprotozoal Agents",
            "InterventionBrowseLeafRelevance": "low"
          },
          {
            "InterventionBrowseLeafId": "M2875",
            "InterventionBrowseLeafName": "Antiparasitic Agents",
            "InterventionBrowseLeafRelevance": "low"
          },
          {
            "InterventionBrowseLeafId": "M2795",
            "InterventionBrowseLeafName": "Anti-Infective Agents",
            "InterventionBrowseLeafRelevance": "low"
          },
          {
            "InterventionBrowseLeafId": "M19188",
            "InterventionBrowseLeafName": "Antirheumatic Agents",
            "InterventionBrowseLeafRelevance": "low"
          }
        ]
      },
      "InterventionBrowseBranchList": {
        "InterventionBrowseBranch": [{
            "InterventionBrowseBranchAbbrev": "Infe",
            "InterventionBrowseBranchName": "Anti-Infective Agents"
          },
          {
            "InterventionBrowseBranchAbbrev": "ARhu",
            "InterventionBrowseBranchName": "Antirheumatic Agents"
          },
          {
            "InterventionBrowseBranchAbbrev": "All",
            "InterventionBrowseBranchName": "All Drugs and Chemicals"
          }
        ]
      }
    },
    "ConditionBrowseModule": {
      "ConditionMeshList": {
        "ConditionMesh": [{
            "ConditionMeshId": "D000018352",
            "ConditionMeshTerm": "Coronavirus Infections"
          },
          {
            "ConditionMeshId": "D000045169",
            "ConditionMeshTerm": "Severe Acute Respiratory Syndrome"
          }
        ]
      },
      "ConditionAncestorList": {
        "ConditionAncestor": [{
            "ConditionAncestorId": "D000003333",
            "ConditionAncestorTerm": "Coronaviridae Infections"
          },
          {
            "ConditionAncestorId": "D000030341",
            "ConditionAncestorTerm": "Nidovirales Infections"
          },
          {
            "ConditionAncestorId": "D000012327",
            "ConditionAncestorTerm": "RNA Virus Infections"
          },
          {
            "ConditionAncestorId": "D000014777",
            "ConditionAncestorTerm": "Virus Diseases"
          },
          {
            "ConditionAncestorId": "D000012141",
            "ConditionAncestorTerm": "Respiratory Tract Infections"
          },
          {
            "ConditionAncestorId": "D000012140",
            "ConditionAncestorTerm": "Respiratory Tract Diseases"
          }
        ]
      },
      "ConditionBrowseLeafList": {
        "ConditionBrowseLeaf": [{
            "ConditionBrowseLeafId": "M8866",
            "ConditionBrowseLeafName": "Infection",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M4951",
            "ConditionBrowseLeafName": "Communicable Diseases",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M19074",
            "ConditionBrowseLeafName": "Coronavirus Infections",
            "ConditionBrowseLeafAsFound": "Coronavirus",
            "ConditionBrowseLeafRelevance": "high"
          },
          {
            "ConditionBrowseLeafId": "M24032",
            "ConditionBrowseLeafName": "Severe Acute Respiratory Syndrome",
            "ConditionBrowseLeafAsFound": "Coronavirus Infection",
            "ConditionBrowseLeafRelevance": "high"
          },
          {
            "ConditionBrowseLeafId": "M6379",
            "ConditionBrowseLeafName": "Emergencies",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M14938",
            "ConditionBrowseLeafName": "Syndrome",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M5138",
            "ConditionBrowseLeafName": "Coronaviridae Infections",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M16105",
            "ConditionBrowseLeafName": "Virus Diseases",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M13732",
            "ConditionBrowseLeafName": "RNA Virus Infections",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M13561",
            "ConditionBrowseLeafName": "Respiratory Tract Infections",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "M13560",
            "ConditionBrowseLeafName": "Respiratory Tract Diseases",
            "ConditionBrowseLeafRelevance": "low"
          },
          {
            "ConditionBrowseLeafId": "T5212",
            "ConditionBrowseLeafName": "Severe Acute Respiratory Syndrome",
            "ConditionBrowseLeafAsFound": "Coronavirus Infection",
            "ConditionBrowseLeafRelevance": "high"
          }
        ]
      },
      "ConditionBrowseBranchList": {
        "ConditionBrowseBranch": [{
            "ConditionBrowseBranchAbbrev": "BC01",
            "ConditionBrowseBranchName": "Bacterial and Fungal Diseases"
          },
          {
            "ConditionBrowseBranchAbbrev": "All",
            "ConditionBrowseBranchName": "All Conditions"
          },
          {
            "ConditionBrowseBranchAbbrev": "BC02",
            "ConditionBrowseBranchName": "Viral Diseases"
          },
          {
            "ConditionBrowseBranchAbbrev": "BC08",
            "ConditionBrowseBranchName": "Respiratory Tract (Lung and Bronchial) Diseases"
          },
          {
            "ConditionBrowseBranchAbbrev": "BC23",
            "ConditionBrowseBranchName": "Symptoms and General Pathology"
          },
          {
            "ConditionBrowseBranchAbbrev": "Rare",
            "ConditionBrowseBranchName": "Rare Diseases"
          }
        ]
      }
    }
  }
}
```
### After parsing:
```
{
  "@type": "ClinicalTrial",
  "_id": "NCT04341441",
  "identifier": "NCT04341441",
  "identifierSource": "ClinicalTrials.gov",
  "url": "https:\\/\\/clinicaltrials.gov\\/ct2\\/show\\/NCT04341441",
  "name": "Will Hydroxychloroquine Impede or Prevent COVID-19: WHIP COVID-19 Study",
  "alternateName": ["WHIP COVID-19", "Will Hydroxychloroquine Impede or Prevent COVID-19"],
  "abstract": "The primary objective of this study is to determine whether the use of daily or weekly oral hydroxychloroquine (HCQ) therapy will prevent SARS-CoV-2 infection and COVID-19 viremia and clinical COVID-19 infection healthcare workers (HCW) and first responders (FR) (EMS, Fire, Police, bus drivers) in Metro Detroit, Michigan.\\n\\nPreventing COVID-19 transmission to HCW, FR, and Detroit Department of Transportation (DDOT) bus drivers is a critical step in preserving the health care and first responder force, the prevention of COVID-19 transmission in health care facilities, with the potential to preserve thousands of lives in addition to sustaining health care systems and civil services both nationally and globally. If efficacious, further studies on the use of hydroxychloroquine to prevent COVID-19 in the general population could be undertaken, with a potential impact on hundreds of thousands of lives.",
  "description": "The study will randomize a total of 3,000 healthcare workers (HCW) and first responders (FR) within Henry Ford Hospital System, the Detroit COVID Consortium in Detroit, Michigan. The participants will be randomized in a 1:1:1 blinded comparison of daily oral HCQ, weekly oral HCQ, or placebo. A fourth comparator group of HCW and FR who are currently on standard HCQ therapy will be recruited to assess the impact of weight-based daily dosing of HCQ as compared to the randomized arms.\\n\\nEligible participants who are asymptomatic for pre-specified signs and symptoms suggestive of COVID-19 infection will have a whole blood specimen obtained at study entry.\\n\\nParticipants will be provided with weekly dosing of hydroxychloroquine (HCQ) 400 mg po q weekly, daily dosing of HCQ 200 mg po q daily following a loading dose of 400 mg day 1, or placebo. Participants will receive monitoring at each study week visit to assess for the development of COVID-19 related symptoms, COVID-19 clinical disease, and medication side effects. At week 8 or if diagnosed positive, participants will provide additional samples of whole blood and complete the final study questionnaire.\\n\\nData including demographic, clinical results, work duties, location of main work area and possible exposures in the community will be collected through questionnaires and electronic medical record (EMR) review. Disease-specific, immunologic, and other serologic marker data will be obtained from stored samples.\\n\\nFive (5) 10 ml blood tubes consisting of 4 ethylenediaminetetraacetic acid (EDTA) and 1 Shield tubes of whole blood will be collected from each participant at the baseline\\/enrollment, week 4 and week 8 timepoints. The samples will be collected using standard aseptic procedures and will be stored in a 4\\u00b0C refrigerator or cooler until transport to the research laboratory where the samples will be processed. Samples will be processed to serum plasma or cell components. Testing for SARS-CoV 2 will be done for study entry samples. Remainder of the samples will be stored in -80\\u00b0C for whole blood\\/serum plasma and cell samples will be stored in liquid nitrogen for future testing.",
  "sponsor": [{
    "@type": "Organization",
    "name": "Henry Ford Health System",
    "class": "other",
    "role": "lead sponsor"
  }],
  "author": [{
    "@type": "Person",
    "name": "William W. O\'Neill",
    "affiliation": "Henry Ford Health System",
    "title": "Director, Center for Structural Heart Disease",
    "role": "Principal Investigator"
  }, {
    "@type": "Person",
    "name": "Dee Dee Wang, MD",
    "role": "Study Director",
    "affiliation": "Henry Ford Health System"
  }],
  "studyStatus": {
    "@type": "StudyStatus",
    "status": "recruiting",
    "statusDate": "April 2020",
    "statusExpanded": false,
    "enrollmentCount": 3000,
    "enrollmentType": "anticipated"
  },
  "studyEvent": [{
    "@type": "StudyEvent",
    "studyEventType": "start",
    "studyEventDate": "April 7, 2020",
    "studyEventDateType": "actual"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "primary completion",
    "studyEventDate": "June 30, 2020",
    "studyEventDateType": "anticipated"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "completion",
    "studyEventDate": "April 30, 2021",
    "studyEventDateType": "anticipated"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "first posting to clinicaltrials.gov",
    "studyEventDate": "April 10, 2020",
    "studyEventDateType": "actual"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "last posting to clinicaltrials.gov",
    "studyEventDate": "April 15, 2020",
    "studyEventDateType": "actual"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "first submission",
    "studyEventDate": "April 7, 2020"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "first submission that met quality control criteria",
    "studyEventDate": "April 7, 2020"
  }, {
    "@type": "StudyEvent",
    "studyEventType": "last update submission",
    "studyEventDate": "April 13, 2020"
  }],
  "hasResults": false,
  "dateCreated": "2020-04-07",
  "datePublished": "2020-04-10",
  "dateModified": "2020-04-15",
  "curatedBy": {
    "@type": "Organization",
    "name": "ClinicalTrials.gov",
    "url": "https:\\/\\/clinicaltrials.gov\\/ct2\\/results?cond=COVID-19",
    "versionDate": "2020-04-26"
  },
  "healthCondition": ["COVID-19", "Coronavirus", "Coronavirus Infections", "SARS-CoV 2"],
  "keywords": ["COVID-19", "Coronavirus", "Healthcare Workers", "SARS-CoV 2", "First Responders", "Emergency Medical Technicians", "Paramedics", "Firefighters", "Police Officers", "Detroit", "Michigan", "Henry Ford Hospital"],
  "studyDesign": [{
    "@type": "StudyDesign",
    "studyType": "interventional",
    "designAllocation": "randomized",
    "designModel": "parallel assignment",
    "designPrimaryPurpose": "prevention",
    "phase": ["Phase 3"]
  }],
  "outcome": [{
    "@type": "Outcome",
    "outcomeMeasure": "Reduction in the number of COVID-19 infections in healthcare workers.",
    "outcomeTimeFrame": "8 Weeks",
    "outcomeType": "primary"
  }],
  "eligibilityCriteria": [{
    "@type": "Eligibility",
    "inclusionCriteria": ["Participant is willing and able to provide informed consent.", "Participant is 18-75 years of age.", "Participant does not have symptoms of respiratory infection, including cough, fevers (temperature >38.0C), difficulty breathing, shortness of breath, chest pains, malaise, myalgia, headaches, nausea or vomiting, or other symptoms associated with COVID-19.", "Participant is willing to provide blood samples for the study.", "Subject agrees to all aspects of the study.", "The participant has no known allergies or contraindications (as stated in the consent form) to the use of hydroxychloroquine (HCQ) as noted in the exclusion criteria and Pharmacy sections."],
    "exclusionCriteria": ["Does not meet inclusion criteria.", "Participant unable or unwilling to provide informed consent.", "Participant has any of the symptoms above or screens positive for possible COVID-19 disease.", "Participant is currently enrolled in a study to evaluate an investigational drug.", "Vulnerable populations deemed inappropriate for study by the site Principal Investigator.", "The participant has a known allergy\\/hypersensitivity or has a medication or co-morbidity (including history of gastric bypass, epilepsy, cardiovascular disease or renal failure) that prevents the use of HCQ (see pharmacy section).", "The participant is a woman of childbearing age whose pregnancy status is unknown and is not willing to use 2 methods of contraception.", "The participant is pregnant or nursing.", "The participant was diagnosed with retinopathy prior to study entry.", "The participant has a diagnosis of porphyria prior to study entry.", "The participant has renal failure with a creatinine clearance of <10 ml\\/min, pre-dialysis or requiring dialysis.", "The Participant has a family history of Sudden Cardiac Death.", "The participant is currently on diuretic therapy.", "The participant has a history of known Prolonged QT Syndrome.", "The participant is already taking any of the following medications: Abiraterone acetate, Agalsidase, Amodiaquine, Azithromycin, Conivaptan, Dabrafenib, Dacomitinib, Dapsone (Systemic), Digoxin, Enzalutamide, Fusidic Acid (Systemic), Idelalisib, Lanthanum, Lumefantrine, Mefloquine, Mifepristone, Mitotane, Pimozide, QT-prolonging Agents, Stiripentol)."],
    "minimumAge": "18 years",
    "maximumAge": "75 years",
    "gender": "all",
    "healthyVolunteers": null,
    "stdAge": ["adult", "older adult"]
  }],
  "isBasedOn": [{
    "@type": "Protocol",
    "name": "Prot_000.pdf",
    "datePublished": "2020-04-06",
    "description": "Study Protocol for Clinical Trial NCT04341441",
    "identifier": "NCT04341441_Prot_000.pdf",
    "type": "ClinicalTrial",
    "url": "https:\\/\\/clinicaltrials.gov\\/ct2\\/show\\/NCT04341441"
  }],
  "relatedTo": [{
    "@type": "Publication",
    "identifier": "pmid32083643",
    "pmid": "32083643",
    "citation": "Bai Y, Yao L, Wei T, Tian F, Jin DY, Chen L, Wang M. Presumed Asymptomatic Carrier Transmission of COVID-19. JAMA. 2020 Feb 21. doi: 10.1001\\/jama.2020.2565. [Epub ahead of print]"
  }, {
    "@type": "Publication",
    "identifier": "pmid32061333",
    "pmid": "32061333",
    "citation": "Chang, Xu H, Rebaza A, Sharma L, Dela Cruz CS. Protecting health-care workers from subclinical coronavirus infection. Lancet Respir Med. 2020 Mar;8(3):e13. doi: 10.1016\\/S2213-2600(20)30066-7. Epub 2020 Feb 13."
  }, {
    "@type": "Publication",
    "identifier": "pmid32194981",
    "pmid": "32194981",
    "citation": "Liu J, Cao R, Xu M, Wang X, Zhang H, Hu H, Li Y, Hu Z, Zhong W, Wang M. Hydroxychloroquine, a less toxic derivative of chloroquine, is effective in inhibiting SARS-CoV-2 infection in vitro. Cell Discov. 2020 Mar 18;6:16. doi: 10.1038\\/s41421-020-0156-0. eCollection 2020."
  }, {
    "@type": "Publication",
    "identifier": "pmid16115318",
    "pmid": "16115318",
    "citation": "Vincent MJ, Bergeron E, Benjannet S, Erickson BR, Rollin PE, Ksiazek TG, Seidah NG, Nichol ST. Chloroquine is a potent inhibitor of SARS coronavirus infection and spread. Virol J. 2005 Aug 22;2:69."
  }, {
    "@type": "Publication",
    "identifier": "pmid21221847",
    "pmid": "21221847",
    "citation": "Ben-Zvi I, Kivity S, Langevitz P, Shoenfeld Y. Hydroxychloroquine: from malaria to autoimmunity. Clin Rev Allergy Immunol. 2012 Apr;42(2):145-53. doi: 10.1007\\/s12016-010-8243-x. Review."
  }, {
    "@type": "Publication",
    "identifier": "pmid28556555",
    "pmid": "28556555",
    "citation": "Mohammad S, Clowse MEB, Eudy AM, Criscione-Schreiber LG. Examination of Hydroxychloroquine Use and Hemolytic Anemia in G6PDH-Deficient Patients. Arthritis Care Res (Hoboken). 2018 Mar;70(3):481-485. doi: 10.1002\\/acr.23296. Epub 2018 Feb 9."
  }, {
    "@type": "Publication",
    "identifier": "pmid32205204",
    "pmid": "32205204",
    "citation": "Gautret P, Lagier JC, Parola P, Hoang VT, Meddeb L, Mailhe M, Doudier B, Courjon J, Giordanengo V, Vieira VE, Dupont HT, Honor\\u00e9 S, Colson P, Chabri\\u00e8re E, La Scola B, Rolain JM, Brouqui P, Raoult D. Hydroxychloroquine and azithromycin as a treatment of COVID-19: results of an open-label non-randomized clinical trial. Int J Antimicrob Agents. 2020 Mar 20:105949. doi: 10.1016\\/j.ijantimicag.2020.105949. [Epub ahead of print]"
  }, {
    "@type": "Publication",
    "identifier": "pmid32150618",
    "pmid": "32150618",
    "citation": "Yao X, Ye F, Zhang M, Cui C, Huang B, Niu P, Liu X, Zhao L, Dong E, Song C, Zhan S, Lu R, Li H, Tan W, Liu D. In Vitro Antiviral Activity and Projection of Optimized Dosing Design of Hydroxychloroquine for the Treatment of Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2). Clin Infect Dis. 2020 Mar 9. pii: ciaa237. doi: 10.1093\\/cid\\/ciaa237. [Epub ahead of print]"
  }, {
    "@type": "Publication",
    "identifier": "pmid19188392",
    "pmid": "19188392",
    "citation": "Lim HS, Im JS, Cho JY, Bae KS, Klein TA, Yeom JS, Kim TS, Choi JS, Jang IJ, Park JW. Pharmacokinetics of hydroxychloroquine and its clinical implications in chemoprophylaxis against malaria caused by Plasmodium vivax. Antimicrob Agents Chemother. 2009 Apr;53(4):1468-75. doi: 10.1128\\/AAC.00339-08. Epub 2009 Feb 2."
  }],
  "studyLocation": [{
    "@type": "Place",
    "name": "Henry Ford Hospital",
    "studyLocationCity": "Detroit",
    "studyLocationCountry": "United States",
    "studyLocationState": "Michigan",
    "studyLocationStatus": "recruiting"
  }, {
    "@type": "Place",
    "name": "Detroit Department of Transportation (DDOT)",
    "studyLocationCity": "Detroit",
    "studyLocationCountry": "United States",
    "studyLocationState": "Michigan",
    "studyLocationStatus": "recruiting"
  }, {
    "@type": "Place",
    "name": "Detroit Fire Department & Detroit EMS",
    "studyLocationCity": "Detroit",
    "studyLocationCountry": "United States",
    "studyLocationState": "Michigan",
    "studyLocationStatus": "recruiting"
  }, {
    "@type": "Place",
    "name": "Detroit Police Department",
    "studyLocationCity": "Detroit",
    "studyLocationCountry": "United States",
    "studyLocationState": "Michigan",
    "studyLocationStatus": "recruiting"
  }],
  "armGroup": [{
    "@type": "ArmGroup",
    "name": "Study Drug - Daily Dose",
    "description": "The daily hydroxychloroquine treatment arm will receive a 200 mg oral dose daily following day 1 dose of 400 mg orally once. This dose represents approximately half the standard weight-based dosing recommended for management of autoimmune diseases and therefore less likely to produce side effects than standard of care.",
    "role": "active comparator",
    "intervention": [{
      "@type": "Intervention",
      "category": "drug",
      "name": "hydroxychloroquine - daily dosing",
      "description": "the daily hydroxychloroquine treatment arm will receive a 200 mg oral dose daily following day 1 dose of 400 mg orally once. this dose represents approximately half the standard weight-based dosing recommended for management of autoimmune diseases and therefore less likely to produce side effects than standard of care.\\n\\nall treatment groups will receive placebo pills to have the patients take 2 pills a day."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - baseline",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 4",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 8",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "other",
      "name": "weekly assessment",
      "description": "participants will be asked to contact the study team if covid-19 infection is established at any time during the study. for study weeks 1,2,3,5,6 &7, participants will receive a monitoring questionnaire to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects. these monitoring visits will be done by telephone and\\/or electronic encounters (virtual visits, email), whichever method the patient prefers to encourage adherence to the monitoring."
    }]
  }, {
    "@type": "ArmGroup",
    "name": "Study Drug - Weekly Dose",
    "description": "The once weekly randomized treatment arm will receive the proposed dose of hydroxychloroquine for prophylaxis of malaria is 6.5 mg\\/kg per dose (maximum of 400mg per dose) administered orally weekly on the same day of each week. This is based on the recommended dose for prophylaxis of malaria.",
    "role": "active comparator",
    "intervention": [{
      "@type": "Intervention",
      "category": "drug",
      "name": "hydroxychloroquine - weekly dosing",
      "description": "the once weekly randomized treatment arm will receive the proposed dose of hydroxychloroquine for prophylaxis of malaria is 6.5 mg\\/kg per dose (maximum of 400 mg per dose) administered orally weekly on the same day of each week. this is based on the recommended dose for prophylaxis of malaria\\n\\nall treatment groups will receive placebo pills to have the patients take 2 pills a day."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - baseline",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 4",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 8",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "other",
      "name": "weekly assessment",
      "description": "participants will be asked to contact the study team if covid-19 infection is established at any time during the study. for study weeks 1,2,3,5,6 &7, participants will receive a monitoring questionnaire to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects. these monitoring visits will be done by telephone and\\/or electronic encounters (virtual visits, email), whichever method the patient prefers to encourage adherence to the monitoring."
    }]
  }, {
    "@type": "ArmGroup",
    "name": "Placebo",
    "description": "All treatment groups will receive placebo pills to have the patients take 2 pills a day. The randomized placebo arm will receive placebo pills made to resemble the daily dosing of HCQ. Similarly, the once a week treatment arm will receive placebo pills for the days not on HCQ medication.",
    "role": "active comparator",
    "intervention": [{
      "@type": "Intervention",
      "category": "other",
      "name": "placebo oral tablet",
      "description": "participants randomized to this arm will be provided with daily dosing of oral placebo to have the patients take 2 pills a day..\\n\\nparticipants will receive a monitoring phone call at 4 weeks post study entry to monitor for covid-19 symptoms and medication side effects. at week 8, participants will provide additional samples of whole blood.\\n\\nadditional studies will include serology, inflammatory and other disease associated markers. clinical data and location of main work area will be collected."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - baseline",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 4",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 8",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "other",
      "name": "weekly assessment",
      "description": "participants will be asked to contact the study team if covid-19 infection is established at any time during the study. for study weeks 1,2,3,5,6 &7, participants will receive a monitoring questionnaire to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects. these monitoring visits will be done by telephone and\\/or electronic encounters (virtual visits, email), whichever method the patient prefers to encourage adherence to the monitoring."
    }]
  }, {
    "@type": "ArmGroup",
    "name": "Non-Randomized Active Comparator",
    "description": "A non-randomized comparator group will be enrolled in the study comprising of healthcare workers and first responders who are chronically on oral hydroxychloroquine as part of their standard of care for their autoimmune disease(s). This will be an open enrollment group and will provide information of chronic weight-based daily therapy of HCQ effectiveness as a prophylactic\\/preventive strategy.",
    "role": "active comparator",
    "intervention": [{
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - baseline",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 4",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "diagnostic test",
      "name": "monitoring visit - week 8",
      "description": "face-to-face monitoring visit to obtain monitoring questionnaires to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects, and collect study blood samples. three (3) blood specimens will be collected from each participant using the sterile procedure as routine standard of care. a total of five (5) 10 ml tubes of whole blood will be collected at each timepoint."
    }, {
      "@type": "Intervention",
      "category": "other",
      "name": "weekly assessment",
      "description": "participants will be asked to contact the study team if covid-19 infection is established at any time during the study. for study weeks 1,2,3,5,6 &7, participants will receive a monitoring questionnaire to assess for covid-19 symptoms\\/diagnosis, adherence and medication side effects. these monitoring visits will be done by telephone and\\/or electronic encounters (virtual visits, email), whichever method the patient prefers to encourage adherence to the monitoring."
    }]
  }]
}
```
