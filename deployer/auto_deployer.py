from enum import Enum
import yaml
import json

from util.sftp import SFTPClient
from util.ssh import SSHClient


class DeployType(Enum):
    DOCKER = 1
    JAR = 2


class DeployConfig:


    def __init__(self,config):
        self.host_config = config['host_config']


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
        self.host_config = deploy_config.host_config
        self.sftp_client = SFTPClient(host_config=self.host_config)
        self.ssh_client = SSHClient(host_config=self.host_config)

    def upload(self):
        self.upload()

    def deploy(self):
        self.sftp_client.sftp() \
            .cd('') \
            .lcd('') \
            .put() \
            .bye()

        self.ssh_client.ssh() \
            .shell() \
            .shell() \
            .exit()
        return self

    def validate(self):
        return self
