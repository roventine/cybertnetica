from enum import Enum

from util.sftp import SFTPClient
from util.ssh import SSHClient


class TaskType(Enum):
    SHELL = 0
    UPLOAD = 1
    DOWNLOAD = 2


class BaseTask:

    def __init__(self, t: str):
        self.type = TaskType[t]


class ShellTask(BaseTask):

    def __init__(self, d: dict):
        BaseTask.__init__(self, d['type'])
        self.shell = d['shell']


class SFTPTask(BaseTask):

    def __init__(self, d: dict):
        BaseTask.__init__(self, d['type'])
        self.remote_path = d['remote_path']
        self.local_path = d['local_path']
        self.pattern = d['pattern']


class HostConfig:

    def __init__(self, d: dict):
        self.hostname = d['hostname']
        self.port = d['port']
        self.username = d['username']
        self.password = d['password']


class SimpleController:

    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.task = None
        self.result = {'success': False, 'msg': ''}

    def set_host_config(self, host_config: HostConfig):
        self.ssh = SSHClient(host_config.__dict__)
        self.sftp = SFTPClient(host_config.__dict__)
        return self

    def set_task(self, task: BaseTask):
        self.task = task
        return self

    def execute(self):
        try:
            if self.task.type == TaskType.SHELL:
                self.ssh.ssh() \
                    .shell(self.task.shell) \
                    .exit()

            if self.task.type == TaskType.UPLOAD:
                self.sftp.sftp() \
                    .cd(self.task.remote_path) \
                    .lcd(self.task.local_path) \
                    .mput(self.task.pattern) \
                    .bye()

            if self.task.type == TaskType.DOWNLOAD:
                self.sftp.sftp() \
                    .cd(self.task.remote_path) \
                    .lcd(self.task.local_path) \
                    .mget(self.task.pattern) \
                    .bye()

            self.result['success'] = True

        except Exception as e:
            self.result['msg'] = str(e)

        return self.result

# class GroupController:
#
#     def __init__(self, host_config_list: list):
#         self.controllers = {}
#         self.hosts = {}
#         self.result = {}
#         self.task = None
#         for host_config in host_config_list:
#             self.controllers[host_config['hostname']] = RemoteController(host_config)
#             self.hosts[host_config['hostname']] = host_config
#
#     def set_task(self, task: BaseTask):
#         self.task = task
#         return self
#
#     def execute_in_sequence(self):
#         self.result.clear()
#         for name, controller in self.controllers.items():
#             self.result[name] = controller.execute(self.task)
#         return self
#
#     def execute_in_assigned_host(self, host_name: str):
#         self.result.clear()
#         self.result[host_name] = self.controllers[host_name].execute(self.task)
#         return self
#
#
# def execute(controller: RemoteController, task: BaseTask):
#     return controller.execute(task)
#
#
# def execute_in_concurrent(group_controller: GroupController):
#     with ThreadPoolExecutor(max_workers=8) as t:
#
#         future_list = []
#
#         for name, controller in group_controller.controllers.items():
#             args = [controller, group_controller.task]
#             future = t.submit(lambda p: execute(*p), args)
#             future_list.append(future)
#
#         for future in as_completed(future_list):
#             data = future.result()
#             logger.info(data)


