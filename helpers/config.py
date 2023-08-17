import yaml
from pathlib import Path


class Config:
    __instance = None

    @staticmethod
    def instance():
        """ Static access method. """
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """ Virtually private constructor. """

        if Config.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            root = Path(__file__).parent.parent
            self.data = yaml.load(open(str(root) + '/config.yml'), Loader=yaml.FullLoader)

            Config.__instance = self


if __name__ == '__main__':
    print('::::::::: Script will transition Jiras :::::::::')
    config = Config.instance()

