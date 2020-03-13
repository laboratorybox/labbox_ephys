import random
import spikewidgets as sw
import spiketoolkit as st
import labbox_ephys as le
import matplotlib as mpl
mpl.use('Agg') # This is important for speed!
import matplotlib.pyplot as plt
import mpld3
import time
import hither2 as hi
from .make_unit_template_figure import make_unit_template_figure
import labbox_ephys as le
import numpy as np

class SortingUnitTemplateWidget:
    def __init__(self):
        super().__init__()
        self._job = None

    def javascript_state_changed(self, prev_state, state):
        timer = time.time()

        print('SortingUnitTemplateWidget 1')

        self._set_status('running', 'Running SortingUnitTemplateWidget')

        sorting = state['sorting']
        unit_id = int(state['unit_id'])

        all_unit_ids = sorting['unit_ids']
        config = le.hither2_job_config()

        with hi.config(**config):
            job = make_unit_template_figure.run(
                recording=sorting['recording'],
                sorting=sorting['sorting'],
                unit_ids=all_unit_ids
            )
        unit_ind = np.where(np.array(all_unit_ids) == unit_id)[0][0]
        setattr(job, 'unit_ind', unit_ind)
        self._job = job
        print('SortingUnitTemplateWidget 2')

    def on_message(self, msg):

        # process custom messages from JavaScript here
        # In .js file, use this.pythonInterface.sendMessage({...})
        pass

    def iterate(self):
        job = self._job
        if job is None:
            return
        print('SortingUnitTemplateWidget 3')
        x = job.wait(0)
        if job.status() == 'finished':
            print('SortingUnitTemplateWidget 4')
            unit_ind = job.unit_ind
            self._set_state(
                plot=dict(
                    id=_random_string(10),
                    object=x[unit_ind]
                )
            )
            self._job = None
            # print(f'Elapsed: {time.time() - timer} sec')
            self._set_status('finished', 'Finished SortingUnitTemplateWidget')
        elif job.status() == 'error':
            self._job = None
            # print(f'Elapsed: {time.time() - timer} sec')
            self._set_status('finished', 'Finished SortingUnitTemplateWidget')
    
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