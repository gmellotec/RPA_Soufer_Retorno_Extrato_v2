from __init__ import config, log, path, bot
from datetime import datetime
from workflow import InitApplication
from workflow import ProcessApplication
from workflow import EndApplication
from utils.decorators import time_execution
from utils import SendMail
from utils import CloseApplication
from utils import Functions
import sys
import os


@time_execution
def main():
    
    status_process = False
    init_application = InitApplication()
    process_application = ProcessApplication()
    end_application = EndApplication()
    close_application = CloseApplication()
    mail = SendMail()
    
    try:
        # Setar o horario inicial do processo
        date_init = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        ## Limpar os diretórios padrões antes de iniciar o processo
        Functions.clear_dirs()

        log.info(f"INICIO DO PROCESSO: {os.getenv('JOB_BASE_NAME')}")
        log.info(f"AGENT EXECUTION: {os.getenv('NODE_NAME')}")
        log.info(f"ID EXECUTION: {os.getenv('BUILD_NUMBER')}")

        ## Enviar email inicial
        if config.getboolean('EMAIL', 'email_inicio'):
            log.info('Enviar email de inicio do processo')
            mail.send_init_mail(date_init)


        ## Inicializar as aplicações do Bot
        init_application.execute()

        ## Inicializar o processamento do Bot
        process_application.execute()
        
        ## Inicializar a finalização do processamento do Bot
        end_application.execute()

        log.info('FIM DO PROCESSO COM SUCESSO')
        status_process = True

    except Exception as erro:
        log.error(f'Ocorreu um erro durante a execucao do bot: {erro}')
        
        #Tirar print da tela
        Functions.get_screen_error()

        ## LISTAR O NOME DOS PROCESSOS QUE DEVEM SER FECHADOS
        list_process = ['']
        close_application.kill_all_application(list_process)

        log.info('FIM DO PROCESSO COM ERRO')

    finally:
        # SETAR O HORARIO FINAL DO PROCESSO
        date_end = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        if config.getboolean('EMAIL', 'email_fim'):
            # ENVIAR E-MAIL FINAL DO PROCESSO
            log.info('Enviando email ao final do processamento')
            mail.send_finish_mail(date_init, date_end, status_process)
            
        # Verificar o status do processo e sair com código de erro se necessário
        if not status_process:
            log.warning("O processo terminou com falha.")
            sys.exit(1)
            

if __name__ == '__main__':
    main()