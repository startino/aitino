import json
from types import SimpleNamespace
from enum import Enum


class FrameType(Enum):
    MESG = 'MESG'
    SYEV = 'SYEV'
    DELM = 'DELM'
    TPEN = 'TPEN'
    TPST = 'TPST'
    READ = 'READ'
    USEV = 'USEV'
    MACK = 'MACK'
    BRDM = 'BRDM'
    LOGI = 'LOGI'
    EROR = 'EROR'
    MEDI = 'MEDI'
    MRCT = 'MRCT'


class FrameModel(SimpleNamespace):
    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "({})".format(", ".join(items))


def convert_to_framemodel(d):
    return json.loads(d, object_hook=lambda d: FrameModel(**d))


def get_frame_data(data):
    data_r = data[4:]
    data_j = convert_to_framemodel(data_r)
    type_f = FrameType[data[:4]]

    if type_f == FrameType.MESG:
        data_j.data = convert_to_framemodel(data_j.data)

    data_j.type_f = type_f

    return data_j
