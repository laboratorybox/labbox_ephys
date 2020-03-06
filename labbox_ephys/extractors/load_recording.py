from .labboxephysrecordingextractor import LabboxEphysRecordingExtractor
from ..utils import dbcollection

def load_recording_doc(*, recording_id=None):
    docs = list(dbcollection('recordings').find(dict(recording_id=recording_id)))
    rdoc = docs[0]
    return rdoc

def load_recording(*, recording_id=None, download=True):
    rdoc = load_recording_doc(recording_id=recording_id)
    recording = LabboxEphysRecordingExtractor(rdoc['recording'])
    return recording
