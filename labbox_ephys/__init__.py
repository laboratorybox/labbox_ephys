from .extractors import DiskReadMda, readmda, writemda32, writemda64, writemda, appendmda
from .extractors import MdaRecordingExtractor, MdaSortingExtractor, LabboxEphysRecordingExtractor, LabboxEphysSortingExtractor, load_recording, load_recording_doc
from .utils import database, dbcollection, sort_recording_from_database, remote_job_handler, job_cache
from .sorters import sorters
from .processing_daemon import ProcessingDaemon

def hither2_job_config():
    return dict(
        container=True,
        job_handler=remote_job_handler(),
        # job_cache=job_cache() # need to implement local job cache in case where results are downloaded ???? think about it
    )