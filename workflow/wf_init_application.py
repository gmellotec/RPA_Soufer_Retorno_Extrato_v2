from __init__ import log, config, path


class InitApplication:
    def __init__(self):
        pass

    def execute(self):
        try:
            log.info('INICIO DA EXECUCAO DO WORKFLOW INIT APPLICATION')
            
            
            log.info('FIM DA EXECUCAO DO WORKFLOW INIT APPLICATION')
        except Exception as erro:
            log.error(f'Ocorreu um erro durante a execução do INIT APPLICATION: {erro}')
            raise
