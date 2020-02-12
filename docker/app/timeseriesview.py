


import argparse
import spikeforest_widgets as sw
from spikeforest2_utils import AutoRecordingExtractor
import kachery as ka

sw.init_electron()

ka.set_config(fr='default_readonly')

parser = argparse.ArgumentParser(description='View an ephys recording')
parser.add_argument('--path', help='Path to the recoring to view', required=True)

args = parser.parse_args()

with ka.config(fr='default_readonly'):
    R = AutoRecordingExtractor(args.path)

    X = sw.TimeseriesView(
        recording=R
    )
    X.show()