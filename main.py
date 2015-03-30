import logging
import os
import sys
import imp


import yaml
import schedule
import time

#https://github.com/dbader/schedule/blob/master/FAQ.rst

class PluginManager():
    def __init__(self, config):
        self.index = {}
        self.config = config 

    def load_plugins(self):
        for file_ in os.listdir(self.config[0]['plugin_dir']):
            full_path   = '%s/%s' % (self.config[0]['plugin_dir'], file_)
            plugin_name = self.plugin_basename(full_path)
            extension   = file_.split('.')[-1]

            if extension == 'py' and self.validate_plugin(plugin_name) == True:
                plugin = imp.load_source(plugin_name, full_path)
                self.index[plugin_name] = {'full_path':full_path, 'plugin':plugin}

                logging.info('loaded plugin: %s' % plugin_name)

                interval = self.config[0][plugin_name]['interval']
    
                if interval <= 0:
                    logging.info('interval is less than 0, cannot schedule')
                    continue

                schedule.every(interval).minutes.do(plugin.run)

                logging.info('scheduling plugin for execution every %s minutes' % (interval))


    
    def validate_plugin(self, plugin_name):
        for item in self.config:
            if plugin_name in item:
                logging.info('plugin found in config: %s' % plugin_name)
                return True

        logging.info('plugin not in config: %s' % plugin_name)
        return False


    def plugin_basename(self, path):
        return os.path.basename(path).split('.py')[0].strip()


    def remove_plugin(self, path):
        del self.index[path]


class ConfigManager():
    def __init__(self):
        self.base_dir    = os.getcwd()
        self.config_path = '%s/config.yml' % (self.base_dir)
        self.config = {}
         
        logging.basicConfig(filename='%s/log' % (self.base_dir), level=logging.DEBUG)

        if not os.path.exists(self.config_path):
            logging.critical('Could not locate config: %s' % (self.config_path))
            return 1

        # Docs for YAML: http://pyyaml.org/wiki/PyYAMLDocumentation
        with open(self.config_path) as cfg:
            self.config = yaml.load(cfg.read())

        self.config[0]['db_path']    = '%s/items.db' % self.base_dir # Fix for MariaDB
        self.config[0]['plugin_dir'] = '%s/plugins'  % self.base_dir
        
        sys.path.append(self.config[0]['plugin_dir'])

    def get_config(self):
        return self.config

if __name__ == '__main__':
    cfg_mgr = ConfigManager()
    plg_mgr = PluginManager(cfg_mgr.get_config())
    plg_mgr.load_plugins()

    while True:
        schedule.run_pending()
        time.sleep(1)




# load plugins
# run plugins by time

