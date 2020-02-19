import kachery as ka
from .bandpass_filter import bandpass_filter
import spikeextractors as se
import numpy as np
import hashlib
import json
from .mdaextractors import MdaRecordingExtractor

class AutoRecordingExtractor(se.RecordingExtractor):
    def __init__(self, arg, download=False):
        super().__init__()
        self._hash = None
        if isinstance(arg, str):
            arg = dict(path=arg)
        if isinstance(arg, se.RecordingExtractor):
            self._recording = arg
        else:
            self._recording = None

            if 'kachery_config' in arg:
                ka.set_config(**arg['kachery_config'])

            # filters
            if ('recording' in arg) and ('filters' in arg):
                recording1 = AutoRecordingExtractor(arg['recording'])
                self._recording = self._apply_filters(recording1, arg['filters'])
            elif ('raw' in arg) and ('params' in arg) and ('geom' in arg):
                self._recording = MdaRecordingExtractor(timeseries_path=arg['raw'], samplerate=arg['params']['samplerate'], geom=np.array(arg['geom']), download=download)
            else:
                path = arg.get('path', '')
                if not path:
                    path = arg.get('directory', '')
                if path.endswith('.mda'):
                    if 'samplerate' not in arg:
                        raise Exception('Missing argument: samplerate')
                    samplerate = arg['samplerate']
                    self._recording = MdaRecordingExtractor(timeseries_path=path, samplerate=samplerate, download=download)
                    hash0 = _sha1_of_object(dict(
                        timeseries_sha1=ka.get_file_info(path, algorithm='sha1')['sha1'],
                        samplerate=samplerate
                    ))
                    setattr(self, 'hash', hash0)
                elif path.endswith('.nwb.json'):
                    self._recording = NwbJsonRecordingExtractor(file_path=path)
                    hash0 = ka.get_file_info(path)['sha1']
                    setattr(self, 'hash', hash0)
                elif path.endswith('.json') and (not path.endswith('.nwb.json')):
                    obj = ka.load_object(path)
                    if obj is None:
                        raise Exception(f'Unable to load object: {path}')
                    if ('raw' in obj) and ('params' in obj) and ('geom' in obj):
                        self._recording = MdaRecordingExtractor(timeseries_path=obj['raw'], samplerate=obj['params']['samplerate'], geom=np.array(obj['geom']), download=download)
                    else:
                        raise Exception('Problem initializing recording extractor')
                elif can_load_mda(path):
                    self._recording = MdaRecordingExtractor(recording_directory=path, download=download)
                elif can_load_nrs(path):
                    self._recording = NrsRecordingExtractor(path)
                else:
                    raise Exception('Unable to initialize recording extractor. Unable to determine format of recording: {}'.format(path))
            if 'group' in arg:
                R = self._recording
                channel_ids = np.array(R.get_channel_ids())
                groups = R.get_channel_groups(channel_ids=R.get_channel_ids())
                group = int(arg['group'])
                inds = np.where(np.array(groups) == group)[0]
                channel_ids = channel_ids[inds]
                self._recording = se.SubRecordingExtractor(
                    parent_recording=R,
                    channel_ids=np.array(channel_ids)
                )
        self.copy_channel_properties(recording=self._recording)
    
    def _apply_filters(self, recording, filters):
        ret = recording
        for filter0 in filters:
            ret = self._apply_filter(ret, filter0)
        return ret
    
    def _apply_filter(self, recording, filter0):
        if filter0['type'] == 'bandpass_filter':
            args = dict()
            if 'freq_min' in filter0:
                args['freq_min'] = filter0['freq_min']
            if 'freq_max' in filter0:
                args['freq_max'] = filter0['freq_max']
            if 'freq_wid' in filter0:
                args['freq_wid'] = filter0['freq_wid']
            return bandpass_filter(recording, **args)
        return None
    
    def hash(self):
        if not self._hash:
            if hasattr(self._recording, 'hash'):
                if type(self._recording.hash) == str:
                    self._hash = self._recording.hash
                else:
                    self._hash = self._recording.hash()
            else:
                self._hash = _samplehash(self._recording)
        return self._hash

    def get_channel_ids(self):
        return self._recording.get_channel_ids()

    def get_num_frames(self):
        return self._recording.get_num_frames()

    def get_sampling_frequency(self):
        return self._recording.get_sampling_frequency()

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        return self._recording.get_traces(channel_ids=channel_ids, start_frame=start_frame, end_frame=end_frame)

    @staticmethod
    def can_load_dir(path):
        if can_load_mda(path):
            return True
        if can_load_nrs(path):
            return True
        return False

def can_load_mda(path):
    dd = ka.read_dir(path)
    if 'raw.mda' in dd['files'] and 'params.json' in dd['files'] and 'geom.csv' in dd['files']:
        return True
    return False

def check_load_nrs(recording_path):
    dd = ka.read_dir(recording_path)
    probe_file = None
    xml_file = None
    nrs_file = None
    dat_file = None
    for f in dd['files'].keys():
        if f.endswith('.json'):
            obj = ka.load_object(recording_path + '/' + f)
            if obj.get('format_version', None) in ['flatiron-probe-0.1', 'flatiron-probe-0.2']:
                probe_file = recording_path + '/' + f
        elif f.endswith('.xml'):
            xml_file = recording_path + '/' + f
        elif f.endswith('.nrs'):
            nrs_file = recording_path + '/' + f
        elif f.endswith('.dat'):
            dat_file = recording_path + '/' + f
    if probe_file is not None and xml_file is not None and nrs_file is not None and dat_file is not None:
        info = dict(
            probe_file=probe_file,
            xml_file=xml_file,
            nrs_file=nrs_file,
            dat_file=dat_file
        )
        return info
    return None

def can_load_nrs(recording_path):
    info = check_load_nrs(recording_path)
    return (info is not None)

class NrsRecordingExtractor(se.RecordingExtractor):
    extractor_name = 'NrsRecordingExtractor'
    is_writable = False
    def __init__(self, dirpath):
        se.RecordingExtractor.__init__(self)
        info = check_load_nrs(dirpath)
        assert info is not None
        probe_obj = ka.load_object(info['probe_file'])
        xml_file = ka.load_file(info['xml_file'])
        # nrs_file = ka.load_file(info['nrs_file'])
        dat_file = ka.load_file(info['dat_file'])

        from xml.etree import ElementTree as ET
        xml = ET.parse(xml_file)
        root_element = xml.getroot()
        try:
            self._samplerate = float(root_element.find('acquisitionSystem/samplingRate').text)
        except:
            raise Exception('Unable to load acquisitionSystem/samplingRate')
        try:
            self._nChannels = int(root_element.find('acquisitionSystem/nChannels').text)
        except:
            raise Exception('Unable to load acquisitionSystem/nChannels')
        try:
            self._nBits = int(root_element.find('acquisitionSystem/nBits').text)
        except:
            raise Exception('Unable to load acquisitionSystem/nBits')

        if self._nBits == 16:
            dtype = np.int16
        elif self._nBits == 32:
            dtype = np.int32
        else:
            raise Exception(f'Unexpected nBits: {self._nBits}')

        self._rec = se.BinDatRecordingExtractor(dat_file, sampling_frequency=self._samplerate, numchan=self._nChannels, dtype=dtype)

        self._channel_ids = probe_obj['channel']
        for ii in range(len(probe_obj['channel'])):
            channel = probe_obj['channel'][ii]
            x = probe_obj['x'][ii]
            y = probe_obj['y'][ii]
            z = probe_obj['z'][ii]
            group = probe_obj.get('group', probe_obj.get('shank'))[ii]
            self.set_channel_property(channel, 'location', [x, y, z])
            self.set_channel_property(channel, 'group', group)

    def get_channel_ids(self):
        return self._channel_ids

    def get_num_frames(self):
        return self._rec.get_num_frames()

    def get_sampling_frequency(self):
        return self._rec.get_sampling_frequency()

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        if channel_ids is None:
            channel_ids = self._channel_ids
        return self._rec.get_traces(channel_ids=channel_ids, start_frame=start_frame, end_frame=end_frame)

class NwbJsonRecordingExtractor(se.RecordingExtractor):
    extractor_name = 'NwbJsonRecordingExtractor'
    is_writable = False
    def __init__(self, file_path):
        import h5_to_json as h5j
        se.RecordingExtractor.__init__(self)
        X = ka.load_object(file_path)
        X = h5j.hierarchy(X)
        self._timeseries = h5j.get_value(X['root']['acquisition']['ElectricalSeries']['_datasets']['data'], use_kachery=True, lazy=True)
        self._sampling_frequency = 30000 # hard-coded for now -- TODO: need to get this from the file
        self._geom = None # TODO: need to get this from the file
        if self._geom is not None:
            for m in range(self._timeseries.shape[0]):
                self.set_channel_property(m, 'location', self._geom[m, :])

    def get_channel_ids(self):
        return list(range(self._timeseries.shape[1]))

    def get_num_frames(self):
        return self._timeseries.shape[0]

    def get_sampling_frequency(self):
        return self._sampling_frequency

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = self.get_num_frames()
        if channel_ids is None:
            channel_ids = self.get_channel_ids()
        recordings = self._timeseries[start_frame:end_frame, :][:, channel_ids].T
        return recordings

class NwbElectricalSeriesRecordingExtractor(se.RecordingExtractor):
    def __init__(self, *, path, nwb_path):
        import h5py
        super().__init__()
        self._path = path
        self._nwb_path = nwb_path
        with h5py.File(self._path, 'r') as f:
            X = load_nwb_item(file=f, nwb_path=self._nwb_path)
            self._samplerate = X['starting_time'].attrs['rate']
            self._num_timepoints = X['data'].shape[0]
            self._num_channels = X['data'].shape[1]

    def get_channel_ids(self):
        return list(range(self._num_channels))

    def get_num_frames(self):
        return self._num_timepoints

    def get_sampling_frequency(self):
        return self._samplerate

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        import h5py
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = self.get_num_frames()
        if channel_ids is None:
            channel_ids = self.get_channel_ids()
        with h5py.File(self._path, 'r') as f:
            X = load_nwb_item(file=f, nwb_path=self._nwb_path)
            return X['data'][start_frame:end_frame, :][:, channel_ids].T

def _samplehash(recording):
    obj = {
        'channels': tuple(recording.get_channel_ids()),
        'frames': recording.get_num_frames(),
        'data': _samplehash_helper(recording)
    }
    return _sha1_of_object(obj)


def _samplehash_helper(recording):
    rng = np.random.RandomState(37)
    n_samples = min(recording.get_num_frames() // 1000, 100)
    inds = rng.randint(low=0, high=recording.get_num_frames(), size=n_samples)
    h = 0
    for i in inds:
        t = recording.get_traces(start_frame=i, end_frame=i + 100)
        h = hash((hash(bytes(t)), hash(h)))
    return h

def _sha1_of_string(txt: str) -> str:
    hh = hashlib.sha1(txt.encode('utf-8'))
    ret = hh.hexdigest()
    return ret


def _sha1_of_object(obj: object) -> str:
    txt = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return _sha1_of_string(txt)
