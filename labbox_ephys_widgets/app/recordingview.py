import argparse
import labbox_ephys_widgets as lew
import kachery as ka
import kachery as ka

ka.set_config(fr='labbox_ephys_readonly')

lew.init_electron()

parser = argparse.ArgumentParser(description='View a recording')
parser.add_argument('--recording_id', help='Recording ID for the recording to view', required=True)

args = parser.parse_args()

X = lew.RecordingView(
    recordingId=args.recording_id
)
X.show()