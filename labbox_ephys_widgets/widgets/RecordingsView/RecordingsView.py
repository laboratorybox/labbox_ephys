from .lbdb import find, remove

class RecordingsView:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Loading recordings...')

        self._refresh_recordings()

        self._set_status('finished', 'Finished loading recordings.')

    def on_message(self, msg):
        if msg['action'] == 'remove_recordings':
            recording_ids = msg['recording_ids']
            remove(collection='recordings', query={'recording_id': {'$in': recording_ids}})
        self._refresh_recordings()
    
    def _refresh_recordings(self):
        recordings = find(collection='recordings', query=dict())
        self._set_state(recordings=recordings)
    
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