from ConfigParser import ConfigParser

def is_int_helper(num):
    try:
        int(num)
        return True
    except:
        return False

def is_float_helper(num):
    try:
        float(num)
        return True
    except:
        return False

def get_proper_type(val):
    if val in ["False", "false"]:
        return False
    elif val in ["True", "true"]:
        return True
    elif is_int_helper(val):
        return int(val)
    elif is_float_helper(val):
        return float(val)
    elif len(val) > 0 and val[0] == '"': # It must be a string
        # Remove " " around it.
        if val[-1] == '"':
            return val[1:-1]
        else:
            return val[1:]
    else:
        return val

class Config(object):
    def __init__(self):
        self.section_name = "config"
        self.config_handler = ConfigParser()

    def init(self, filename):
        if len(self.config_handler.sections()) == 0:
            self.config_handler.read(filename)

            # Load all values from the config file over as attributes of the object.
            for (key, val_raw) in self.config_handler.items(self.section_name):
                val = get_proper_type(val_raw)
                setattr(self, key, val)



config = Config()
