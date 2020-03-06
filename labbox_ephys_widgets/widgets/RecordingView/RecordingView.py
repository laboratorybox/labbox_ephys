import labbox_ephys as le
from .lbdb import find


class RecordingView:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running RecordingView')

        recording = state.get('recording', None)
        if not recording:
            recording_id = state['recording_id']
            recording = le.load_recording_doc(recording_id=recording_id)
            self._set_state(recording=recording)

        if recording:
            R = le.LabboxEphysRecordingExtractor(recording['recording'])
            self._set_state(
                channel_ids=R.get_channel_ids(),
                channel_groups=R.get_channel_groups(),
                channel_locations=R.get_channel_locations()
            )

        self._set_status('finished', 'Finished RecordingView')

    def on_message(self, msg):
        # process custom messages from JavaScript here
        # In .js file, use this.pythonInterface.sendMessage({...})
        pass
    
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