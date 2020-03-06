import labbox_ephys as le
import hither2 as hi

def store_sorting_in_database(*, recording, sorting, recording_id, sorting_name, sorter_name, sorting_params, runtime_info):
    sorting_id = recording_id + '::' + sorting_name
    doc = dict(
        recording_id=recording_id,
        recording=recording.object(),
        sorting=sorting.object(),
        sorting_name=sorting_name,
        sorter_name=sorter_name,
        sorting_id=sorting_id,
        unit_ids=sorting.get_unit_ids().tolist(),
        runtime_info=runtime_info
    )
    le.dbcollection('sortings').replace_one(dict(recording_id=recording_id, sorting_name=sorting_name), doc, upsert=True)

def sort_recording_from_database(recording_id, sorter_name, sorting_params, sorting_name):
    recording = le.load_recording(recording_id=recording_id)
    Robj = le.LabboxEphysRecordingExtractor.get_recording_object(recording=recording)
    sorter = getattr(le.sorters, sorter_name)
    with hi.config(download_results=True):
        result = sorter.run(
            recording=Robj,
            **sorting_params
        )
    sorting_obj = result.wait()
    sorting = le.LabboxEphysSortingExtractor(sorting_obj)
    store_sorting_in_database(
        recording=recording,
        sorting=sorting,
        recording_id=recording_id,
        sorting_name=sorting_name,
        sorter_name=sorter_name,
        sorting_params=sorting_params,
        runtime_info=result.runtime_info()
    )