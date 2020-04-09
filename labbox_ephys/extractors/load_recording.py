from .labboxephysrecordingextractor import LabboxEphysRecordingExtractor
from ..utils import dbcollection

def load_recording_doc(*, recording_id=None):
    docs = list(dbcollection('recordings').find(dict(recording_id=recording_id)))
    if len(docs) == 0:
        return None
    rdoc = docs[0]
    return rdoc

def load_recording(*, recording_id=None, download=False):
    print('---------- load_recording', download)
    rdoc = load_recording_doc(recording_id=recording_id)
    if rdoc is None:
        print(f'Unable to load recording doc with ID: {recording_id}')
        return None
    recording = LabboxEphysRecordingExtractor(rdoc['recording'], download=download)
    return recording
