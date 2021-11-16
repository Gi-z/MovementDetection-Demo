import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from matplotlib import animation
from numpy.core.fromnumeric import var

from CSIKit.util import filters

from stats import slidingpeaks

mpl.use('TkAgg')

def heatmap(csi, timestamps):
    extent = [0, timestamps[-1], 1, csi.shape[0]]

    _, ax = plt.subplots()
    im = ax.imshow(csi, cmap="jet", aspect="auto", extent=extent)

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Amplitude (dBm)")

    plt.xlabel("Time (s)")
    plt.ylabel("Subcarrier Index")

    plt.title("Channel State Information")

    plt.show()

def heatmap_3d(csi, timestamps):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    csi = np.transpose(csi)

    x = np.arange(csi.shape[0])
    y = timestamps

    x, y = np.meshgrid(x, y)

    csi = np.transpose(csi)

    surf = ax.plot_surface(x, y, csi, cmap="jet", linewidth=0, antialiased=True)
    
    ax.set_xlabel('Subcarrier Index')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Amplitude (dBm)')

    fig.colorbar(surf)

    plt.show()

# def plot_movement(csi, sti_values, corr_values, timestamps, filename, containsmovement_threshold, moving_threshold, notmoving_threshold):

#     # filt_sti_norm = filt_sti - np.mean(filt_sti)
#     # filt_corr_norm = filt_corr - np.mean(filt_corr)

#     # sign_sti = np.sign(filt_sti_norm)
#     # sign_corr = np.negative(np.sign(filt_corr_norm))

#     # movement_conf = {
#     #     -1: "No Movement",
#     #     1: "Movement"
#     # }

#     # bin_sti = [movement_conf[x] for x in sign_sti]
#     # bin_corr = [movement_conf[x] for x in sign_corr]

#     # var_sti = filters.running_variance(sti_values, 5)
#     var_corr = filters.running_variance(corr_values, 10)

#     # std_sti = filters.running_stdev(sti_values, 5)
#     std_corr = filters.running_stdev(corr_values, 10)

#     diffs, markers, signals, thresh_mov, thresh_nomov = slidingpeaks(var_corr, corr_values, containsmovement_threshold, moving_threshold, notmoving_threshold)

#     #Plot STI Values.
#     # plt.subplot(2, 2, 1)

#     # plt.title("Signal Tendency Index")
#     # plt.xlabel("Time (s)")
#     # # plt.ylabel("Signal Tendency Index (STI)")

#     # plt.plot(timestamps, sti_values, color="blue", label="STI")
#     # plt.plot(timestamps, filt_sti, color="red", label="STI (filtered)")

#     # plt.legend()

#     plt.subplot(3, 3, 1)
#     extent = [0, timestamps[-1], 1, csi.shape[1]]

#     plt.imshow(np.transpose(csi), cmap="jet", aspect="auto", extent=extent)

#     plt.xlabel("Time (s)")
#     plt.ylabel("Subcarrier Index")

#     plt.title("Channel State Information")

#     # pcc_thresh = 0.92
#     pcc_thresh = containsmovement_threshold

#     #Plot Correlation Coefficient
#     plt.subplot(3, 3, 4)

#     plt.title("Pearson Correlation Coefficient")
#     plt.xlabel("Time (s)")
#     # plt.ylabel("Pearson Correlation Coefficient")

#     plt.plot(timestamps, corr_values, color="blue", label="PCC")
#     plt.plot(timestamps, np.full((len(timestamps)), fill_value=pcc_thresh), color="red", label="Threshold")

#     plt.legend()



#     plt.subplot(3, 3, 3)

#     mov_vals = []
#     for x in corr_values:
#         if x < pcc_thresh:
#             mov_vals.append(1)
#         else:
#             mov_vals.append(0)
#     mov_vals = np.array(mov_vals)

#     # chunk_size = 10
#     # for i in range(len(mov_vals)):
#     #     if i % chunk_size == 0:
#     #         #Get previous second's worth of data and check for movement.
#     #         win = mov_vals[i-chunk_size:i]
#     #         if 1 in win:
#     #             mov_vals[i-chunk_size:i] = 1

#     plt.title("PCC Thresh")
#     plt.xlabel("Time (s)")
#     plt.plot(timestamps, mov_vals, color="red")

#     #PCC Variance Plot
#     plt.subplot(3, 3, 7)

#     plt.title("PCC Running Variance (Movement)")
#     plt.xlabel("Time (s)")
#     plt.plot(timestamps, var_corr, "-gD", color="red", markevery=markers)

#     #PCC Stdev Plot
#     plt.subplot(3, 3, 5)

#     plt.title("PCC Running Standard Deviation (Movement)")
#     plt.xlabel("Time (s)")
#     plt.plot(timestamps, std_corr, color="red")

#     plt.subplot(3, 3, 8)

#     plt.title("Movement")
#     plt.xlabel("Time (s)")
#     plt.plot(timestamps, signals, color="red")

#     plt.subplot(3, 3, 9)

#     plt.title("Mean Diffs (+/- 0.5s)")
#     plt.xlabel("Time (s)")
#     plt.plot(timestamps, diffs, color="blue")
#     plt.plot(timestamps, thresh_mov, color="red", label="Movement Threshold")
#     plt.plot(timestamps, thresh_nomov, color="green", label="No Movement Threshold")

#     plt.suptitle(filename)
#     plt.show()

# def plot_movement(csi, sti_values, corr_values, timestamps, filename, containsmovement_threshold, moving_threshold, notmoving_threshold):

#     var_corr = filters.running_variance(corr_values, 10)
#     std_corr = filters.running_stdev(corr_values, 10)

#     diffs, markers, signals, thresh_mov, thresh_nomov = slidingpeaks(var_corr, corr_values, containsmovement_threshold, moving_threshold, notmoving_threshold)

#     tfinal = len(csi)
#     sub_extent = csi.shape[1]

#     mov_vals = []
#     for x in corr_values:
#         if x < containsmovement_threshold:
#             mov_vals.append(1)
#         else:
#             mov_vals.append(0)
#     mov_vals = np.array(mov_vals)

#     # plt.subplot(3, 3, 1)
#     fig, ax = plt.subplots(3, 3, figsize=(3, 3))
    
#     fig.delaxes(ax[0][1])
#     fig.delaxes(ax[0][2])
#     fig.delaxes(ax[1][2])

#     heatmap_ax = ax[0][0]

#     heatmap_ax.set_title("CSI Heatmap")
#     heatmap_ax.set_xlabel("Time (s)")
#     heatmap_ax.set_ylabel("Subcarrier Index")

#     pcc_ax = ax[1][0]

#     pcc_ax.set_xlabel("Time (s)")
#     pcc_ax.set_ylabel("PCC")

#     pcc_thresh_ax = ax[1][1]

#     pcc_thresh_ax.set_xlabel("Time (s)")
#     pcc_thresh_ax.set_ylabel("PCC")

#     pcc_running_ax = ax[2][0]

#     pcc_running_ax.set_xlabel("Time (s)")
#     pcc_running_ax.set_ylabel("Variance")

#     mov_ax = ax[2][1]

#     mov_ax.set_xlabel("Time (s)")
#     mov_ax.set_ylabel("Movement")

#     mean_diffs_ax = ax[2][2]

#     mean_diffs_ax.set_xlabel("Time (s)")
#     mean_diffs_ax.set_ylabel("Mean Diff")

#     i = 1

#     extent = [0, timestamps[i], 1, csi.shape[1]]
#     heatmap_ax.set_title("Channel State Information")
#     # im = heatmap_ax.imshow(np.transpose(csi[:i]), cmap="jet", aspect="auto", extent=extent)
#     # im = heatmap_ax.imshow(np.transpose(csi[:i]), cmap="jet", aspect="auto")
#     heatmap_ax.set_xlim([0, timestamps[-1]])
#     heatmap_ax.set_ylim([1, 48])

#     pcc_ax.set_title("Pearson Correlation Coefficient")
#     pcc_line, = pcc_ax.plot(timestamps[:i], corr_values[:i])
#     pcc_ax.set_xlim([0, timestamps[-1]])
#     pcc_ax.set_ylim([min(corr_values), max(corr_values)])

#     pcc_thresh_ax.set_title("PCC Threshold-based Movement")
#     pcc_thresh_line, = pcc_thresh_ax.plot(timestamps[:i], mov_vals[:i], color="red")
#     pcc_thresh_ax.set_xlim([0, timestamps[-1]])
#     pcc_thresh_ax.set_ylim([-0.2, 1.2])

#     pcc_running_ax.set_title("PCC Running Variance")
#     pcc_running_line, = pcc_running_ax.plot(timestamps[:i], var_corr[:i], color="red")
#     pcc_running_ax.set_xlim([0, timestamps[-1]])
#     pcc_running_ax.set_ylim([min(var_corr), max(var_corr)])

#     mov_ax.set_title("Mean Diffs-based Movement")
#     mov_line, = mov_ax.plot(timestamps[:i], signals[:i], color="red")
#     mov_ax.set_xlim([0, timestamps[-1]])
#     mov_ax.set_ylim([-0.2, 1.2])

#     mean_diffs_ax.set_title("Mean Diffs")
#     mean_diffs_diffs_line, = mean_diffs_ax.plot(timestamps[:i], diffs[:i], color="blue")
#     mean_diffs_ax.plot(timestamps, thresh_mov, color="red", label="Movement Threshold")
#     mean_diffs_ax.plot(timestamps, thresh_nomov, color="green", label="No Movement Threshold")
#     mean_diffs_ax.set_xlim([0, timestamps[-1]])
#     mean_diffs_ax.set_ylim([min(var_corr), max(var_corr)])

#     def animate(i):

#         o = 0

#         if i > len(timestamps):
#             o = timestamps[-1]
#         else:
#             o = timestamps[i]

#         extent = [0, o, 1, csi.shape[1]]
#         im = heatmap_ax.imshow(np.transpose(csi[:i]), cmap="jet", aspect="auto", extent=extent)

#         # im.set_array(np.transpose(csi[:i]))

#         pcc_line.set_xdata(timestamps[:i])
#         pcc_line.set_ydata(corr_values[:i])

#         pcc_thresh_line.set_xdata(timestamps[:i])
#         pcc_thresh_line.set_ydata(mov_vals[:i])

#         pcc_running_line.set_xdata(timestamps[:i])
#         pcc_running_line.set_ydata(var_corr[:i])

#         mov_line.set_xdata(timestamps[:i])
#         mov_line.set_ydata(signals[:i])

#         mean_diffs_diffs_line.set_xdata(timestamps[:i])
#         mean_diffs_diffs_line.set_ydata(diffs[:i])

#         return pcc_line, pcc_thresh_line, pcc_running_line, mov_line, mean_diffs_diffs_line, im, 

#     fig.set_size_inches(10, 10, True)

#     anim = animation.FuncAnimation(fig, animate, frames=len(csi), interval=1, blit=True)
#     anim.save("test.mp4", dpi=100, fps=10)

#     # pcc_anim = animation.FuncAnimation(fig, pcc_animate, frames=len(timestamps)+1, interval=1, blit=False)

#     # #Plot Correlation Coefficient
#     # plt.subplot(3, 3, 4)

#     # plt.title("Pearson Correlation Coefficient")
#     # plt.xlabel("Time (s)")

#     # plt.plot(timestamps, corr_values, color="blue", label="PCC")
#     # plt.plot(timestamps, np.full((len(timestamps)), fill_value=containsmovement_threshold), color="red", label="Threshold")

#     # plt.legend()

#     # plt.subplot(3, 3, 3)

#     # plt.title("PCC Thresh")
#     # plt.xlabel("Time (s)")
#     # plt.plot(timestamps, mov_vals, color="red")

#     # #PCC Variance Plot
#     # plt.subplot(3, 3, 7)

#     # plt.title("PCC Running Variance (Movement)")
#     # plt.xlabel("Time (s)")
#     # plt.plot(timestamps, var_corr, "-gD", color="red", markevery=markers)

#     # #PCC Stdev Plot
#     # plt.subplot(3, 3, 5)

#     # plt.title("PCC Running Standard Deviation (Movement)")
#     # plt.xlabel("Time (s)")
#     # plt.plot(timestamps, std_corr, color="red")

#     # plt.subplot(3, 3, 8)

#     # plt.title("Movement")
#     # plt.xlabel("Time (s)")
#     # plt.plot(timestamps, signals, color="red")

#     # plt.subplot(3, 3, 9)

#     # plt.title("Mean Diffs (+/- 0.5s)")
#     # plt.xlabel("Time (s)")
#     # plt.plot(timestamps, diffs, color="blue")
#     # plt.plot(timestamps, thresh_mov, color="red", label="Movement Threshold")
#     # plt.plot(timestamps, thresh_nomov, color="green", label="No Movement Threshold")

#     # plt.suptitle(filename)
#     # mng = plt.get_current_fig_manager()
#     # mng.full_screen_toggle()
#     # plt.show()

def plot_movement(path, csi, sti_values, corr_values, timestamps, timestamps_unscaled, filename, containsmovement_threshold, moving_threshold, notmoving_threshold):

    var_corr = filters.running_variance(corr_values, 10)
    std_corr = filters.running_stdev(corr_values, 10)

    diffs, markers, signals, thresh_mov, thresh_nomov = slidingpeaks(var_corr, corr_values, containsmovement_threshold, moving_threshold, notmoving_threshold)

    mov_vals = []
    for x in corr_values:
        if x < containsmovement_threshold:
            mov_vals.append(1)
        else:
            mov_vals.append(0)
    mov_vals = np.array(mov_vals)

    mov_vals2 = []
    for x in sti_values:
        if x > 0.8:
            mov_vals2.append(1)
        else:
            mov_vals2.append(0)
    mov_vals2 = np.array(mov_vals2)

    plt.subplot(3, 3, 1)
    extent = [0, timestamps[-1], 1, csi.shape[1]]

    plt.imshow(np.transpose(csi), cmap="jet", aspect="auto", extent=extent)

    plt.xlabel("Time (s)")
    plt.ylabel("Subcarrier Index")

    plt.title("Channel State Information")

    #Plot Correlation Coefficient
    plt.subplot(3, 3, 4)

    plt.title("Pearson Correlation Coefficient")
    plt.xlabel("Time (s)")

    plt.plot(timestamps, corr_values, color="blue", label="PCC")
    plt.plot(timestamps, np.full((len(timestamps)), fill_value=containsmovement_threshold), color="red", label="Threshold")

    plt.legend()

    plt.subplot(3, 3, 3)

    chunk_size = 10
    for i in range(len(mov_vals)):
        if i % chunk_size == 0:
            #Get previous second's worth of data and check for movement.
            win = mov_vals[i-chunk_size:i]
            if 1 in win:
                mov_vals[i-chunk_size:i] = 1

    plt.title("PCC Thresh")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, mov_vals, color="red")

    plt.subplot(3, 3, 2)
    plt.title("STI")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, sti_values, color="red")

    plt.subplot(3, 3, 6)
    plt.title("STI Thresh (Movement)")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, mov_vals2, color="red")

    #PCC Variance Plot
    plt.subplot(3, 3, 7)

    plt.title("PCC Running Variance (Movement)")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, var_corr, "-gD", color="red", markevery=markers)

    #PCC Stdev Plot
    plt.subplot(3, 3, 5)

    plt.title("PCC Running Standard Deviation (Movement)")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, std_corr, color="red")

    plt.subplot(3, 3, 8)

    plt.title("Movement")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, signals, color="red")

    plt.subplot(3, 3, 9)

    plt.title("Mean Diffs (+/- 0.5s)")
    plt.xlabel("Time (s)")
    plt.plot(timestamps, diffs, color="blue")
    plt.plot(timestamps, thresh_mov, color="red", label="Movement Threshold")
    plt.plot(timestamps, thresh_nomov, color="green", label="No Movement Threshold")

    plt.suptitle(filename)
    plt.show()

    # csvs = []
    # timestamps_unscaled = timestamps_unscaled[::10]
    # for timestamp, val in zip(timestamps_unscaled, signals):
    #     csvs.append("{},{}\n".format(int(val), int(timestamp)))
    # with open(path[:-5]+"_predicted.csv", "w+") as file:
    #     for x in csvs:
    #         file.write(x)

    # csvs = []
    # for timestamp, val in zip(timestamps_unscaled, mov_vals2):
    #     csvs.append("{},{}\n".format(int(val), int(timestamp)))
    # with open(path[:-5]+"_predicted_sti.csv", "w+") as file:
    #     for x in csvs:
    #         file.write(x)