import easyocr
import numpy as np
import json

reader = easyocr.Reader(['en'])

#results = reader.readtext('bill2.jpg')


def readimage(path :str):
    return  reader.readtext(path)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)