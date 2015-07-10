import logging
import os
import sys
import imp
import copy


import yaml
import schedule
import time

#from sql.db_connect import Connect
import dataset
import stuf


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
        self.global_cfg    = cfg_manager.get_global_cfg()
        self.agent_cfg     = cfg_manager.get_agent_cfg()
        self.observer_cfg  = cfg_manager.get_observer_cfg()
        self.settings      = cfg_manager.get_settings()


        self.email_settings = Helper.get_item(self.global_cfg, 'email')
   
        self.loaded_agents    = {}
        self.loaded_observers = {}
       
        self.db = dataset.connect(self.settings['db_path'])
        #self.db = Connect(self.settings['db_path'])
    
        if self.db:
            logging.info('connected to database')

        else:
            logging.info('could not connect to database')
            return 


    def load_agent(self, name):

        if name in self.loaded_agents:
            return self.loaded_agents[name]

        agents = False

        for file_ in os.listdir(self.settings['agent_dir']):
            full_path   = '%s/%s' % (self.settings['agent_dir'], file_)
            agent_name = self.agent_basename(full_path)

            extension   = file_.split('.')[-1]
           
            if agent_name != name:
                continue

            if extension == 'py':
                agent = imp.load_source(agent_name, full_path)
                logging.info('loaded agent: %s' % (agent_name))

                # Save the agent
                self.loaded_agents[agent_name] = agent

                return agent

        return False 

    def load_observer(self, name):
        if name in self.loaded_observers:
            return self.loaded_observers[name]

        observers = False

        for file_ in os.listdir(self.settings['observer_dir']):
            full_path = '%s/%s' % (self.settings['observer_dir'], file_)
            observer_name = self.agent_basename(full_path)

            extension = file_.split('.')[-1]
            
            # If its not what we are looking for, continue
            if observer_name != name:
                continue

            if extension == 'py':
                observer = imp.load_source(observer_name, full_path)
                logging.info('loaded observer: %s' % (observer_name))

                # Save the observer
                self.loaded_observers[observer_name] = observer

                return observer


    def schedule_agents(self):

        for agent_name,args in Helper.yield_items(self.agent_cfg):
            logging.debug('scheduling agent: %s, args: %s' % (agent_name, args))
            if 'interval' not in args:
                logging.critical('interval not set for agent: %s' % (agent_name))
                return False

            # Modify the arguments so the execute function gets what it needs. 
            copy_args = copy.copy(args) 
            del copy_args['interval']

            copy_args['agent']    = self.load_agent
            copy_args['db']         = self.db
            #copy_args['email_settings'] = self.email_settings[0]

            # See if agent is already loaded
            if agent_name not in self.loaded_agents:
                self.load_agent(agent_name)

            #https://github.com/dbader/schedule/blob/master/FAQ.rst
            schedule.every(args['interval']).minutes.do(self.loaded_agents[agent_name].execute, **copy_args)

   
    def schedule_observers(self):
        for observer_name,args in Helper.yield_items(self.observer_cfg):
            logging.debug('scheduling observer: %s, args: %s' % (observer_name, args))

            if 'interval' not in args:
                logging.critical('interval not set for observer: %s' % (observer_name))
                return False

            copy_args = copy.copy(args)
            del copy_args['interval']

            #copy_args['observer'] = self.load_observer
            copy_args['db'] = self.db
            copy_args['email_settings'] = self.email_settings[0]

            # See if the observer is already loaded
            if observer_name not in self.loaded_observers:
                self.load_observer(observer_name)

            schedule.every(args['interval']).minutes.do(self.loaded_observers[observer_name].execute, **copy_args)

    def agent_basename(self, path):
        return os.path.basename(path).split('.py')[0].strip()


    def remove_agent(self, path):
        del self.index[path]


class ConfigManager():
    def __init__(self, global_cfg_path=None, agent_cfg_path=None, observer_cfg_path=None):
        self.base_dir = os.getcwd()

        # I do this so I can use self.base_dir, otherwise I would use def __init__(self, global_cfg_path='%s/configs/global.yml' % (self.base_dir))
        if not global_cfg_path:
            self.global_cfg_path = '%s/configs/global.yml'  % (self.base_dir)
        
        if not agent_cfg_path:
            self.agent_cfg_path = '%s/configs/agent_config.yml' % (self.base_dir)

        if not observer_cfg_path:
            self.observer_cfg_path = '%s/configs/observer_config.yml' % (self.base_dir)

        self.agent_cfg      = {}
        self.observer_cfg   = {}
        self.global_cfg     = {}
        self.settings       = {}
        self.email_settings = {}
         
        
        if not os.path.exists(self.global_cfg_path):
            logging.critical('Could not locate global config: %s' % (self.global_cfg_path))
            return 


        # Docs for YAML: http://pyyaml.org/wiki/PyYAMLDocumentation
        # load the global config
        self.global_cfg = self.load_yaml(self.global_cfg_path)
      
        # Look for settings (item_data, args)
        self.settings = Helper.get_item(self.global_cfg, 'settings')[0]
        self.email_settings = Helper.get_item(self.global_cfg, 'email')[0]

        if not self.settings:
            print('Could not load settings')
            return 

        if not self.email_settings:
            print('Could not load email settings') 

        if 'log_path' not in self.settings:
            self.settings['log_path'] = '%s/log' % (self.base_dir)
            print('No log specified, using: %s' % (self.settings['log_path']))

                
        if 'db_path' not in self.settings:
            print('No database specified, quitting')

        logging.basicConfig(filename=self.settings['log_path'], level=logging.DEBUG)

        self.agent_cfg    = self.load_yaml(self.agent_cfg_path)
        self.observer_cfg = self.load_yaml(self.observer_cfg_path)

    def load_yaml(self, path):
        with open(path) as cfg:
            return yaml.load(cfg.read())

    def get_agent_cfg(self):
        return self.agent_cfg

    def get_observer_cfg(self):
        return self.observer_cfg

    def get_global_cfg(self):
        return self.global_cfg

    def get_settings(self):
        return self.settings

if __name__ == '__main__':
    core = Core()
    core.schedule_agents()
    core.schedule_observers()

    while True:
        schedule.run_pending()
        time.sleep(1)



