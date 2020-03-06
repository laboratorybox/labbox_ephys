#!/usr/bin/env python

from labbox_ephys import load_recording, LabboxEphysRecordingExtractor
import spikeextractors as se
import kachery as ka

# Load recording from database
print('Loading recording...')
# recording = load_recording(recording_id='sf:synth_magland_noise10_K10_C4/001_synth')
with ka.config(fr='default_readonly'):
    recording = LabboxEphysRecordingExtractor('sha1://ee5214337b2e01910a92c3613a4b8ad4be4dc476/SYNTH_MAGLAND/synth_magland_noise10_K10_C4/001_synth.json')

# Extract 10 seconds
print('Extracting sub-recording...')
rec2 = se.SubRecordingExtractor(parent_recording=recording, start_frame=0, end_frame=recording.get_sampling_frequency()*10)

# Convert to an object
print('Converting to object...')
recobj = LabboxEphysRecordingExtractor.get_recording_object(recording=rec2)

# store object in remote (and local) kachery
print('Storing object remotely...')
p = ka.store_object(recobj, to='default_readwrite')

# store raw file in remote (and local) kachery
print('Storing raw file remotely...')
ka.store_file(recobj['raw'], to='default_readwrite')

print(p)

print('Done.')