import win32com.client as win32
from __init__ import config, log, path
from utils import Functions

class SendMail:
    def __init__(self):
        self.config = config
        self.log = log
        self.path = path

    def send_init_mail(self, date_init):
        try:
            ## ATRIBUIR VARIAVEIS PARA UTILIZAÇÃO DENTRO DO CÓDIGO
            var_lista_destinatarios = self.config.get('EMAIL', 'destinatarios').replace(',',';')
            var_nome_processo = self.config.get('INFO', 'project_name')

            # Ler o conteúdo do arquivo TXT de SUCESSO
            with open(self.path.templates('template_email_inicial.txt'), 'r', encoding='utf-8') as file:
                body_message = file.read()
            
            body_message = body_message.replace('::NOME_PROJETO::', var_nome_processo).replace('::DATA_HORA::', date_init)

            # Cria uma instância do Outlook
            outlook = win32.Dispatch('outlook.application')
            
            # Cria um novo e-mail
            mail = outlook.CreateItem(0)
            
            # Define os atributos do e-mail
            mail.Subject = f'Início de Execução - {var_nome_processo}'
            mail.HTMLBody = body_message
            mail.To = var_lista_destinatarios
            
            # Envia o e-mail
            mail.Send()
            
            self.log.info("E-mail Inicial enviado com sucesso!")
        except Exception as erro:
            self.log.info(f'Ocorreu um erro ao tentar enviar o e-mail: {erro}')

    def send_finish_mail(self, date_init, date_end, status_process):
        try:
            ## ATRIBUIR VARIAVEIS PARA UTILIZAÇÃO DENTRO DO CÓDIGO
            var_lista_destinatarios = self.config.get('EMAIL', 'destinatarios').replace(',',';')
            var_nome_processo = self.config.get('INFO', 'project_name')

            var_status_processo = status_process

            if var_status_processo == 'SUCESSO':

                # Ler o conteúdo do arquivo TXT de SUCESSO
                with open(self.path.templates('template_email_sucesso.txt'), 'r', encoding='utf-8') as file:
                    body_message = file.read()
                
                body_message = body_message.replace('::NOME_PROJETO::', var_nome_processo).replace('::DATA_INIT::', date_init).replace('::DATA_END::', date_end)
            
            elif var_status_processo == 'ERRO':
                # Ler o conteúdo do arquivo TXT de ERRO
                with open(self.path.templates('template_email_erro.txt'), 'r', encoding='utf-8') as file:
                    body_message = file.read()
                
                body_message = body_message.replace('::NOME_PROJETO::', var_nome_processo).replace('::DATA_INIT::', date_init).replace('::DATA_END::', date_end)
            
            
            # Cria uma instância do Outlook
            outlook = win32.Dispatch('outlook.application')
            
            # Cria um novo e-mail
            mail = outlook.CreateItem(0)
            
            # Define os atributos do e-mail
            mail.Subject = f'Resultado de Execução - {var_nome_processo}'
            mail.HTMLBody = body_message
            mail.To = var_lista_destinatarios

            if var_status_processo == 'SUCESSO':
                try:
                    ## Capturar Relatório
                    path_relatorio = Functions.list_file_excel(self.path.output())
                    
                    # Listar Arquivos para Anexar
                    attachs = [self.path.output(path_relatorio[0]), self.path.log('log.txt')]
                    
                    # ANEXAR UM ARQUIVO
                    for att in attachs:
                        mail.Attachments.Add(att)
                except:
                    mail.Attachments.Add(self.path.log('log.txt'))

            else:
                mail.Attachments.Add(self.path.log('log.txt'))
            
            # Envia o e-mail
            mail.Send()
            
            self.log.info("E-mail final enviado com sucesso!")
        except Exception as erro:
            self.log.info(f'Ocorreu um erro ao tentar enviar o e-mail: {erro}')
