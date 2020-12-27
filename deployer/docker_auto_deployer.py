from util.sftp import SFTPClient
from util.ssh import SSHClient
from util.logger import logger


class DockerAutoDeployer():

    def __init__(self,host_config:dict):
        self.host_config = host_config

    def deploy(self):
        sftp_client = SFTPClient(host_config=self.host_config)
        sftp_client.sftp()\
            .cd('')\
            .lcd('')\
            .put()\
            .bye()

        ssh_client = SSHClient(host_config=self.host_config)
        ssh_client.ssh()\
            .cmd()\
            .cmd()\
            .bye()
        return self

    def validate(self):
        return self




