from joblib import load
from config import Initializer
from pre_process import process_raw_data, down_sample_signal, filt, notch_filt, min_max_normalize
from extract_feature import calc_time_fea
import numpy as np
import warnings

def load_model(model_path):
    # 加载模型
    model = load(model_path)
    return model

def predict(decoder, X_data):
    return decoder.predict(X_data)


def extract_raw_data(data_path):
    pass
    # raw_data = np.random.rand(1, 20000)
    # return raw_data


def pre_process(raw_data, extract_time_potin, time_length, fs, dn_fs, filt_type=None, filt_params=None, notch_filt_params=None):
    # signal  = process_raw_data(raw_data, extract_time_potin, time_length, fs)
    signal  = raw_data
    signal  = down_sample_signal(signal, fs, dn_fs)
    if filt_type is not None or filt_params is not None:
        signal  = filt(signal, filt_type=filt_type, params=filt_params, dn_fs=dn_fs)
    if notch_filt_params is not None:
        signal  = notch_filt(signal, params=notch_filt_params, dn_fs=dn_fs)
    
    return min_max_normalize(signal)
    
def extract_feature(signal, fs, signal_step, signal_overlabp):
    x_data = calc_time_fea(signal, fs=fs, step=signal_step, overlap=signal_overlabp)
    x_data = x_data.reshape(1, -1)
    return x_data


def align_data(data, dimension, fill_value=0):
    if data.ndim == 1:
        data = data.reshape(1, -1)
    n, d = data.shape
    if d > dimension:
        data = data[:, :dimension]  # 截断多余的列
    elif d < dimension:
        padding = np.full((n, dimension - d), fill_value)  # 填充缺失的列
        data = np.hstack((data, padding))

    return data


def main(config_path='', raw_data=None):
    warnings.simplefilter("ignore")
    # read_config
    if config_path == '':
        config_path  = "./config/settings.toml"
    parameters         = Initializer(config_path)
    fs                 = parameters['Database']['fs']
    dn_fs              = parameters['Database']['down_sampling_fs']
    extract_time_potin = parameters['Database']['extract_time_potin']
    time_length        = parameters['Database']['time_length']
    data_path          = parameters['Database']['data_path']
    filt_type          = parameters['Database']['filter'][0]
    filt_params        = (int)(parameters['Database']['filter'][1])
    notch_filt_params  = parameters['Database']['notch_freq']
    channel            = parameters['Database']['channel']
    signal_step        = parameters['Analysis']['signal_step']
    signal_overlap     = parameters['Analysis']['signal_overlap']
    decoder_path       = parameters['Decoder']['decoder_path']
    channel            = np.array(channel) - 1

    # extract_feature
    if raw_data is None:
        raw_data     = extract_raw_data(data_path)      # raw_data应是n * d的形式
    else:
        raw_data = np.array(raw_data)
        if raw_data.ndim == 1:
            raw_data = raw_data.reshape(1, -1)
        else:
            raw_data = raw_data[channel, :]

    signal       = pre_process(raw_data, extract_time_potin, time_length, fs, dn_fs, filt_type, filt_params, notch_filt_params)
    x_data       = extract_feature(signal, dn_fs, signal_step, signal_overlap)
    
    # load decoder
    decoder      = load_model(decoder_path)
    dimension    = decoder.n_features_in_
    x_data       = align_data(x_data, dimension)
    y_pred       = predict(decoder, x_data)
    
    return y_pred


if __name__ == "__main__":
    config_path  = "./config/settings.config"
    main(config_path)


