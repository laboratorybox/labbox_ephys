import labbox_ephys as le
import hither2 as hi

def store_sorting_in_database(*, recording, sorting, recording_id, group_id, sorting_name, sorter_name, sorting_params, runtime_info):
    sorting_id = f'{recording_id}::{group_id}::{sorting_name}'
    doc = dict(
        recording_id=recording_id,
        group_id=group_id,
        recording=recording.object(),
        sorting=sorting.object(),
        sorting_name=sorting_name,
        sorter_name=sorter_name,
        sorting_id=sorting_id,
        unit_ids=sorting.get_unit_ids().tolist(),
        runtime_info=runtime_info
    )
    le.dbcollection('sortings').replace_one(dict(sorting_id=sorting_id), doc, upsert=True)

def sort_recording_from_database(recording_id, sorter_name, sorting_params, sorting_name, group_ids=None):
    recording = le.load_recording(recording_id=recording_id)
    sorter = getattr(le.sorters, sorter_name)
    grps = recording.get_channel_groups()
    all_group_ids = list(set(grps))
    if group_ids is None:
        group_ids = all_group_ids
    else:
        for gid in group_ids:
            if gid not in all_group_ids:
                raise Exception(f'No group/shank in recording: {gid}')
    for group_id in group_ids:
        print(f'Sorting shank {group_id} using {sorter_name}')
        recording_shank = le.LabboxEphysRecordingExtractor(dict(group=group_id, recording=recording.object()))
        recording_shank_obj = le.LabboxEphysRecordingExtractor.get_recording_object(recording=recording_shank)
        with hi.config(download_results=True):
            result_shank = sorter.run(
                recording=recording_shank_obj,
                **sorting_params
            )
        sorting_shank_obj = result_shank.wait()
        sorting_shank = le.LabboxEphysSortingExtractor(sorting_shank_obj)
        store_sorting_in_database(
            recording=recording_shank,
            sorting=sorting_shank,
            recording_id=recording_id,
            group_id=group_id,
            sorting_name=sorting_name,
            sorter_name=sorter_name,
            sorting_params=sorting_params,
            runtime_info=result_shank.runtime_info()
        )