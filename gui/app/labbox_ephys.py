import os
import labbox_ephys_widgets as lew

lew.init_electron()

X = lew.MainWidget(
    ephys_data_dir=os.getenv('EPHYS_DATA_DIR', '')
)
print('writing --- to /kachery-storage')
with open('/kachery-storage/testA.txt', 'w') as f:
    f.write('this is a test from inside the container')
X.show()