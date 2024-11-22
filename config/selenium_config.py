from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxServices
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeServices
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os

class FirefoxSelenium:
    def __init__(self, path_download=None):
        
        # Definir o diretório padrão de download, se não for passado
        if path_download is None:
            path_download = os.path.join(os.getcwd(), 'downloads')
        
        # Criar a pasta de download, se não existir
        os.makedirs(path_download, exist_ok=True)
        
        # Configurações do Firefox
        self.options = FirefoxOptions()
        self.options.set_preference("browser.download.folderList", 2)  # Usar o diretório especificado
        self.options.set_preference("browser.download.dir", path_download)  # Diretório de download
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                                    "application/pdf,application/octet-stream,application/vnd.ms-excel")  
        # Definir tipos de arquivos a serem baixados automaticamente
        self.options.set_preference("pdfjs.disabled", True)  # Desativar visualização de PDF no navegador
        self.options.set_preference("browser.download.manager.showWhenStarting", False)  # Não mostrar a janela de download
        self.options.set_preference("browser.download.useDownloadDir", True)  # Usar o diretório de download
        self.options.set_preference("dom.block_download_insecure", False)  # Permitir downloads inseguros
        
        self.service = FirefoxServices(GeckoDriverManager().install())

    def init_driver(self):
        driver = webdriver.Firefox(service=self.service, options=self.options)
        driver.maximize_window()
        driver.set_page_load_timeout(60)
        return driver
    
class ChromeSelenium:
    def __init__(self, path_download=None):
        # Definir o diretório padrão de download, se não for passado
        if path_download is None:
            path_download = os.path.join(os.getcwd(), 'downloads')
        
        # Criar a pasta de download, se não existir
        os.makedirs(path_download, exist_ok=True)
        
        # Definir opções do Chrome
        self.chrome_options = ChromeOptions()
        # self.chrome_options.add_argument("--headless")  # Executar em segundo plano (opcional)
        self.chrome_options.add_argument("--no-sandbox")  # Melhor para ambientes Linux sem GUI
        self.chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memória compartilhada
        self.chrome_options.add_argument("--disable-gpu")  # Desativar GPU se não for necessária
        prefs = {
            "download.default_directory": path_download,  # Diretório de download
            "download.prompt_for_download": False,  # Não mostrar pop-up
            "directory_upgrade": True,  # Atualizar diretório se necessário
            "safebrowsing.enabled": True,  # Habilitar navegação segura
            "profile.default_content_settings.popups": 0,  # Bloquear pop-ups
            "profile.default_content_setting_values.automatic_downloads": 1,  # Permitir downloads automáticos
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1  # Permitir em qualquer site
        }
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.service = ChromeServices(ChromeDriverManager().install())
          
    def init_driver(self):
        driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        driver.maximize_window()
        driver.set_page_load_timeout(60)
        return driver