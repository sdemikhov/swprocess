from swprocess.base_connection import BaseConnection

class Dlink(BaseConnection):
    def __init__(self, *args, **kwargs):
        self.login_user_pattern = b'UserName:'
        self.login_password_pattern = b'PassWord:'
        self.base_promt = b'#'
        self.enable_promt = b'#'
        self.enable_command = 'enable admin'
        self.enable_password_pattern = b'PassWord:'
        self.error_pattern = [
            'Fail!',
            'Next possible completions:',
            'Available commands:'
        ]
        
        super().__init__(*args, **kwargs)

    def _bulk(*args):
        '''Make telnetlib less smart =)))'''
        pass

    def make_session(self):
        super().make_session()
        self.session.set_option_negotiation_callback(self._bulk)

 
    def send_commands(self, *args, **kwargs):
        self._write_line('disable clipaging')
        self.session.read_until(self.enable_promt, timeout=self.timeout)
        
        output = super().send_commands(*args, **kwargs)
        
        self._write_line('enable clipaging')
        return output
        
    def send_config_commands(self, commands):
        raise ValueError('Not supported method for this device_type')
