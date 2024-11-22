import os
from __init__ import config, log, path, bot
from datetime import datetime, timedelta

class Functions:
    
    @staticmethod
    def clear_dirs():
        ## Limpar os diretórios padrões antes de iniciar o processo
        path.clear_dirs(path.log())
        path.clear_dirs(path.input())
        path.clear_dirs(path.output())
        path.clear_dirs(path.downloads())
        path.clear_dirs(path.images())
        
    @staticmethod
    def data_formatada(format: str='%Y%m%d', time_delta=0):
        data_hoje = datetime.today()

        if time_delta > 0:
            data_retroativa = data_hoje - timedelta(days=time_delta)
            data_retroativa = data_retroativa.strftime(format)   

            return data_retroativa
        else:
            data_hoje = data_hoje.strftime(format)
        
            return data_hoje
        

    @staticmethod
    def check_file_exist(path_file):
        """
        Verifica se um arquivo existe em um caminho específico. Deverá passar o caminho
        juntamente com o nome do arquivo.

        :param path_file: Caminho completo do arquivo a ser verificado.
        :return: True se o arquivo existir, False caso contrário.
        """
        # Verifica se o arquivo existe
        if os.path.isfile(path_file):
            return True
        else:
            return False

    @staticmethod
    def count_files(path_dir):
        try:
            # Lista todos os itens no diretório
            itens = os.listdir(path_dir)
            
            # Filtra apenas os arquivos
            files = [item for item in itens if os.path.isfile(os.path.join(path_dir, item))]
            
            # Conta os arquivos
            qnt_files = len(files)
            
            return qnt_files
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return 0

    @staticmethod
    def list_file_excel(path_dir):
        """
        A função `list_file_excel` recebe um caminho de diretório como argumento e retorna uma lista de arquivos Excel presentes nesse diretório. 

        Parâmetros:
        - `path_dir` (str): O caminho do diretório que será verificado.

        Comportamento:
        1. Verifica se o caminho fornecido corresponde a um diretório válido. Caso contrário, levanta uma exceção `NotADirectoryError`.
        2. Lista todos os arquivos no diretório especificado que possuem as extensões '.xlsx' ou '.xls'.
        3. Retorna uma lista contendo os nomes dos arquivos Excel encontrados."""

        if not os.path.isdir(path_dir):
            raise NotADirectoryError(f"A pasta {path_dir} não foi encontrada.")
        
        files_excel = [f for f in os.listdir(path_dir) if f.endswith(('.xlsx', '.xls'))]
        
        return files_excel

    @staticmethod
    def get_screen_error():
        bot.get_screenshot(filepath=path.images('error.png'))

