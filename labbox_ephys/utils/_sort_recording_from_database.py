import labbox_ephys as le
import hither2 as hi
import numpy as np

def _list(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x

def store_sorting_in_database(*, recording, sorting, recording_id, group_id, sorting_name, sorter_name, sorting_params, runtime_info, channel_ids=None):
    sorting_id = f'{recording_id}::{group_id}::{sorting_name}'
    if channel_ids is None:
        channel_ids = recording.get_channel_ids()
    doc = dict(
        recording_id=recording_id,
        group_id=group_id,
        channel_ids=_list(channel_ids),
        recording=recording.object(),
        sorting=sorting.object(),
        sorting_name=sorting_name,
        sorter_name=sorter_name,
        sorting_id=sorting_id,
        unit_ids=_list(sorting.get_unit_ids()),
        runtime_info=runtime_info
    )
    le.dbcollection('sortings').replace_one(dict(sorting_id=sorting_id), doc, upsert=True)

def sort_recording_from_database(recording_id, sorter_name, sorting_params, sorting_name, group_ids=None, channel_ids=None):
    recording = le.load_recording(recording_id=recording_id)
    sorter = getattr(le.sorters, sorter_name)
    all_channel_groups = recording.get_channel_groups()
    all_channel_ids = recording.get_channel_ids()
    groups_for_channel = dict()
    for i in range(len(all_channel_ids)):
        groups_for_channel[all_channel_ids[i]] = all_channel_groups[i]
    all_group_ids = list(set(all_channel_groups))
    if group_ids is None:
        group_ids = all_group_ids
    else:
        for gid in group_ids:
            if gid not in all_group_ids:
                raise Exception(f'No group/shank in recording: {gid}')
    for group_id in group_ids:
        print(f'Sorting shank {group_id} using {sorter_name}')
        arg_shank = dict(group=group_id, recording=recording.object())
        if channel_ids is not None:
            channel_ids_shank = [ch for ch in channel_ids if groups_for_channel[ch] == group_id ]
        else:
            channel_ids_shank = None
        if channel_ids_shank is None or len(channel_ids_shank) > 0:
            if channel_ids_shank is not None:
                arg_shank = dict(channel_ids=channel_ids_shank, recording=arg_shank)
            recording_shank = le.LabboxEphysRecordingExtractor(arg_shank)
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
                channel_ids=channel_ids_shank,
                sorting_name=sorting_name,
                sorter_name=sorter_name,
                sorting_params=sorting_params,
                runtime_info=result_shank.runtime_info()
            )