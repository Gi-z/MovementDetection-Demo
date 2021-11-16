from CSIKit.reader import CSVBeamformReader

import numpy as np
from plot import heatmap

from data_handler import load_csi_data
from stats import get_sti, get_correlation_coefficient

channels = [*range(183, 207), *range(209, 233)]

# files = ["calibration1_1","calibration1_2","calibration1_3","calibration1_4","calibration1_5"] # environment1/calibration
# files = ["calibration1_config1", "calibration2_config1", "calibration3_config1", "calibration4_config1", "calibration5_config1"] # house_experiments/calibration for config1
files = ["calibration1_config2", "calibration2_config2", "calibration3_config2", "calibration4_config2", "calibration5_config2"] # house_experiments/calibration for config2

corrs = []
results = []

reader = CSVBeamformReader()

for file in files:

    # full_name = "data/environment1/calibration/{}.csv".format(file)
    full_name = "data/house_experiments/calibration/{}.csv".format(file)
    csi_data = reader.read_file(full_name)

    csi, timestamps, _ = load_csi_data(csi_data, subcarrier_range=channels)

    # plot.heatmap_3d(csi, timestamps)
    # heatmap(csi, timestamps)

    #Assuming this data contains zero movement.
    #Only ambient CSI with a lack of presence.

    prev_frame = None

    sti_values = []
    corr_values = []

    prev_frame = csi[0]

    for x in range(csi.shape[0]-1):
        frame = csi[x+1]

        sti = get_sti(frame, prev_frame)
        corr = get_correlation_coefficient(frame, prev_frame)

        sti_values.append(sti)
        corr_values.append(corr)
        
        corrs.append(corr)

        prev_frame = frame

    timestamps = timestamps[1:]

    diff_corr = max(corr_values)-min(corr_values)
    results.append(diff_corr)

print("Mean Corr: {:.4f}".format(np.mean(corrs)))
print("Diff Corr: {:.4f}".format(np.mean(results)))