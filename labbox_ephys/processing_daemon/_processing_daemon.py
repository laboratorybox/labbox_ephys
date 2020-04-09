import traceback
import numpy as np
import time
from labbox_ephys import load_recording
from labbox_ephys import dbcollection
from labbox_ephys import sorters
from labbox_ephys import LabboxEphysRecordingExtractor, LabboxEphysSortingExtractor
from labbox_ephys import remote_job_handler
import hither2 as hi

class ProcessingDaemon:
    def __init__(self):
        pass
    def iterate(self):
        # pending sorting jobs
        for doc in dbcollection('sortings').find(dict(
            status='pending'
        )):
            try:
                self._handle_pending_sorting(doc)
            except:
                traceback.print_exc()
                dbcollection('sortings').update_one(
                    dict(sorting_id=doc['sorting_id']),
                    {'$set': dict(
                        status='error'
                    )}
                )
    def run(self):
        while True:
            self.iterate()
            time.sleep(5)
    def _handle_pending_sorting(self, doc):
        print('Queuing sorting', doc['sorting_id'])

        # doc = dict(
        #     recording_id=recording_id,
        #     group_id=group_id,
        #     channel_ids=_list(channel_ids),
        #     recording=recording.object(),
        #     sorting=None,
        #     sorting_name=sorter['name'],
        #     sorter_name=sorter['name'],
        #     sorting_id=sorting_id,
        #     unit_ids=None,
        #     runtime_info=None,
        #     status='pending'
        # )
        recording_id = doc['recording_id']
        sorter_name = doc['sorter_name']
        sorting_params = doc.get('sorting_params', dict())
        group_id = doc['group_id']
        channel_ids = doc['channel_ids']

        recording = load_recording(recording_id=recording_id)
        sorter = getattr(sorters, sorter_name)

        all_channel_groups = recording.get_channel_groups()
        all_channel_ids = recording.get_channel_ids()
        groups_for_channel = dict()
        for i in range(len(all_channel_ids)):
            groups_for_channel[all_channel_ids[i]] = all_channel_groups[i]
        all_group_ids = list(set(all_channel_groups))
        
        print(f'Sorting shank {group_id} using {sorter_name}')

        arg_shank = dict(group=group_id, recording=recording.object())
        if channel_ids is not None:
            channel_ids_shank = [ch for ch in channel_ids if groups_for_channel[ch] == group_id ]
        else:
            channel_ids_shank = None
        if channel_ids_shank is None or len(channel_ids_shank) > 0:
            if channel_ids_shank is not None:
                arg_shank = dict(channel_ids=channel_ids_shank, recording=arg_shank)
        recording_shank = LabboxEphysRecordingExtractor(arg_shank)
        recording_shank_obj = LabboxEphysRecordingExtractor.get_recording_object(recording=recording_shank)

        dbcollection('sortings').update_one(
            dict(sorting_id=doc['sorting_id']),
            {'$set': dict(
                status='running'
            )}
        )

        with hi.config(download_results=True, container=True, job_handler=remote_job_handler()):
            result_shank = sorter.run(
                recording=recording_shank_obj,
                **sorting_params
            )
        sorting_shank_obj = result_shank.wait()
        sorting_shank = LabboxEphysSortingExtractor(sorting_shank_obj)

        dbcollection('sortings').update_one(
            dict(sorting_id=doc['sorting_id']),
            {'$set': dict(
                status='finished',
                sorting=sorting_shank.object(),
                unit_ids=_list(sorting_shank.get_unit_ids()),
                runtime_info=result_shank.runtime_info()
            )}
        )

def _list(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x