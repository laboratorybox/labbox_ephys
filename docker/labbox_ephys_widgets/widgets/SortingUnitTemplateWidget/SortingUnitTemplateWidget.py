import random
import spikewidgets as sw
import spiketoolkit as st
from labbox_ephys import AutoRecordingExtractor, AutoSortingExtractor

class SortingUnitTemplateWidget:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running SortingUnitTemplateWidget')

        sorting = state['sorting']
        unit_id = state['unit_id']
        figsize = state['figsize']

        import matplotlib.pyplot as plt, mpld3
        f = plt.figure(figsize=figsize)
        R = AutoRecordingExtractor(sorting['recording_path'])
        S = AutoSortingExtractor(sorting['sorting_path'])
        template = st.postprocessing.get_unit_templates(
            recording=R, sorting=S, unit_ids=[unit_id],
            mode='median',
            max_spikes_per_unit=200,
            ms_before=1, ms_after=1,
        )[0]

        plt.plot(template.T)
        x = mpld3.fig_to_dict(f)

        self._set_state(
            plot=dict(
                id=_random_string(10),
                object=x
            )
        )

        self._set_status('finished', 'Finished SortingUnitTemplateWidget')

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

def _random_string(num: int):
    """Generate random string of a given length.
    """
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=num))