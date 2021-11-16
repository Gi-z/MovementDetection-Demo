from CSIKit.util.csitools import get_CSI
from CSIKit.util import filters

import numpy as np

# ALL_CHANNELS = [*range(24), *range(26, 50), *range(62, 85), *range(88, 112), *range(121, 145), *range(147, 170), *range(183, 207), *range(209, 233)]

# NULL_SUBCARRIERS = [0, 1, 2, 3, 4, 5, 127, 128, 129, 251, 252, 253, 254, 255]
# PILOT_SUBCARRIERS = [25, 53, 89, 117, 139, 167, 203, 231]
# USELESS_SUBCARRIERS = NULL_SUBCARRIERS + PILOT_SUBCARRIERS

# -26 to -1, 1 to 26.
# Pilots: +/- 7, 21
# Null? 62, 63, 64, 27 to 37.
# Total on-paper ones: 52 total, 48 usable.
# Real ones: 64.
# Usable count: 64 - (4) - (3) - (10) = 47?
# Seems like I've removed 5 too many.

# 27:37 are -inf. 11 null subcarriers.
# 0:1 are weirdly high/low. 2 strange subcarriers.
# 64 - 13 = 51.
# I really want to know why these numbers from the textbooks never seem to match up.
# But let's go with these 51 normal-looking ones.

ALL_CHANNELS = [*range(24), *range(26, 50), *range(62, 85), *range(88, 112), *range(121, 145), *range(147, 170), *range(183, 207), *range(209, 233)]

NULL_SUBCARRIERS = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
PILOT_SUBCARRIERS = [0, 1]
USELESS_SUBCARRIERS = NULL_SUBCARRIERS + PILOT_SUBCARRIERS

DEFAULT_FS = 100

def load_csi_data(csi_data, subcarrier_range=ALL_CHANNELS, target_sample_rate=10, lowpass=True):

    frames = csi_data.frames

    #Identify the need for source resampling.
    no_frames = len(frames)
    first_timestamp = float(frames[0].real_timestamp)
    last_timestamp = float(frames[-1].real_timestamp)

    final_timestamp = last_timestamp-first_timestamp
    average_sample_rate = no_frames/final_timestamp
    
    #Check the average sample rate is close enough to that we'd expect.
    if abs(average_sample_rate-DEFAULT_FS) > 10:

        #Ideally we'd like to use some interpolation.
        #But supposedly scipy's interp1d is slow.
        #For now, we'll stick with downsampling since we're in control of data capture.

        if average_sample_rate > DEFAULT_FS:
            downsample_factor = int(average_sample_rate / DEFAULT_FS)
            frames = frames[::downsample_factor]

    #At this point, our trace object should have an avg sampling rate of 100Hz.

    #Retrieve CSI for the data we've got now.
    csi, _, _ = get_CSI(csi_data)
    timestamps = csi_data.timestamps

    csi = np.squeeze(csi)
    csi = np.transpose(csi)
    # timestamps = [x["timestamp"] for x in trace]
    # timestamps_unscaled = [x["timestamp_low"] for x in trace]

    #Filter out unwanted subcarriers.
    csi = csi[[x for x in range(64) if x not in USELESS_SUBCARRIERS]]
    # csi = csi[[x for x in subcarrier_range]]

    #Handle Lowpass filter.
    if lowpass:
        sampling_rate = 100#Hz
        lowpass_cutoff = 10#Hz
        order = 5#n

        for x in range(csi.shape[0]):
            csi[x] = filters.lowpass(csi[x], lowpass_cutoff, sampling_rate, order)
        csi = np.nan_to_num(csi)

    csi_trans = np.transpose(csi)

    #Downsample to 10Hz.
    csi_trans = csi_trans[::10]
    timestamps = timestamps[::10]

    return csi_trans, timestamps, timestamps
    # return csi_trans, timestamps, timestamps_unscaled