import os
import yaml

from definitions import CONFIG_ROOT


#use yamls to avoid dbs for now
class ConfigUtil:

    @staticmethod
    def get_config_path(config_type: str):
        config_yaml_path = CONFIG_ROOT + '/config_paths.yaml'
        with open(config_yaml_path, 'r') as file:
            config_paths = yaml.safe_load(file)
        return CONFIG_ROOT + config_paths[config_type]

    @staticmethod
    def get_current_configs(config_type: str):
        config_path = ConfigUtil.get_config_path(config_type)

        with open(config_path, 'r') as file:
            current_configs = yaml.safe_load(file)

        return current_configs


    @staticmethod
    def add_config_value(key: str, value: str, config_to_change: str):
        #get configurations
        configs_to_change = ConfigUtil.get_current_configs(config_to_change)
        if configs_to_change is None:
            configs_to_change = {}

        #update config
        configs_to_change[key] = value

        #write update
        with open(ConfigUtil.get_config_path(config_to_change), 'w') as file:
            yaml.dump(configs_to_change, file, default_flow_style=False)

    @staticmethod
    def get_config_value(key: str, config_to_fetch: str):
        #get configurations
        fetched_configs = ConfigUtil.get_current_configs(config_to_fetch)

        #return config
        return fetched_configs[key]


