import time

from swprocess.base_connection import BaseConnection

class Huawei(BaseConnection):
    def __init__(self, *args, **kwargs):
        self.login_user_pattern = b'Username'
        self.login_password_pattern = b'Password'
        self.base_promt = b'>'
        self.enable_promt = b']'
        self.enable_command = 'system-view'
        self.enable_password_pattern = b''
        self.config_command = ''
        self.error_pattern = [
            'Error:'
        ]
        self.exit_command = 'quit'
        
        super().__init__(*args, **kwargs)

    def send_config_commands(self, *args, **kwargs):
        raise ValueError('Not supported method for this device_type')
