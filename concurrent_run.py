from concurrent.futures import ThreadPoolExecutor, as_completed

from swprocess import logger
from swprocess.telnet_connect import connect


start_msg = '===> Connection: {}'
received_msg = '<=== Received: {}'

def massive_send_commands(devices, limit):
    return _massive_send(
        _generate_connections(devices),
        'send_commands',
        limit
        )

   
def massive_send_config_commands(devices, limit):
    return _massive_send(
        _generate_connections(devices),
        'send_config_commands',
        limit
        )


def _generate_connections(devices):
    for device, commands in devices:
        if isinstance(commands, str):
            commands = [commands]
        yield (connect(**device), commands)


def _massive_send(connections, commands_type, limit):
    data = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(_run_commands,
                                   connect,
                                   commands,
                                   commands_type)
                    for connect, commands in connections]
        for f in as_completed(futures):
            data.append(f.result())
        return data


def _run_commands(connect, commands, commands_type):
    ip = connect.ip
    logger.debug(start_msg.format(ip))
    result = getattr(connect, commands_type)(commands)
    connect.disconnect()
    logger.debug(received_msg.format(ip))
    return (ip, result)
