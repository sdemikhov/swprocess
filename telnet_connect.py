from swprocess.dlink.dlink import Dlink
from swprocess.topaz.topaz import Topaz

device_types = {
    'dlink': Dlink,
    'topaz': Topaz
    }

def connect(*args, **kwargs):
    device_type = kwargs['device_type']
    if device_type not in device_types:
        raise TypeError('Unsupported device type')
    else:
        return device_types[device_type](*args, **kwargs)
