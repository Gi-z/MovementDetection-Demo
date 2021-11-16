import numpy as np

def get_h_hat_t(csi_vec):
    csi_mean = np.mean(csi_vec)

    translation = csi_vec - csi_mean
    scaling = np.std(csi_vec)

    return translation/scaling

def get_sti(csi_vec_1, csi_vec_2):
    h1 = get_h_hat_t(csi_vec_1)
    h2 = get_h_hat_t(csi_vec_2)

    return np.linalg.norm(h1 - h2)

def get_correlation_coefficient(csi_vec_1, csi_vec_2):
    return np.corrcoef([csi_vec_1, csi_vec_2])[0,1]

def slidingpeaks(y, corr, containsmovement_threshold, moving_threshold, notmoving_threshold):
    window_length = 5
    i = 0

    signals = np.zeros(len(y))
    markers = []
    diffs = []

    is_moving = False

    max_val = max(y)

    while i < len(y):
        first_window = y[i:i+window_length]
        second_window = y[i+window_length:i+window_length*2]

        first_mean = np.mean(first_window)/max_val
        second_mean = np.mean(second_window)/max_val

        diff = np.abs(second_mean-first_mean)

        if min(corr) < containsmovement_threshold:
            if is_moving:
                #Large diff means movement continues.
                #Small diff means return to steady.
                if diff < notmoving_threshold:
                    is_moving = False
                else:
                    markers.append(i)
            else:
                if diff > moving_threshold:
                    markers.append(i)
                    is_moving = True

        signals[i] = int(is_moving)
        diffs.append(diff)

        i += 1

    thresh_mov = np.full(len(y), fill_value=moving_threshold)
    thresh_nomov = np.full(len(y), fill_value=notmoving_threshold)

    #Merges movement samples to chunk_size*fs precision.
    #Assumes 10Hz.
    chunk_size = 10
    for i in range(len(signals)):
        if i % chunk_size == 0:
            #Get previous second's worth of data and check for movement.
            win = signals[i-chunk_size:i]
            if 1 in win:
                signals[i-chunk_size:i] = 1

    return (diffs, markers, signals, thresh_mov, thresh_nomov)