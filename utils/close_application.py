from botcity.core import DesktopBot
from __init__ import log

class CloseApplication:
    def __init__(self):
        self.bot = DesktopBot()


    def close_application(self, process_name:str):
        process = self.bot.find_process(process_name)
        if process is not None:
            log.info(f'Finalizando aplicação: {process_name}')
            self.bot.terminate_process(process)
        else:
            log.warning(f'Não foi encontrado o processo: {process_name}')


    def kill_all_application(self, list_process:list):
        ## LISTAR AQUI OS APLICATIVOS E PROCESSOS QUE O BOT UTILIZA PARA QUE SEJAM FECHADOS CASO OCORRA UM ERRO
        processes_to_close = list_process

        for process_name in processes_to_close:
            log.robot(f'Fechar {process_name}')
            process = self.bot.find_process(process_name)
            if process is not None:
                self.bot.terminate_process(process)
                log.robot(f'{process_name} fechado com sucesso.')
            else:
                log.robot(f'{process_name} não encontrado ou já está fechado.')