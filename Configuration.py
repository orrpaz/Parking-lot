import configparser


def readconfig():
    config = configparser.RawConfigParser()
    config.read('./config.properties')
    details_dict = dict(config.items('SECTION_NAME'))
    return details_dict
