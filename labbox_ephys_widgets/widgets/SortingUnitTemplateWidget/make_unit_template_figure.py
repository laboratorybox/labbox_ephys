import hither2 as hi
import kachery as ka

@hi.function('make_unit_template_figure', '0.1.4')
@hi.container('docker://magland/labbox_ephys_base:latest')
@hi.local_modules(['../../../../../../labbox_ephys'])
def make_unit_template_figure(*, recording, sorting, unit_ids):
    print('------ make_unit_template_figure', recording, sorting, unit_ids)
    import labbox_ephys as le
    from labbox_ephys.utils import compute_unit_templates, plot_spike_waveform
    from matplotlib import pyplot as plt
    import mpld3
    with ka.config(fr='labbox_ephys_readonly'):
        R = le.LabboxEphysRecordingExtractor(recording)
        S = le.LabboxEphysSortingExtractor(sorting)

        filtopts = dict(
            freq_min=300,
            freq_max=6000,
            freq_wid=1000
        )
        templates = compute_unit_templates(
            recording=R, sorting=S,
            unit_ids=unit_ids,
            ms_before=2, ms_after=2,
            max_spikes_per_unit=100,
            filtopts=filtopts
        )

        ret = []
        for i in range(len(unit_ids)):
            # f = plt.figure(figsize=[figsize[0]/100, figsize[1]/100], dpi=100)        
            f = plt.figure(figsize=[6, 6], dpi=100)        
            plot_spike_waveform(templates[i], spacing='auto', amp_scale_factor=2)
            # plt.title(f'Unit {unit_id}')
            x = mpld3.fig_to_dict(f)
            # here's how you would disable the menu button plugins:
            x['plugins'] = []
            ret.append(x)
        return ret