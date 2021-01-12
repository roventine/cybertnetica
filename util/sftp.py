import os

import paramiko
import pywildcard
# from util.logger import logger


class SFTPClient:

    def __init__(self, host_config):
        self.host_config = host_config
        self.transport = paramiko.Transport((host_config['hostname'], host_config['port']))
        self.local_path = ''
        self.remote_path = ''
        self.client = None

    def sftp(self):
        self.transport.connect(username=self.host_config['username'],
                               password=self.host_config['password'])
        # logger.info('sftp to [{1}]'.format(self.host_config['hostname']))
        self.client = paramiko.SFTPClient.from_transport(self.transport)
        return self

    def cd(self, path: str):
        self.remote_path = path
        self.client.chdir(self.remote_path)
        return self

    def lcd(self, path: str):
        self.local_path = path
        return self

    def put(self, file):
        # logger.info('put [{0}].[{1}] to [{2}]'.format(self.local_path,file,self.remote_path))
        if self.local_path:
            local_file = '{0}/{1}'.format(self.local_path, file)
        self.client.put(local_file, file)
        return self

    def get(self, file):
        # logger.info('get [{0}].[{1}] to [{2}]'.format(self.remote_path,file,self.local_path))
        if self.local_path:
            local_file = '{0}/{1}'.format(self.local_path, file)
        self.client.get(file, local_file)
        return self

    def mput(self, pattern):
        files = os.listdir(self.local_path)
        matched_files = pywildcard.filter(files, pattern)
        for file in matched_files:
            self.put(file)
        return self

    def mget(self, pattern):
        files = self.client.listdir(self.client.getcwd())
        matched_files = pywildcard.filter(files, pattern)
        for file in matched_files:
            self.get(file)
        return self

    def bye(self):
        # logger.info('bye to [{1}]'.format(self.host_config['hostname']))
        self.transport.close()


