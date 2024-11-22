from __init__ import log, path, config

class ProcessApplication:
    def __init__(self):
        pass

    def execute(self):
        try:
            log.info('INICIO DA EXECUÇÃO DO WORKFLOW PROCESS APPLICATION')

            

            log.info('FIM DA EXECUÇÃO DO WORKFLOW PROCESS APPLICATION')
        except Exception as erro:
            log.error(f'Ocorreu um erro durante a execução do PROCESS APPLICATION: {erro}')
            raise
