import time


from swprocess.base_connection import BaseConnection

class Qtech(BaseConnection):
    def __init__(self, *args, **kwargs):
        self.login_user_pattern = b'login'
        self.login_password_pattern = b'Password'
        self.base_promt = b'#'
        self.enable_promt = b'#'
        self.enable_command = ''
        self.enable_password_pattern = b''
        self.config_command = 'config terminal'
        self.error_pattern = [
            '% '
        ]
        self.exit_command = 'exit'
        
        super().__init__(*args, **kwargs)

    def disconnect(self):
        self._write_line('end')
        time.sleep(1)
        self._write_line('exit')
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._write_line('end')
        time.sleep(1)
        self._write_line('exit')
