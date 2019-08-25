import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                              ' - %(message)s',
                              datefmt='%H:%M:%S')    

#stdout
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)

#file
logfile = logging.FileHandler(''.join([__name__, '_log.log']), 'w')
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(formatter)
logger.addHandler(logfile)                        

from swprocess.telnet_connect import connect
from swprocess.concurrent_run import massive_send_commands, massive_send_config_commands
