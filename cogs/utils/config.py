import json


def write_config_value(section, key, value):
    with open('settings/' + section + '.json', 'r+') as fp:
        option = json.load(fp)
        option[key] = value
        fp.seek(0)
        fp.truncate()
        json.dump(option, fp, indent=4)


def get_config_value(section, key, fallback=''):
    with open('settings/' + section + '.json', 'r') as f:
        try:
            value = json.load(f)[key]
        except KeyError:
            # Value doesn't exist
            value = fallback
            write_config_value(section, key, fallback)
        return value
