from scipy.signal import stft, butter, filtfilt, iirnotch
import numpy as np


def min_max_normalize(data):
    data_min = data.min(axis=1, keepdims=True)
    data_max = data.max(axis=1, keepdims=True)
    data_scaled = (data - data_min) / (data_max - data_min)
    return data_scaled


def process_raw_data(raw_data, extract_time_potin, time_legth, fs):
    
    """
    """
    data_length    = int(time_legth * fs)
    extract_point  = raw_data.shape[1] - int(extract_time_potin * fs)

    return raw_data[:, extract_point: extract_point + data_length] 

def down_sample_signal(signal, fs, dn_fs):
    dn_ratio    = fs / dn_fs
    r_ch, r_len = signal.shape
    d_len       = np.ceil(r_len / dn_ratio).astype(np.uint32)
    dn_signal   = np.zeros([r_ch, d_len])

    for i in range(d_len):
        dn_signal[:, i] = np.mean(signal[:, int(i * dn_ratio):int((i + 1) * dn_ratio)], axis=1)
    
    return dn_signal

# filter = ["high", "15"]

def filt(signal, filt_type, params, dn_fs):
    """
    Usage:
    filt the signal with different types of filters
    --------------------------------------------------------------------------
    Parameters:
    filt_type: the filter type, including low pass, high pass and band pass
    params: the filter parameters, including the filter cut-off
    --------------------------------------------------------------------------
    Return:
    the filtered data
    """
    butter_tap = 5
    Wn         = None
    if isinstance(params, list):
        Wn = []
        for p in params:
            Wn.append(2 * p / dn_fs)
    else:
        Wn = 2 * params / dn_fs
    if filt_type == "low":
        b, a = butter(butter_tap, Wn, 'low')
    elif filt_type == "high":
        b, a = butter(butter_tap, Wn, 'high')
    elif filt_type == "bandpass":
        b, a = butter(butter_tap, Wn, 'bandpass')
    filter_signal = filtfilt(b, a, signal)   
    return filter_signal

# notch_freq = [50, 100, 150, 200]
def notch_filt(signal, params, dn_fs, Q=30):
    if isinstance(params, list):
        for p in params:
            b, a   = iirnotch(p, Q, dn_fs)
            signal = filtfilt(b, a, signal)
    else:
        b, a   = iirnotch(params, Q, dn_fs)
        signal = filtfilt(b, a, signal)
    return signal


