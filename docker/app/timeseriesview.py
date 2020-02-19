import argparse
import spikeforest_widgets as sw
from labbox_ephys import AutoRecordingExtractor
import kachery as ka

sw.init_electron()

ka.set_config(fr='default_readonly')

parser = argparse.ArgumentParser(description='View an ephys recording')
parser.add_argument('--path', help='Path to the recording to view', required=True)
parser.add_argument('--group', help='Optional shank group', required=False, default=None)

args = parser.parse_args()

with ka.config(fr='default_readonly'):
    r = dict(
        path=args.path
    )
    if args.group is not None:
        r['group'] = int(args.group)
    R = AutoRecordingExtractor(r)

    X = sw.TimeseriesView(
        recording=R
    )
    X.show()