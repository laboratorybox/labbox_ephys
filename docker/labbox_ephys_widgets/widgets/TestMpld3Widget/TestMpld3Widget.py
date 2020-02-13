import random

class TestMpld3Widget:
    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running TestMpld3Widget')

        # Processing code goes here
        # The state argument contains the state set from the javacript code
        # In .js file, use this.pythonInterface.setState({...})

        import matplotlib.pyplot as plt, mpld3
        f = plt.figure(figsize=(state['test'], 5))
        plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
        x = mpld3.fig_to_dict(f)

        self._set_state(
            plot=dict(
                id=_random_string(10),
                object=x
            )
        )

        self._set_status('finished', 'Finished TestMpld3Widget')

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