from __init__ import log, path, config
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from utils import Functions


class SendMail:
    def __init__(self):
        self.smtp_server = config.get('EMAIL', 'smtp_server')
        self.smtp_port = config.get('EMAIL', 'smtp_port')
        self.from_email = config.get('EMAIL', 'remetente')
        self.var_nome_processo = os.getenv('JOB_BASE_NAME')
        self.var_nome_maquina = os.getenv('NODE_NAME')
        self.var_lista_destinatarios = config.get('EMAIL', 'destinatarios').replace(',', ';')
        
    def send_email(self, subject, body_message, to_email, attachments=[]):
        max_attempts = 3  # Número máximo de tentativas
        attempt = 0  # Contador de tentativas

        while attempt < max_attempts:
            try:
                # Incrementa a contagem de tentativas
                attempt += 1

                # Cria a mensagem
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(str(body_message), 'html'))

                # Anexa arquivos
                for file_path in attachments:
                    part = MIMEBase('application', "octet-stream")
                    with open(file_path, 'rb') as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    file_name = os.path.basename(file_path)  # Extrai apenas o nome do arquivo
                    part.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
                    msg.attach(part)

                # Conecta-se ao servidor SMTP e envia o e-mail
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                    server.ehlo()  # Identificar-se para o servidor
                    server.starttls()  # Iniciar TLS para comunicação segura
                    server.ehlo()

                    # Envia a mensagem
                    server.send_message(msg)

                log.info("E-mail enviado com sucesso!")
                break  # Sai do loop se o e-mail for enviado com sucesso

            except Exception as e:
                log.warning(f"Tentativa {attempt} falhou: {e}")

                # Verifica se ainda há tentativas restantes
                if attempt < max_attempts:
                    log.info("Tentando novamente em 5 segundos...")
                    time.sleep(5)  # Espera 5 segundos antes de tentar novamente
                else:
                    log.warning("Todas as tentativas de envio falharam.")

    def send_init_mail(self, date_init):
        try:
            
            if self.var_nome_processo is None:
                self.var_nome_processo = 'RPA_NOME_PROCESSO'
                
            if self.var_nome_maquina is None:
                self.var_nome_maquina = 'MAQUINA_RPA_X'
            
            # Ler o conteúdo do arquivo TXT de SUCESSO
            with open(path.email('template_email_inicial.txt'), 'r', encoding='utf-8') as file:
                body_message = file.read()

            body_message = body_message.replace('::NOME_PROJETO::', self.var_nome_processo)
            body_message = body_message.replace('::AGENT_NAME::', self.var_nome_maquina)
            body_message = body_message.replace('::DATA_HORA::', date_init)
            

            # Enviar e-mail
            self.send_email(f'Início de Execução - {self.var_nome_processo}', body_message, self.var_lista_destinatarios)
        except Exception as erro:
            log.info(f'Ocorreu um erro ao tentar enviar o e-mail: {erro}')

    def send_finish_mail(self, date_init: str, date_end: str, status_process: bool):
        try:
            # Atribuir variáveis para utilização dentro do código
            if self.var_nome_processo is None:
                self.var_nome_processo = 'RPA_NOME_PROCESSO'
                
            if self.var_nome_maquina is None:
                self.var_nome_maquina = 'MAQUINA_RPA_X'
            
            if status_process:
                # Ler o conteúdo do arquivo TXT de SUCESSO
                with open(path.email('template_email_sucesso.txt'), 'r', encoding='utf-8') as file:
                    body_message = file.read()
                    
                body_message = body_message.replace('::NOME_PROJETO::', self.var_nome_processo)
                body_message = body_message.replace('::AGENT_NAME::', self.var_nome_maquina)
                body_message = body_message.replace('::DATA_INIT::', date_init)
                body_message = body_message.replace('::DATA_END::', date_end)
            elif not status_process:
                # Ler o conteúdo do arquivo TXT de ERRO
                with open(path.email('template_email_erro.txt'), 'r', encoding='utf-8') as file:
                    body_message = file.read()
                    
                body_message = body_message.replace('::NOME_PROJETO::', self.var_nome_processo)
                body_message = body_message.replace('::AGENT_NAME::', self.var_nome_maquina)
                body_message = body_message.replace('::DATA_INIT::', date_init)
                body_message = body_message.replace('::DATA_END::', date_end)
                    
            # Listar arquivos para anexar
            attachments = [path.log('log.txt'), path.images('error.png')]
            if status_process:
                try:
                    # Capturar Relatório
                    path_relatorio = Functions.list_file_excel(path.output())
                
                    if len(path_relatorio) > 0:
                        attachments.append(path.output(path_relatorio[0]))
                    
                except:
                    pass

            # Enviar e-mail
            self.send_email(f'Resultado de Execução - {self.var_nome_processo}', body_message, self.var_lista_destinatarios, attachments)
        except Exception as erro:
            log.info(f'Ocorreu um erro ao tentar enviar o e-mail: {erro}')