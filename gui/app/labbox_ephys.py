import os
import labbox_ephys_widgets as lew

lew.init_electron()

X = lew.MainWidget(
    ephys_data_dir=os.getenv('EPHYS_DATA_DIR', '')
)

X.show()