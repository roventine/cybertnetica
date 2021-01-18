import json
from typing import Union

import yaml

from controller.remote_controller import ShellTask, SFTPTask, HostConfig, SimpleController


class DeployConfig:

    task_list: list[Union[ShellTask, SFTPTask]]

    def __init__(self, config):
        self.host_config_list = []
        for host_config in config['host_config_list']:
            self.host_config_list.append(HostConfig(host_config))
        self.task_list = []
        for task in config['task_list']:
            if task['type'] == 'SHELL':
                self.task_list.append(ShellTask(task))
            if task['type'] == 'UPLOAD' or task['type'] == 'DOWNLOAD':
                self.task_list.append(SFTPTask(task))

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


class SimpleDeployer:

    def __init__(self, deploy_config: DeployConfig):
        self.host_config_list = deploy_config.host_config_list
        self.task_list = deploy_config.task_list
        self.result_list = []

    def deploy_width_first(self):
        for task in self.task_list:
            for host_config in self.host_config_list:
                r = SimpleController().set_host_config(host_config) \
                    .set_task(task) \
                    .execute()
                self.result_list.append(r)
        return self

    def deploy_depth_first(self):
        for host_config in self.host_config_list:
            for task in self.task_list:
                r = SimpleController().set_host_config(host_config) \
                    .set_task(task) \
                    .execute()
                self.result_list.append(r)
        return self


# if __name__ == '__main__':
#     config = DeployConfig.of_yaml('sicarius.yaml')
#     print(len(config.task_list))
#     deployer = SimpleDeployer(config)
#     result = deployer.deploy_width_first().result_list
#     print(result)
