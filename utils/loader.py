import mne

def load_preprocess_eeg(file_path: str):
    """load a ".set" file, fix channel types,
    and crop intervals based on experiment annotations.
    """

    # load raw data
    raw = mne.io.read_raw_eeglab(file_path, preload=True)

    # exclude all no-EEG channels
    ch_types = {}
    for ch in ["EMGL", "EMGR"]:
        if ch in raw.ch_names:
            ch_types[ch] = "emg" # remove auxiliary temperature
    if "Temp" in raw.ch_names:
        ch_types["Temp"] = "misc" # remove temperature
    if ch_types:
        raw.set_channel_types(ch_types)  # keep EEG

    # extract EEG channels
    raw_eeg = raw.copy().pick(picks="eeg")

    # find when "Open eyes" and "Closed eyes" start automatically from the file notes
    t_open, t_closed = None, None
    for annot in raw.annotations:
        desc = annot["description"]
        if "Open eyes" in desc:
            t_open = annot["onset"]
        elif "Closed eyes" in desc:
            t_closed = annot["onset"]

    t_end = raw.times[-1]

    # safety buffer: cut 2 seconds from the start and the end of each interval (blinking or reacting to instruction)
    raw_eo = raw_eeg.copy().crop(tmin=t_open + 2.0, tmax=t_closed - 2.0)
    raw_ec = raw_eeg.copy().crop(tmin=t_closed + 2.0, tmax=t_end - 2.0)

    return raw_eo, raw_ec, raw_eeg.ch_names