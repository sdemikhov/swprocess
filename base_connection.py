# -*- coding: utf-8 -*-

import telnetlib
import time
from functools import wraps

from swprocess import logger


class BaseConnection:
    def __init__(self,
                 ip,
                 username,
                 password,
                 secret,
                 device_type,
                 timeout=10):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.device_type = device_type
        self.timeout = timeout

        self.make_session()

    def make_session(self):        
        self.session = telnetlib.Telnet(self.ip, timeout=self.timeout)
        self.disable_telnet_options()
        
        self.session.read_until(self.login_user_pattern,
                                timeout=self.timeout)
        self._write_line(self.username)
        self.session.read_until(self.login_password_pattern,
                                timeout=self.timeout)
        self._write_line(self.password)
        
        self._auth = self.session.read_until(
            self.base_promt,
            timeout=self.timeout
            ).decode('utf-8')
        if self.login_user_pattern.decode('utf-8') in self._auth:
            raise ValueError(f'{self.ip}: Wrong username or password')
        self._enable_mode()

    def disable_telnet_options(self):
        pass

    def _enable_mode(self):
        self._write_line(self.enable_command)
        self.session.read_until(self.enable_password_pattern,
                                timeout=self.timeout)
        self._write_line(self.secret)
        time.sleep(1)
        authorised_enable = self.session.read_until(
            self.enable_promt, timeout=self.timeout
            ).decode('utf-8')
        if not self._check_output(authorised_enable):
            raise ValueError(f'{self.ip}: Wrong enable password')

    def _write_line(self, command):
        self.session.write(command.encode('ascii') + b'\n')
    

    def send_commands(self, commands):
        result = ''
        
        if isinstance(commands, str):
            commands = [commands]
            
        for command in commands:
            self._write_line(command)
            time.sleep(1)
            output = self.session.read_until(self.enable_promt,
                                          timeout=self.timeout).decode('utf-8')

            result += output
            
        result += self.session.read_until(self.enable_promt,
                                          timeout=self.timeout).decode('utf-8')
        return result


    def send_config_commands(self, commands):
        result = ''
        self._write_line(self.config_command)
        
        if isinstance(commands, str):
            commands = [commands]
            
        for command in commands:
            self._write_line(command)
            time.sleep(1)
            output = self.session.read_until(self.enable_promt,
                                          timeout=self.timeout).decode('utf-8')

            result += output
        
        self._write_line(self.exit_command)
        time.sleep(1)
        result += self.session.read_until(self.enable_promt,
                                          timeout=self.timeout).decode('utf-8')
        return result

    def _check_output(self, output):
        for error in self.error_pattern:
            if error in output:
                return False
        return True

    def disconnect(self):
        self.session.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
