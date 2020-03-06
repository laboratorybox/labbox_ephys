import numpy as np
from ._correlograms_phy import compute_correlograms


def _create_filter_kernel(N, samplerate, freq_min, freq_max, freq_wid=1000):
    from scipy import special
    # Matches ahb's code /matlab/processors/ms_bandpass_filter.m
    # improved ahb, changing tanh to erf, correct -3dB pts  6/14/16
    T = N / samplerate  # total time
    df = 1 / T  # frequency grid
    # relative bottom-end roll-off width param, kills low freqs by factor 1e-5.
    relwid = 3.0

    k_inds = np.arange(0, N)
    k_inds = np.where(k_inds <= (N + 1) / 2, k_inds, k_inds - N)

    fgrid = df * k_inds
    absf = np.abs(fgrid)

    val = np.ones(fgrid.shape)
    if freq_min != 0:
        val = val * (1 + special.erf(relwid * (absf - freq_min) /
                                     freq_min)) / 2  # pylint: disable=no-member
        val = np.where(np.abs(k_inds) < 0.1, 0, val)  # kill DC part exactly
    if freq_max != 0:
        val = val * (1 - special.erf((absf - freq_max) / freq_wid)
                     ) / 2  # pylint: disable=no-member
    # note sqrt of filter func to apply to spectral intensity not ampl
    val = np.sqrt(val)
    return val


def _bandpass_filter(traces, samplerate, freq_min, freq_max, freq_wid=1000):
    ndim = traces.ndim
    if ndim == 1:
        traces2 = traces.reshape((1, 1, traces.shape[0]))
    elif ndim == 2:
        traces2 = traces.reshape((1, traces.shape[0], traces.shape[1]))
    elif ndim == 3:
        traces2 = traces
    else:
        raise Exception('This case not supported yet')
    K = traces2.shape[0]
    M = traces2.shape[1]
    N = traces2.shape[2]
    traces_fft = np.fft.rfft(traces2, axis=2)
    kernel = _create_filter_kernel(
        N=N,
        samplerate=samplerate,
        freq_min=freq_min, freq_max=freq_max, freq_wid=freq_wid
    )
    # because this is the DFT of real data
    kernel = kernel[0:traces_fft.shape[2]]
    traces_fft = traces_fft * \
        np.tile(kernel.reshape(1, 1, len(kernel)), (K, M, 1))
    traces_filtered = np.fft.irfft(traces_fft, axis=2)
    return traces_filtered.reshape(traces.shape)


def extract_unit_clips(*, recording, sorting, unit_ids, ms_before, ms_after, max_spikes_per_unit, filtopts=None):
    import spiketoolkit as st
    ms_padding = 0
    if filtopts is not None:
        freq_min = filtopts['freq_min']
        ms_padding = 2 * (1000 / freq_min)
    clips = st.postprocessing.get_unit_waveforms(
        recording=recording,
        sorting=sorting,
        unit_ids=unit_ids,
        ms_before=ms_before + ms_padding,
        ms_after=ms_after + ms_padding,
        max_spikes_per_unit=max_spikes_per_unit,
        save_as_features=False
    )
    if filtopts is not None:
        for i in range(len(unit_ids)):
            clips[i] = _bandpass_filter(clips[i], samplerate=recording.get_sampling_frequency(
            ), freq_min=filtopts['freq_min'], freq_max=filtopts['freq_max'], freq_wid=filtopts['freq_wid'])

    if ms_padding > 0:
        n_padding = int(ms_padding / 1000 * recording.get_sampling_frequency())
        for i in range(len(unit_ids)):
            clips[i] = clips[i][:, :, n_padding:-n_padding]
    return clips


def compute_unit_templates(*, recording, sorting, unit_ids, ms_before, ms_after, max_spikes_per_unit, filtopts=None):
    clips = extract_unit_clips(
        recording=recording,
        sorting=sorting,
        unit_ids=unit_ids,
        ms_before=ms_before,
        ms_after=ms_after,
        max_spikes_per_unit=max_spikes_per_unit,
        filtopts=filtopts
    )
    templates = []
    for i in range(len(unit_ids)):
        template0 = np.median(clips[i], axis=0)
        templates.append(template0)
    return templates


def plot_spike_waveform(X, spacing='auto', amp_scale_factor=1):
    import matplotlib.pyplot as plt
    if spacing == 'auto':
        spacing = np.max(np.abs(X)) / amp_scale_factor
    M = X.shape[0]
    T = X.shape[1]
    for m in range(M):
        plt.plot(np.arange(T), X[m, :].T + spacing * m)
    plt.ylim([-spacing*2, (M+1)*spacing])
    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)


def _plot_correlogram(*, ax, bin_counts, bins, wid, title='', color=None):
    kk = 1000
    ax.bar(x=(bins-wid/2)*kk, height=bin_counts,
           width=wid*kk, color=color, align='edge')
    ax.set_xlabel('dt (msec)')
    ax.set_xticks([bins[0]*kk, bins[len(bins)//2]*kk, bins[-1]*kk])
    # ax.set_yticks([])


def plot_autocorrelogram(sorting, unit_id, window_size_msec, bin_size_msec):
    import matplotlib.pyplot as plt
    times = sorting.get_unit_spike_train(unit_id=unit_id)
    labels = np.ones(times.shape, dtype=np.int32)
    window_size = window_size_msec / 1000
    bin_size = bin_size_msec / 1000
    C = compute_correlograms(
        spike_times=times/sorting.get_sampling_frequency(),
        spike_clusters=labels,
        cluster_ids=[1],
        bin_size=bin_size,
        window_size=window_size,
        sample_rate=sorting.get_sampling_frequency(),
        symmetrize=True
    )
    bins = np.linspace(- window_size / 2, window_size / 2, C.shape[2])
    _plot_correlogram(
        ax=plt.gca(), bin_counts=C[0, 0, :], bins=bins, wid=bin_size, color='gray')


def plot_crosscorrelogram(sorting, unit_id1, unit_id2, window_size_msec, bin_size_msec):
    import matplotlib.pyplot as plt
    times1 = sorting.get_unit_spike_train(unit_id=unit_id1)
    times2 = sorting.get_unit_spike_train(unit_id=unit_id2)
    times = np.concatenate((times1, times2))
    labels = np.concatenate(
        (np.ones(times1.shape, dtype=np.int32)*1, np.ones(times2.shape, dtype=np.int32)*2))
    inds = np.argsort(times)
    times = times[inds]
    labels = labels[inds]
    window_size = window_size_msec / 1000
    bin_size = bin_size_msec / 1000
    C = compute_correlograms(
        spike_times=times/sorting.get_sampling_frequency(),
        spike_clusters=labels,
        cluster_ids=[1, 2],
        bin_size=bin_size,
        window_size=window_size,
        sample_rate=sorting.get_sampling_frequency(),
        symmetrize=True
    )
    bins = np.linspace(- window_size / 2, window_size / 2, C.shape[2])
    _plot_correlogram(
        ax=plt.gca(), bin_counts=C[0, 1, :], bins=bins, wid=bin_size, color='gray')
