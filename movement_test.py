from CSIKit.reader import CSVBeamformReader

from data_handler import load_csi_data
from stats import get_sti, get_correlation_coefficient

import plot
import time

startTime = time.time()

# filename = "data/environment1/movement1/movement1_1.csv"
# filename = "data/environment1/movement1/movement1_2.csv"
# filename = "data/environment1/movement1/movement1_3.csv"
# filename = "data/environment1/movement1/movement1_4.csv"
# filename = "data/environment1/movement1/movement1_5.csv"

# filename = "data/environment1/movement2/movement2_1619789649.csv"
# filename = "data/environment1/movement2/movement2_1619789687.csv"
# filename = "data/environment1/movement2/movement2_1619789723.csv"
# filename = "data/environment1/movement2/movement2_1619789766.csv"
# filename = "data/environment1/movement2/movement2_1619789806.csv"

# filename = "data/environment1/movement3/movement3_1619789958.csv"
# filename = "data/environment1/movement3/movement3_1619789999.csv"
# filename = "data/environment1/movement3/movement3_1619790037.csv"
# filename = "data/environment1/movement3/movement3_1619790081.csv"
# filename = "data/environment1/movement3/movement3_1619790125.csv"

# filename = "data/environment1/movement4/movement4_1619790203.csv"
# filename = "data/environment1/movement4/movement4_1619790224.csv"
# filename = "data/environment1/movement4/movement4_1619790243.csv"
# filename = "data/environment1/movement4/movement4_1619790264.csv"
# filename = "data/environment1/movement4/movement4_1619790298.csv"

# filename = "data/environment1/movement5/movement5_1619790327.csv"
# filename = "data/environment1/movement5/movement5_1619790344.csv"
# filename = "data/environment1/movement5/movement5_1619790369.csv"
# filename = "data/environment1/movement5/movement5_1619790385.csv"
# filename = "data/environment1/movement5/movement5_1619790403.csv"

filename = "data/house_experiments/movement1/movement1_1_config1.csv"
# filename = "data/house_experiments/movement1/movement1_2_config1.csv"
# filename = "data/house_experiments/movement1/movement1_3_config1.csv"
# filename = "data/house_experiments/movement1/movement1_4_config1.csv"
# filename = "data/house_experiments/movement1/movement1_5_config1.csv"

# filename = "data/house_experiments/movement1/movement1_1_config2.csv"
# filename = "data/house_experiments/movement1/movement1_2_config2.csv"
# filename = "data/house_experiments/movement1/movement1_3_config2.csv"
# filename = "data/house_experiments/movement1/movement1_4_config2.csv"
# filename = "data/house_experiments/movement1/movement1_5_config2.csv"

# filename = "data/house_experiments/movement1/movement1_kitchen_config1.csv"
# filename = "data/house_experiments/movement1/movement1_kitchen2_config1.csv"
# filename = "data/house_experiments/movement1/movement1_kitchen3_config1.csv"

# filename = "data/house_experiments/movement1/movement1_masterbedroom1_config2.csv"
# filename = "data/house_experiments/movement1/movement1_masterbedroom2_config2.csv"
# filename = "data/house_experiments/movement1/movement1_masterbedroom3_config2.csv"

reader = CSVBeamformReader()
csi_data = reader.read_file(filename)

csi, timestamps, timestamps_unscaled = load_csi_data(csi_data)

#ESP32 setup (Day 1).
# mean_corr = 0.9917
# diff_corr = 0.0246

#ESP32 setup (Day 2).
# mean_corr = 0.9962
# diff_corr = 0.0117

#ESP32 setup house_experiments config1
mean_corr = 0.9971
diff_corr = 0.0080

#ESP32 setup house_experiments config2
# mean_corr = 0.9962
# diff_corr = 0.0083

# plot.heatmap_3d(csi, timestamps)
# plot.heatmap(np.transpose(csi), timestamps)

#%diff thresholds.
moving_threshold = 0.15
# moving_threshold = 0.10
notmoving_threshold = 0.05
# notmoving_threshold = 0.10

#PCC-activation threshold.
#Let's try and establish this by calibrating with a "no presence" example.
#Then we can use take a multiplier of the average max-min diff as our threshold.
# containsmovement_threshold = 0.92
containsmovement_threshold = mean_corr-(diff_corr*2)

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
    
    prev_frame = frame

#Hack to re-add scaled timestamps.
first_timestamp = timestamps[0]
for i, stamp in enumerate(timestamps):
    stamp -= first_timestamp
    timestamps[i] = stamp

timestamps = sorted(timestamps[1:])
timestamps_unscaled = sorted(timestamps_unscaled[1:])

plot.plot_movement(filename, csi, sti_values, corr_values, timestamps, timestamps_unscaled, reader.filename, containsmovement_threshold, moving_threshold, notmoving_threshold)

endTime = time.time()

print("Took {:.2f}s to run.".format(endTime-startTime))