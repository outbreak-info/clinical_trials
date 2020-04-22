# umin-clinical-trials
Parser to import COVID-19 clinical trials from https://www.umin.ac.jp/ctr/ into [outbreak.info](https://outbreak.info/resources?type=ClinicalTrial)

## About the data
The clinical trials metadata is sourced from the [UMIN Clinical Trials Registry](https://www.umin.ac.jp/ctr/) and is updated weekly.  

## Parsing
Example initial record:
```
{
          "TrialID": "ChiCTR2000031104",
          "Last Refreshed on": 1584921600000,
          "Public title": "Study for metagenomics of patients with novel coronavirus pneumonia (COVID-19)",
          "Scientific title": "Study for metagenomics of patients with novel coronavirus pneumonia (COVID-19)                                                                                                                                                                                 ",
          "Acronym": null,
          "Primary sponsor": "The Fifth Affiliated Hospital of Sun Yat-Sen University",
          "Date registration": 1584835200000,
          "Date registration3": 20200322,
          "Export date": "4\\/22\\/2020 12:57:03 PM",
          "Source Register": "ChiCTR",
          "web address": "http:\\/\\/www.chictr.org.cn\\/showproj.aspx?proj=51185",
          "Recruitment Status": "Recruiting",
          "other records": "No",
          "Inclusion agemin": 0,
          "Inclusion agemax": 90,
          "Inclusion gender": "Both",
          "Date enrollement": 1580860800000,
          "Target size": "Diagnosed Group:98;Suspending Group:102;",
          "Study type": "Observational study",
          "Study design": "Sequential",
          "Phase": null,
          "Countries": "China",
          "Contact Firstname": "Pengfei Pang",
          "Contact Lastname": null,
          "Contact Address": "52 Meihua Road East, Xiangzhou District, Zhuhai, Guangdong, China",
          "Contact Email": "pangpf@mail.sysu.edu.cn",
          "Contact Tel": "+86 18902536585",
          "Contact Affiliation": "The Fifth Affiliated Hospital of Sun Yat-Sen University ",
          "Inclusion Criteria": "Inclusion criteria: (1) Fever patients;\\r<br>(2) peoples who need to screen the novel coronavirus;\\r<br>(3) patients for possible infection with novel coronavirus through High throughput sequencing of pathogens;\\r<br>(4) Age and gender are not limited;\\r<br>(",
          "Exclusion Criteria": "Exclusion criteria: (1) limited sample size;                                                                          \\r<br>(2) Lack of sample information;\\r<br>(3) unable or failure to detect due to human error;\\r<br>(4) Abnormal results or failure in detec",
          "Condition": "Novel Coronavirus Pneumonia (COVID-19)",
          "Intervention": "Diagnosed Group:Nil;Suspending Group:Nil;",
          "Primary outcome": "Metagenomics Sequencing;",
          "results date posted": null,
          "results date completed": null,
          "results url link": null,
          "Retrospective flag": "No",
          "Bridging flag truefalse": false,
          "Bridged type": "          ",
          "results yes no": null
        }
```
