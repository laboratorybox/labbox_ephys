import argparse
import labbox_ephys_widgets as lew
import labbox_ephys as le
import kachery as ka

lew.init_electron()

ka.set_config(fr='default_readonly')

parser = argparse.ArgumentParser(description='View an ephys recording')
parser.add_argument('--path', help='Path to the recording to view', required=False)
parser.add_argument('--recording_id', help='ID of the recording', required=False)
parser.add_argument('--group', help='Optional shank group', required=False, default=None)

args = parser.parse_args()

if args.recording_id is not None:
    R = le.load_recording(recording_id=args.recording_id)
else:
    with ka.config(fr='default_readonly'):
        r = dict(
            path=args.path
        )
        R = le.LabboxEphysRecordingExtractor(r)

if args.group is not None:
    R = le.LabboxEphysRecordingExtractor(dict(
        group=int(args.group),
        recording=R
    ))

    X = lew.TimeseriesView(
        recording=R
    )
    X.show()