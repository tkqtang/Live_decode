import numpy as np

def zc(data, threshold=10e-7):
    numOfZC = []
    channel = data.shape[0]
    length = data.shape[1]

    for i in range(channel):
        count = 0
        for j in range(1, length):
            diff = data[i, j] - data[i, j - 1]
            mult = data[i, j] * data[i, j - 1]

            if np.abs(diff) > threshold and mult < 0:
                count = count + 1
        numOfZC.append(count / length)
    return np.array(numOfZC)


def calc_time_fea(signal, fs, step=0.05, overlap=0):
    
    ch_num, d_len = signal.shape
    step_bin      = int(fs * step)
    overlap_bin   = int(fs * overlap / 2)
    avg_step      = 4
    signal        = np.pad(signal, ((0, 0), (overlap_bin, overlap_bin)), 'reflect')
    fea_len       = int(d_len / step_bin)
    m_x           = np.zeros([ch_num, fea_len])
    v_x           = np.zeros([ch_num, fea_len])
    w_x           = np.zeros([ch_num, fea_len])
    
    for i in range(fea_len):
        m_x[:, i] = np.mean(signal[:, i * step_bin:(i + 1) * step_bin + 2 * overlap_bin], axis=1)
    mpad_x = np.pad(m_x, ((0, 0), (avg_step, avg_step)), 'reflect')
    
    for i in range(fea_len):
        v_x[:, i] = np.mean(mpad_x[:, i:i + 1 + 2 * avg_step], axis=1)
    vpad_x = np.pad(v_x, ((0, 0), (avg_step, avg_step)), 'reflect')
    
    for i in range(fea_len):
        w_x[:, i] = np.mean(vpad_x[:, i:i + 1 + 2 * avg_step], axis=1)
    p_x = m_x - w_x
    r_x = np.abs(p_x)
    P_w = np.power(w_x, 2)
    P_r = np.power(r_x, 2)
    z_p = np.zeros([ch_num, fea_len])
    for i in range(fea_len):
        z_p[:, i] = zc(p_x[:, i:i + 1 + 2 * avg_step])
    fea = np.r_[w_x, P_w, P_r, z_p, r_x]
    
    return fea



