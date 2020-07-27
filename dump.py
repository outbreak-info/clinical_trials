import os

import biothings, config
biothings.config_for_app(config)
from config import DATA_ARCHIVE_ROOT

import biothings.hub.dataload.dumper


class ClinicalTrialDumper(biothings.hub.dataload.dumper.DummyDumper):

    SRC_NAME = "clinical_trials"
    SRC_URLS = ["https://clinicaltrials.gov/api/query/full_studies?expr=(%22covid-19%22%20OR%20%22sars-cov-2%22)&min_rnk=1&max_rnk=100&fmt=json", "https://www.naturalearthdata.com/downloads/10m-cultural-vectors/"]
    # override in subclass accordingly
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    SCHEDULE = "20 7 * * *"  # daily at 14:20UTC/7:20PT
