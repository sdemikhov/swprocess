from concurrent.futures import ThreadPoolExecutor, as_completed

from swprocess import logger
from swprocess.telnet_connect import connect


def massive_send_commands(devices, commands, limit):
    return _massive_send(
        _generate_connections(devices),
        commands,
        'send_commands',
        limit
        )

   
def massive_send_config_commands(devices, commands, limit):
    connections = _generate_connections(devices)
    return _massive_send(
        _generate_connections(devices),
        commands,
        'send_config_commands',
        limit
        )

def _generate_connections(devices):
    for device in devices:
        yield connect(**device)


def _massive_send(connections, commands, commands_type, limit):
    data = []
    if isinstance(commands, str):
        commands = [commands]
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(_run_commands,
                                   connect,
                                   commands,
                                   commands_type)
                    for connect in connections]
        for f in as_completed(futures):
            data.append(f.result())
        return data

def _run_commands(connect, commands, commands_type):
    ip = connect.ip
    start_msg = '===> Connection: {}'
    logger.debug(start_msg.format(ip))
    result = getattr(connect, commands_type)(commands)
    connect.disconnect()
    received_msg = '<=== Received: {}'
    logger.debug(received_msg.format(ip))
    return (ip, result)
