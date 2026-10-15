import os
import numpy as np
from core.iaf_detector import estimate_iaf
from utils.loader import load_preprocess_eeg
from utils.psd_pipeline import compute_welch_psd


def run_pipeline():
    # path to dataset file
    file_path = "Dataset_Rest/SUB05_rest.vhdr.set"

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Processing participant file: {file_path}")

    # step 1: load + preprocess data
    raw_eo, raw_ec, ch_names = load_preprocess_eeg(file_path)

    # step 2: compute PSD with Welch's method
    freqs, psd_eo = compute_welch_psd(raw_eo) # Eyes Open
    _, psd_ec = compute_welch_psd(raw_ec) # Eyes Closed

    # step 3: detect IAF on a target occipital channel
    target_channel = "Oz"
    ch_idx = ch_names.index(target_channel)

    # analyze Closed Eyes condition (expect prominent alpha peak)
    # change to Open Eyes = instead of psd_ec[ch_idx] => psd_eo[ch_idx]
    iaf_cog, power_cog = estimate_iaf(
        freqs, psd_ec[ch_idx], method="center_of_gravity"
    )

    iaf_max, power_max = estimate_iaf(
        freqs, psd_ec[ch_idx], method="max_peak"
    )

    print(f"\n--- Results for Channel {target_channel} (Closed Eyes) ---")
    print(f"IAF (Center of Gravity): {iaf_cog:.2f} Hz")
    print(f"IAF (Peak Maximum):      {iaf_max:.2f} Hz")

if __name__ == "__main__":
    run_pipeline()