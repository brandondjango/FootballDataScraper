import os
import yaml

#use yamls to avoid dbs for now
class ConfigUtil:
    CONFIG_ROOT = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_config_path(config_type):
        config_yaml_path = ConfigUtil.CONFIG_ROOT + '/config_paths.yaml'
        with open(config_yaml_path, 'r') as file:
            config_paths = yaml.safe_load(file)
        return ConfigUtil.CONFIG_ROOT + config_paths[config_type]

    @staticmethod
    def get_current_configs(config_type):
        config_path = ConfigUtil.get_config_path(config_type)

        with open(config_path, 'r') as file:
            current_configs = yaml.safe_load(file)

        return current_configs


    @staticmethod
    def add_config_value(key, value, config_to_change):
        #get configurations
        configs_to_change = ConfigUtil.get_current_configs(config_to_change)
        if configs_to_change is None:
            configs_to_change = {}

        #update config
        configs_to_change[key] = value

        #write update
        with open(ConfigUtil.get_config_path(config_to_change), 'w') as file:
            yaml.dump(configs_to_change, file, default_flow_style=False)