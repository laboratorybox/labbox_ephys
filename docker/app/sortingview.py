import argparse
import labbox_ephys_widgets as lew
import kachery as ka

lew.init_electron()

parser = argparse.ArgumentParser(description='View a sorting result')
parser.add_argument('--sorting_id', help='Sorting ID for the sorting ti view', required=True)

args = parser.parse_args()

print(args.sorting_id)
X = lew.SortingView(
    sortingId=args.sorting_id
)
X.show()