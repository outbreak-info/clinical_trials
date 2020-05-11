import biothings.hub.dataload.uploader
import os

import biothings
import config
biothings.config_for_app(config)


# when code is exported, import becomes relative
try:
    from clinical_trials.parser import load_annotations as parser_func
except ImportError:
    from .parser import load_annotations as parser_func


class ClinicalTrialUploader(biothings.hub.dataload.uploader.BaseSourceUploader):

    main_source = "clinical_trials"
    name = "clinicaltrials"
    __metadata__ = {"src_meta": {}}
    idconverter = None
    storage_class = biothings.hub.dataload.storage.BasicStorage

    def load_data(self, data_folder):
        if data_folder:
            self.logger.info("Load data from directory: '%s'", data_folder)
        return parser_func()

    @classmethod
    def get_mapping(klass):
        return {
            "@type": {
                "normalizer": "keyword_lowercase_normalizer",
                "type": "keyword"
            },
            "abstract": {
                "type": "text"
            },
            "alternateName": {
                "type": "text"
            },
            "armGroup": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "role": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "intervention": {
                        "properties": {
                            "@type": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword"
                            },
                            "name": {
                                "type": "text"
                            },
                            "category": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword"
                            },
                            "description": {
                                "type": "text"
                            }
                        }
                    }
                }
            },
            "author": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "affiliation": {
                        "properties": {
                            "name": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword"
                            }
                        }
                    },
                    "name": {
                        "type": "text"
                    },
                    "title": {
                        "type": "text"
                    },
                    "role": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    }
                }},
            "curatedBy": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text"
                    },
                    "url": {
                        "type": "text"
                    },
                    "versionDate": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                }
            },
            "dateCreated": {
                "type": "keyword"
            },
            "dateModified": {
                "type": "keyword"
            },
            "datePublished": {
                "type": "keyword"
            },
            "description": {
                "type": "text"
            },
            "eligibilityCriteria": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "inclusionCriteria": {
                        "type": "text"
                    },
                    "exclusionCriteria": {
                        "type": "text"
                    },
                    "minimumAge": {
                        "type": "text"
                    },
                    "maximumAge": {
                        "type": "text"
                    },
                    "gender": {
                        "type": "text"
                    },
                    "healthyVolunteers": {
                        "type": "boolean"
                    },
                    "stdAge": {
                        "type": "text"
                    }
                }
            },
            "hasResults": {
                "type": "boolean"
            },
            "healthCondition": {
                "type": "text"
            },
            "identifier": {
                "normalizer": "keyword_lowercase_normalizer",
                "type": "keyword"
            },
            "identifierSource": {
                "normalizer": "keyword_lowercase_normalizer",
                "type": "keyword"
            },
            "interventionText": {
                "type": "text"
            },
            "interventions": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text"
                    },
                    "category": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "description": {
                        "type": "text"
                    }
                }
            },
            "isBasedOn": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "identifier": {
                        "type": "text"
                    },
                    "name": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "url": {
                        "type": "text"
                    },
                    "datePublished": {
                        "type": "text"
                    }
                }
            },
            "keywords": {
                "normalizer": "keyword_lowercase_normalizer",
                "type": "keyword",
                "copy_to": ["all"]
            },
            "name": {
                "type": "text"
            },
            "outcome": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "outcomeMeasure": {
                        "type": "text"
                    },
                    "outcomeTimeFrame": {
                        "type": "text"
                    },
                    "outcomeType": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                }
            },
            "relatedTo": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "identifier": {
                        "type": "text"
                    },
                    "pmid": {
                        "type": "text"
                    },
                    "url": {
                        "type": "text"
                    },
                    "citation": {
                        "type": "text"
                    }
                }
            },
            "sponsor": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "name": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "class": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "role": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    }
                }
            },
            "studyDesign": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "studyType": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "designAllocation": {
                        "type": "text"
                    },
                    "studyDesignText": {
                        "type": "text"
                    },
                    "designModel": {
                        "type": "text"
                    },
                    "designTimePerspective": {
                        "type": "text"
                    },
                    "designPrimaryPurpose": {
                        "type": "text"
                    },
                    "designWhoMasked": {
                        "type": "text"
                    },
                    "phase": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "phaseNumber": {
                        "type": "half_float"
                    }
                }
            },
            "studyEvent": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "studyEventType": {
                        "type": "text"
                    },
                    "studyEventDate": {
                        "type": "text"
                    },
                    "studyEventDateType": {
                        "type": "text"
                    }
                }
            },
            "studyLocation": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text"
                    },
                    "studyLocationCity": {
                        "type": "text"
                    },
                    "studyLocationState": {
                        "type": "text"
                    },
                    "studyLocationCountry": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "studyLocationStatus": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    }
                }
            },
            "studyStatus": {
                "properties": {
                    "@type": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "status": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword"
                    },
                    "statusDate": {
                        "type": "text"
                    },
                    "whyStopped": {
                        "type": "text"
                    },
                    "statusExpanded": {
                        "type": "boolean"
                    },
                    "enrollmentCount": {
                        "type": "integer"
                    },
                    "enrollmentType": {
                        "type": "text"
                    }
                }
            },
            "url": {
                "type": "text"
            }
        }
