from labbox_ephys import dbcollection
import labbox_ephys as le
import numpy as np

class RecordingsView:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._refresh_recordings()

    def on_message(self, msg):
        if msg['action'] == 'remove_recordings':
            recording_ids = msg['recording_ids']
            dbcollection('recordings').remove({'recording_id': {'$in': recording_ids}})
            self._refresh_recordings()
        if msg['action'] == 'refresh_recordings':
            self._refresh_recordings()
        if msg['action'] == 'sort_recordings':
            recording_ids = msg['recording_ids']
            sorter = msg['sorter']
            for recording_id in recording_ids:
                recording = le.load_recording(recording_id=recording_id)
                all_channel_ids = recording.get_channel_ids()
                all_channel_groups = recording.get_channel_groups()
                all_group_ids = list(set(all_channel_groups))
                lookup = dict()
                for i in range(len(all_channel_ids)):
                    lookup[all_channel_ids[i]] = all_channel_groups[i]
                for group_id in all_group_ids:
                    sorting_id = f'{recording_id}::{group_id}::{sorter["name"]}'
                    channel_ids = [ch for ch in all_channel_ids if lookup[ch] == group_id]
                    doc = dict(
                        recording_id=recording_id,
                        group_id=group_id,
                        channel_ids=_list(channel_ids),
                        recording=recording.object(),
                        sorting=None,
                        sorting_name=sorter['name'],
                        sorter_name=sorter['name'],
                        sorting_id=sorting_id,
                        unit_ids=None,
                        runtime_info=None,
                        status='pending'
                    )
                    if dbcollection('sortings').find(dict(sorting_id=sorting_id)).count() == 0:
                        dbcollection('sortings').insert_one(doc)
                    else:
                        print(f'Not inserting sorting because it already exists: {sorting_id}')
            # dbcollection('recordings').remove({'recording_id': {'$in': recording_ids}})
            self._refresh_recordings()
        
    
    def _refresh_recordings(self):
        self._set_status('running', 'Loading recordings...')
        recordings = list(dbcollection('recordings').find(dict()))
        self._set_state(recordings=recordings)
        self._set_status('finished', 'Finished loading recordings.')
    
    # Send a custom message to JavaScript side
    # In .js file, use this.pythonInterface.onMessage((msg) => {...})
    def _send_message(self, msg):
        self.send_message(msg)

    # Set the python state
    def _set_state(self, **kwargs):
        self.set_state(kwargs)
    
    # Set error status with a message
    def _set_error(self, error_message):
        self._set_status('error', error_message)
    
    # Set status and a status message. Use running', 'finished', 'error'
    def _set_status(self, status, status_message=''):
        self._set_state(status=status, status_message=status_message)

def _list(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x