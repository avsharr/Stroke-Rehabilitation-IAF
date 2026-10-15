import numpy as np

def estimate_iaf(
    freqs: np.ndarray,
    psd_curve: np.ndarray,
    fmin: float = 7.0,
    fmax: float = 14.0,
    method: str = "center_of_gravity",
):
    """Finds IAF between 7.0 and 14.0 Hz. Using either
    "Peak Maximum" or "Center of Gravity (CoG)" methods
    """
    # looks inside the alpha wave window (7 to 14 Hz)
    idx = np.where((freqs >= fmin) & (freqs <= fmax))[0]
    sub_freqs = freqs[idx]
    sub_psd = psd_curve[idx]

    if method == "max_peak":
        # method 1: finds the single highest point on the curve
        peak_idx = np.argmax(sub_psd)
        iaf = sub_freqs[peak_idx]
        peak_power = sub_psd[peak_idx]

    elif method == "center_of_gravity":
        # method 2: calculate the "center of mass" of the whole alpha hill
        # this is more stable if the peak is messy or has small bumps
        iaf = np.sum(sub_freqs * sub_psd) / np.sum(sub_psd)
        peak_power = np.max(sub_psd)
    else:
        raise ValueError("Unknown IAF estimation method specified.")

    return iaf, peak_power