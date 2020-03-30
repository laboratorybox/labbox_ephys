from .lbdb import find, remove

class SortingsView:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._refresh_sortings()

    def on_message(self, msg):
        if msg['action'] == 'remove_sortings':
            sorting_ids = msg['sorting_ids']
            remove(collection='sortings', query={'sorting_id': {'$in': sorting_ids}})
            self._refresh_sortings()
        elif msg['action'] == 'refresh_sortings':
            self._refresh_sortings()
    
    def _refresh_sortings(self):
        self._set_status('running', 'Loading sortings...')
        self._set_state(sortings=None)
        sortings = find(collection='sortings', query=dict())
        self._set_state(sortings=sortings)
        self._set_status('finished', f'Finished loading {len(sortings)} sortings.')
    
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