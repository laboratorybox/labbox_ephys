import random
import spikewidgets as sw
import spiketoolkit as st
import labbox_ephys as le
from labbox_ephys.utils import compute_unit_templates, plot_spike_waveform
import matplotlib as mpl
mpl.use('Agg') # This is important for speed!
import matplotlib.pyplot as plt
import mpld3
import time

class SortingUnitTemplateWidget:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        timer = time.time()

        self._set_status('running', 'Running SortingUnitTemplateWidget')

        sorting = state['sorting']
        unit_id = state['unit_id']
        figsize = state['figsize']

        R = le.LabboxEphysRecordingExtractor(sorting['recording'])
        S = le.LabboxEphysSortingExtractor(sorting['sorting'])

        filtopts = dict(
            freq_min=300,
            freq_max=6000,
            freq_wid=1000
        )
        template = compute_unit_templates(
            recording=R, sorting=S,
            unit_ids=[unit_id],
            ms_before=2, ms_after=2,
            max_spikes_per_unit=100,
            filtopts=filtopts
        )[0]

        f = plt.figure(figsize=[figsize[0]/100, figsize[1]/100], dpi=100)        
        plot_spike_waveform(template, spacing='auto', amp_scale_factor=2)
        # plt.title(f'Unit {unit_id}')
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