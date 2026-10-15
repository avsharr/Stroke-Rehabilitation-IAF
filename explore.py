import mne

file_path = "Dataset_Rest/SUB03_rest.vhdr.set"
raw = mne.io.read_raw_eeglab(file_path, preload=True)

print(f"recording info: {raw.info}\n")

print(f"recording channels: {raw.ch_names}\n")

print("annotations:\n")
for annot in raw.annotations:
    print(annot["description"], annot["onset"], annot["duration"])

events, event_id = mne.events_from_annotations(raw)
print(events, event_id)