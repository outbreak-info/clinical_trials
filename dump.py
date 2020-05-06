import os

import biothings, config
biothings.config_for_app(config)
from config import DATA_ARCHIVE_ROOT

import biothings.hub.dataload.dumper


class ClinicalTrialDumper(biothings.hub.dataload.dumper.DummyDumper):

    SRC_NAME = "clinical_trials"
    # override in subclass accordingly
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    SCHEDULE = None  # crontab format schedule, if None, won't be scheduled
