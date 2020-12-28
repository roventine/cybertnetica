import paramiko

from util.logger import logger


class SSHClient:

    def __init__(self, host_config:dict):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host_config = host_config

    def ssh(self):
        self.client.connect(hostname=self.host_config['hostname'],
                            port=self.host_config['port'],
                            username=self.host_config['username'],
                            password=self.host_config['password'])
        logger.info('login to {0} -> {1}'.format(self.host_config, 'success'))
        return self

    def shell(self, cmd: str):
        logger.info('[{0}] : {1}'.format(self.host_config['hostname'], cmd))
        stdin, stdout, stderr = self.client.exec_command(cmd)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        logger.info('[{0}] : {1} -> {2}'.format(self.host_config['hostname'],
                                                cmd,
                                                result.decode()))
        return self

    def exit(self):
        self.client.close()


host_config ={
    'hostname':'122.112.155.31',
    'port':'9022',
    'username':'root',
    'password':'Knownofear!'
}
SSHClient(host_config).ssh().shell('docker info').exit()