import paramiko


class SSHClient():

    def __init__(self, host_config):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host_config = host_config

    def ssh(self):
        self.client.connect(hostname='192.168.158.131',
                         port=22,
                         username='root',
                         password='hadoop')
        return self

    def cmd(self, cmd: str):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        print(result.decode())
        return self

    def bye(self):
        self.client.close()
