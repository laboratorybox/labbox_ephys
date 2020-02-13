import os
import labbox_ephys_widgets as lew

print(lew.__file__)
print(dir(lew))
lew.init_electron()

X = lew.MainWidget(
    local_data_dir=os.getenv('LOCAL_DATA_DIR', ''),
    jupyterlab_port=os.getenv('JUPYTERLAB_PORT', '')
)

X.show()