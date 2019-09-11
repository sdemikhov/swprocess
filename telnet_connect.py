from swprocess.dlink.dlink import Dlink
from swprocess.topaz.topaz import Topaz
from swprocess.maipu.maipu import Maipu
from swprocess.qtech.qtech import Qtech


device_types = {
    'dlink': Dlink,
    'topaz': Topaz,
    'maipu': Maipu,
    'qtech_2910': Maipu,
    'qtech_3470': Qtech,
    }

def connect(*args, **kwargs):
    device_type = kwargs['device_type']
    if device_type not in device_types:
        raise TypeError('Unsupported device type')
    else:
        return device_types[device_type](*args, **kwargs)
