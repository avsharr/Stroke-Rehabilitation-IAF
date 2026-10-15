def compute_welch_psd(raw_epochs_or_raw, fmin=1.0, fmax=30.0, n_fft=1250):
    """Compute PSD with Welch's Method."""

    # fmin=1.0, fmax=30.0: we look only at brain waves from 1 to 30 Hz.
    # n_fft=1250: gives a frequency step of 0.1 Hz
    # window='hamming'

    spectrum = raw_epochs_or_raw.compute_psd(
        method="welch",
        fmin=fmin,
        fmax=fmax,
        n_fft=n_fft,
        n_overlap=n_fft // 2,
        window="hamming",
    )

    psd_data, freqs = spectrum.get_data(return_freqs=True)
    return freqs, psd_data