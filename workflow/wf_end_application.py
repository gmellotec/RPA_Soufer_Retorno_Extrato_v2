from __init__ import log, path, config

class EndApplication:
    def __init__(self):
        pass

    def execute(self):
        try:
            log.info('INICIO DA EXECUCAO DO WORKFLOW END APPLICATION')



            log.info('FIM DA EXECUCAO DO WORKFLOW END APPLICATION')
        except Exception as erro:
            log.error(f'Ocorreu um erro durante a execução do END APPLICATION: {erro}')
            raise
