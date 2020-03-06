import labbox_ephys as le
import kachery as ka
import hither2 as hi

def test_mountainsort4():
    with ka.config(fr='default_readonly'):
        # recording = load_recording(recording_id='sf:synth_magland_noise10_K10_C4/001_synth')
        recording = le.LabboxEphysRecordingExtractor('sha1://0313fc3882af5c36468982d8b00822aee991f771/synth_magland_noise10_K10_C4/001_synth_10sec.json')
    assert recording.get_sampling_frequency() == 30000
    with hi.config(container=True):
        sorting_obj = le.sorters.mountainsort4.run(
            recording=recording.arg,
            detect_sign=-1,
            adjacency_radius=50,
            clip_size=50,
            detect_threshold=3,
            detect_interval=10,
            freq_min=300,
            freq_max=6000,
            whiten=True,
            curation=False,
            filter=True
        ).wait()
    sorting = le.LabboxEphysSortingExtractor(sorting_obj, samplerate=recording.get_sampling_frequency())
    unit_ids = sorting.get_unit_ids()
    print('Unit IDs:', unit_ids)
    assert len(unit_ids) >= 6