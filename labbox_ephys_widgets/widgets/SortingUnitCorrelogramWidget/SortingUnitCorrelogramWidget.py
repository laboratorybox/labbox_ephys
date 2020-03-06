import random
import spikewidgets as sw
import spiketoolkit as st
import labbox_ephys as le
from labbox_ephys.utils import plot_autocorrelogram
import matplotlib as mpl
mpl.use('Agg') # This is important for speed!
import matplotlib.pyplot as plt
import mpld3
import time

class SortingUnitCorrelogramWidget:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        timer = time.time()

        self._set_status('running', 'Running SortingUnitCorrelogramWidget')

        sorting = state['sorting']
        unit_id = state['unit_id']
        figsize = state['figsize']

        R = le.LabboxEphysRecordingExtractor(sorting['recording'])
        S = le.LabboxEphysSortingExtractor(sorting['sorting'])
        S.set_sampling_frequency(R.get_sampling_frequency()) # in case it doesn't have it

        f = plt.figure(figsize=[figsize[0]/100, figsize[1]/100], dpi=100)
        plot_autocorrelogram(sorting=S, unit_id=unit_id, window_size_msec=300, bin_size_msec=1)
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        x = mpld3.fig_to_dict(f)
        # here's how you would disable the menu button plugins:
        x['plugins'] = []


        self._set_state(
            plot=dict(
                id=_random_string(10),
                object=x
            )
        )

        # print(f'Elapsed: {time.time() - timer} sec')

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