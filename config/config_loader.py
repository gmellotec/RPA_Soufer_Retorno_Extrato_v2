import os
from configparser import ConfigParser

class ConfigLoader(ConfigParser):

    def __init__(self, config_filename='config.ini'):
        super().__init__(interpolation=None)
        # Constrói o caminho completo para o arquivo de configuração
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config', config_filename)
        # Lê o arquivo de configuração com a codificação UTF-8
        self.read(config_file, encoding='utf-8')