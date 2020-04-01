import os
import labbox_ephys_widgets as lew
import kachery as ka

ka.set_config(fr='labbox_ephys_readonly')

lew.init_electron()

X = lew.RecordingsView()

X.show()