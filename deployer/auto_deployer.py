from enum import Enum
import yaml
import json


import controller.remote_controller as rc


class DeployType(Enum):
    DOCKER = 1
    JAR = 2


class DeployConfig:

    def __init__(self, config):
        self.host_config_list = config['host_config_list']
        self.task_list = config['task_list']

    def to_string(self):
        return json.dump(self)

    def to_yaml(self):
        yaml_path = self.project_name
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_string())

    @staticmethod
    def of_yaml(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
            return DeployConfig(config)


class SimpleDeployer():

    def __init__(self, deploy_config: DeployConfig):
        self.host_config_list = deploy_config.host_config_list
        self.task_list = deploy_config.task_list

    def deploy_width_first(self):
        group_controller = rc.GroupController(self.host_config_list)
        for task in self.task_list:
            group_controller.set_task(task).execute_in_sequence()

    def deploy_depth_first(self):
        for host_config in self.host_config_list:
            for task in self.task_list:
                rc.RemoteController(host_config).execute(task)
