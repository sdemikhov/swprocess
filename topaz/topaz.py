from swprocess.base_connection import BaseConnection

class Topaz(BaseConnection):
    def __init__(self, *args, **kwargs):
        self.login_user_pattern = b'User Name:'
        self.login_password_pattern = b'Password:'
        self.base_promt = b'#'
        self.enable_promt = b'#'
        self.enable_command = ''
        self.enable_password_pattern = b''
        self.config_command = b'configure terminal'
        self.error_pattern = [
            '%'
        ]
        
        super().__init__(*args, **kwargs)

    def _enable_mode(self):
        pass
