from swprocess.base_connection import BaseConnection

class Dlink(BaseConnection):
    def __init__(self, *args, **kwargs):
        self.login_user_pattern = b'UserName'
        self.login_password_pattern = b'PassWord'
        self.base_promt = b'#'
        self.enable_promt = b'#'
        self.already_enable = ['admin#', '5#', '4#']
        self.enable_command = 'enable admin'
        self.enable_password_pattern = b'PassWord'
        self.error_pattern = [
            'Fail!',
            'Next possible completions',
            'Available commands:'
        ]
        
        self.exit_command = 'exit'
        super().__init__(*args, **kwargs)


    def disable_telnet_options(self):
        self.session.set_option_negotiation_callback(self._bulk)

    def _bulk(*args):
        '''Make telnetlib less smart =)))'''
        pass
 
    def send_commands(self, *args, **kwargs):
        self._write_line('disable clipaging')
        self.session.read_until(self.enable_promt, timeout=self.timeout)
        
        output = super().send_commands(*args, **kwargs)
        
        self._write_line('enable clipaging')
        return output
        
    def send_config_commands(self, commands):
        raise ValueError('Not supported method for this device_type')

    def _enable_mode(self):
        for promt in self.already_enable:
            if promt in self._auth:
                return
        super()._enable_mode()
