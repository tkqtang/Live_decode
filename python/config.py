import os
import toml


class Initializer:
    def __init__(self, filepath, verbose=False):
        if os.path.isfile(filepath):
            self.config_file = toml.load(filepath)
        else:
            print('Using default due to missing config file.')

        self.config = self.get_defaults()
        self.check_defaults()
        if verbose:
           print_configs(self.config)

    def __getitem__(self, key):
        return self.config[key]

    def get_defaults(self):

        Database = {
            'data_path': '',
            'fs': 30000,
            'extract_time_potin':1.5,
            'time_length':1,
            'down_sampling_fs': 2000,
            'filter': ['high', '15'],
            'notch_freq': [50, 100, 150, 200],
            'channel': []
        }

        Analysis = {
                    'feature': 'time',
                    'signal_step': 0.005,
                    'signal_overlap': 0}

        Decoder = {'decoder_path': '',
                    }

        config = {'Database': Database, 'Analysis': Analysis, 'Decoder': Decoder}
        return config

    def check_defaults(self):
        """
        Usage:
        check the default config with the configuration file *.ini. If there is corresponding key in the *.ini file,
        then change the default value to that in *.ini file. Otherwise, keep the default value.
        -----------------------------------------------------------------------
        Params:
        None
        -----------------------------------------------------------------------
        Returns:
        None
        """
        for sec_key in self.config.keys():
            if sec_key in self.config_file:
                for key, value in self.config[sec_key].items():
                    if key in self.config_file[sec_key] and self.config_file[sec_key][key]:
                        self.config[sec_key][key] = self.config_file[sec_key][key]

    def get_config(self):
        return self.config_file


def print_configs(configs):
    for p in configs.keys():
        if isinstance(configs[p], dict):
            print('[{:s}]'.format(p))
            print_configs(configs[p])
        else:
            print('{:s}: {:s}'.format(p, str(configs[p])))