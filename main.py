import logging
import os
import sys
import imp
import copy


import yaml
import schedule
import time

from sql.db_connect import Connect


class Helper:
    @staticmethod
    def get_item(config, name):

        for i in range(len(config)):
            args = {}
            item_name = config[i].keys()[0]

            if item_name != name:
                continue

            item_data = config[i][item_name]

            for arg in item_data:
                args[arg] = item_data[arg]

            return item_data, args
    
    @staticmethod
    def yield_items(config):
        for i in range(len(config)):
            args = {}
            item_name = config[i].keys()[0]
            item_data = config[i][item_name]

            yield item_name, item_data


class Core():
    def __init__(self):

        cfg_manager = ConfigManager()
        self.global_cfg = cfg_manager.get_global_cfg()
        self.plugin_cfg = cfg_manager.get_plugin_cfg()
        self.settings   = cfg_manager.get_settings()
   
        self.loaded_plugins = {}
        
        self.db = Connect(self.settings['db_path'])
    
        if self.db:
            logging.info('connected to database')

        else:
            logging.info('could not connect to database')
            return 


    def load_plugin(self, name):

        if name in self.loaded_plugins:
            return self.loaded_plugins[name]

        plugin = False

        for file_ in os.listdir(self.settings['plugin_dir']):
            full_path   = '%s/%s' % (self.settings['plugin_dir'], file_)
            plugin_name = self.plugin_basename(full_path)
            extension   = file_.split('.')[-1]
           
            if plugin_name != name:
                continue

            if extension == 'py':
                plugin = imp.load_source(plugin_name, full_path)
                logging.info('loaded plugin: %s' % (plugin_name))

                # Save the plugin
                self.loaded_plugins[plugin_name] = plugin
                return plugin

        return False 

    def execute_config(self):

        for plugin_name,args in Helper.yield_items(self.plugin_cfg):
            logging.debug('scheduling plugin: %s, args: %s' % (plugin_name, args))
            if 'interval' not in args:
                logging.critical('interval not set for: %s' % (plugin_name))
                return False

            # Modify the arguments so the execute function gets what it needs. 
            copy_args = copy.copy(args) 
            del copy_args['interval']

            copy_args['plugins'] = self.load_plugin
            copy_args['db']      = self.db

            # See if plugin is already loaded
            if plugin_name not in self.loaded_plugins:
                self.load_plugin(plugin_name)

            #https://github.com/dbader/schedule/blob/master/FAQ.rst
            schedule.every(args['interval']).minutes.do(self.loaded_plugins[plugin_name].execute, **copy_args)

    

    def plugin_basename(self, path):
        return os.path.basename(path).split('.py')[0].strip()


    def remove_plugin(self, path):
        del self.index[path]


class ConfigManager():
    def __init__(self, g_cfg_path=None, p_cfg_path=None):
        self.base_dir = os.getcwd()

        if not g_cfg_path:
            self.g_cfg_path = '%s/global.yml'  % (self.base_dir)
        
        if not p_cfg_path:
            self.p_cfg_path = '%s/plugins.yml' % (self.base_dir)

        self.p_cfg      = {}
        self.g_cfg      = {}
        self.settings   = {}
         
        
        if not os.path.exists(self.g_cfg_path):
            logging.critical('Could not locate global config: %s' % (self.g_cfg_path))
            return 


        # Docs for YAML: http://pyyaml.org/wiki/PyYAMLDocumentation
        # load the global config
        self.g_cfg = self.load_yaml(self.g_cfg_path)
      
        # Look for settings (item_data, args)
        self.settings = Helper.get_item(self.g_cfg, 'settings')[0]

        if not self.settings:
            print('Could not load settings')
            return 

        if 'log_path' not in self.settings:
            self.settings['log_path'] = '%s/log' % (self.base_dir)
            print('No log specified, using: %s' % (self.settings['log_path']))

                
        if 'db_path' not in self.settings:
            print('No database specified, quitting')

        logging.basicConfig(filename=self.settings['log_path'], level=logging.DEBUG)

        self.p_cfg = self.load_yaml(self.p_cfg_path)

    def load_yaml(self, path):
        with open(path) as cfg:
            return yaml.load(cfg.read())

    def get_plugin_cfg(self):
        return self.p_cfg

    def get_global_cfg(self):
        return self.g_cfg

    def get_settings(self):
        return self.settings

if __name__ == '__main__':
    core = Core()
    core.execute_config()

    while True:
        schedule.run_pending()
        time.sleep(1)



