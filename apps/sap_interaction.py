import os
import psutil
import win32com.client, subprocess, time
from __init__ import log, config, path


class SapLogon:
    def __init__(self):
        self.SAPGUI = None
        self.application = None
        self.connection = None
        self.session = None
        self.var_time = 0
        self.env = config.get('INFO', 'env')

    def get_session(self):
        """Retorna a sessão atual para uso direto."""
        if not self.session:
            raise Exception("A sessão SAP não foi inicializada. Certifique-se de conectar primeiro.")
        return self.session

    def start_sap(self):
        """Inicia o SAP Logon e valida se o processo está ativo."""
        log.info('Abrindo o SAP')
        path_sap = os.getenv('SAP_PATH_EXE')
        log.info(f'Valor da variável de ambiente SAP_PATH_EXE: {path_sap}')
        
        try:
            # Abrindo o SAP usando subprocess
            subprocess.Popen(path_sap)
            time.sleep(10)  # Espera 10 segundos para o SAP carregar
            
            # Verificação se o SAP foi realmente aberto
            if self.__is_sap_running():
                log.info("SAP foi iniciado com sucesso.")
            else:
                log.error("Falha ao iniciar o SAP. O processo não foi encontrado.")
                raise Exception("SAP não foi iniciado corretamente.")
        except Exception as e:
            log.error(f"Erro ao tentar abrir o SAP: {e}")
            raise

    def __is_sap_running(self):
        """Verifica se o processo SAP está rodando no sistema."""
        for proc in psutil.process_iter(['pid', 'name']):
            if "saplogon.exe" in proc.info['name'].lower():  # Verifica pelo nome do executável
                log.info(f"Processo SAP encontrado. PID: {proc.info['pid']}")
                return True
        return False

    def connect(self, env: str='prod'):
        """Realiza a conexão ao SAP."""
        try:
            self.SAPGUI = win32com.client.GetObject("SAPGUI")
            if not self.SAPGUI:
                log.error("Não foi possível obter o objeto SAPGUI.")
                return

            self.application = self.SAPGUI.GetScriptingEngine
            if not self.application:
                log.error("Não foi possível obter o Scripting Engine.")
                return

            var_envSAP = self.__get_env_sap(env)
            if not var_envSAP:
                log.error('Não foi possível encontrar o ambiente SAP.')
                raise Exception('Ambiente SAP não encontrado.')

            log.info(f"Conectando ao ambiente: {var_envSAP}")
            self.connection = self.application.OpenConnection(var_envSAP, True)
            time.sleep(5)
            self.session = self.connection.Children(0)
            self.session.findById("wnd[0]").maximize()
        except Exception as e:
            log.error(f"Erro ao conectar ao SAP: {e}")
            raise

    def __get_env_sap(self, env: str):
        """Retorna o ambiente SAP (DEV ou PROD) com base na configuração."""

        env = env.upper()
        if env == 'DEV':
            return os.getenv('SAP_ENV_DEV')
        elif env == 'PROD':
            return os.getenv('SAP_ENV_PROD')
        else:
            return None

    def login(self):
        """Realiza o login no SAP com as credenciais obtidas do ambiente."""
        try:
            log.info('Capturando credenciais SAP')
            var_user = os.getenv('SAP_LOGIN')
            var_pwd = os.getenv('SAP_PWD')

            log.info("Inserindo credenciais SAP")
            self.input_text("wnd[0]/usr/txtRSYST-BNAME", var_user)
            self.input_text("wnd[0]/usr/pwdRSYST-BCODE", var_pwd)

            log.info("Pressionando Enter para acessar o sistema")
            self.session.findById("wnd[0]").sendVKey(0)
        except Exception as e:
            log.error(f"Erro durante o login no SAP: {e}")
            raise
    
    def acess_transaction(self, transacao):
        """Acessa uma transação SAP."""
        try:
            log.robot(f"Acessando transação: {transacao}")
            self.session.StartTransaction(transacao)
        except Exception as e:
            log.error(f"Erro ao acessar a transação {transacao}: {e}")
            raise

    def __access_transaction(self, transaction_code):
        """Acessa uma transação SAP."""
        try:
            log.info(f"Acessando transação {transaction_code}")
            self.input_text("wnd[0]/tbar[0]/okcd", transaction_code)
            self.session.findById("wnd[0]").sendVKey(0)
        except Exception as e:
            log.error(f"Erro ao acessar a transação {transaction_code}: {e}")
            raise

    def input_text(self, element_id, value):
        """Abstrai a inserção de texto em um campo SAP, com tratamento de exceções."""
        try:
            element = self.session.findById(element_id)
            element.text = str(value)
            # log.info(f"Texto '{value}' inserido no campo {element_id}")
        except Exception as e:
            log.error(f"Erro ao inserir texto no elemento {element_id}: {e}")
            raise
        
    def click_element(self, element_id):
        """Clica em um elemento SAP identificado pelo element_id."""
        try:
            element = self.session.findById(element_id)
            element.press()
            # log.info(f"Botão {element_id} clicado com sucesso.")
        except Exception as e:
            log.error(f"Erro ao clicar no elemento {element_id}: {e}")
            raise
        
    def get_text(self, element_id):
        """Captura o texto de um campo identificado por element_id."""
        try:
            element = self.session.findById(element_id)
            text = element.text
            # log.info(f"Texto capturado do elemento {element_id}: {text}")
            return text
        except Exception as e:
            log.error(f"Erro ao capturar texto do elemento {element_id}: {e}")
            raise
        
    def select_combo_box(self, element_id, value):
        """Seleciona um item em um combo box (dropdown) identificado por element_id."""
        try:
            combo_box = self.session.findById(element_id)
            combo_box.Key = value
            # log.info(f"Item '{value}' selecionado no combo box {element_id}")
        except Exception as e:
            log.error(f"Erro ao selecionar item no combo box {element_id}: {e}")
            raise

    def select_radio_button(self, radio_id):
        """Seleciona um botão de rádio pelo ID."""
        try:
            radio = self.session.FindById(radio_id)
            radio.Select()
            # log.info(f"Botão de rádio {radio_id} selecionado com sucesso.")
        except Exception as e:
            log.error(f"Erro ao selecionar o rádio {radio_id}: {e}")
            raise

    def select_checkbox(self, checkbox_id, marcar=True):
        """Seleciona ou desmarca um checkbox pelo ID."""
        try:
            checkbox = self.session.FindById(checkbox_id)
            checkbox.Selected = marcar
            acao = "marcado" if marcar else "desmarcado"
            # log.info(f"Checkbox {checkbox_id} {acao} com sucesso.")
        except Exception as e:
            log.error(f"Erro ao modificar o estado do checkbox {checkbox_id}: {e}")
            raise
        
    def element_exists(self, element_id):
        """Verifica se um elemento existe na interface SAP."""
        try:
            self.session.findById(element_id)
            log.info(f"Elemento encontrado.")
            return True
        except Exception:
            log.info(f"Elemento não encontrado.")
            return False
        
    def send_vkey(self, element_id, key_value):
        """Envia uma tecla de função ou atalho (VKey) ao SAP."""
        try:
            element = self.session.findById(element_id)
            element.sendVKey(key_value)
            # log.info(f"Tecla VKey {key_value} enviada para o elemento {element_id}.")
        except Exception as e:
            log.error(f"Erro ao enviar a tecla VKey {key_value} para o elemento {element_id}: {e}")
            raise

    def press_button(self, element_id, button_name):
        """Pressiona um botão identificado pelo element_id e pelo nome do botão."""
        try:
            element = self.session.findById(element_id)
            element.pressButton(button_name)
            # log.info(f"Botão '{button_name}' pressionado no elemento {element_id}.")
        except Exception as e:
            log.error(f"Erro ao pressionar o botão '{button_name}' no elemento {element_id}: {e}")
            raise