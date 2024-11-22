# RPA Template Default
Este repositório contém um template padrão para a configuração de um projeto de Automação Robótica de Processos (RPA), oferecendo uma estrutura organizada para a automação de tarefas. Abaixo, detalhamos cada parte do código:

# Estrutura
## /apps
Contém scripts principais que interagem com os softwares durante o processo de automação, como abrir aplicações, clicar em botões e inserir dados.

#### sap_interaction.py - Módulo de Interação com SAP
Este módulo é responsável pela automação de tarefas no sistema SAP através da interface de script. Ele gerencia o login, a execução de transações e o logoff no SAP, utilizando a biblioteca win32com.client para interagir com a GUI do SAP.

#### Funções do Módulo
**sap_login**: Realiza o login no SAP, abrindo o programa via subprocesso e inserindo credenciais de acesso obtidas através do objeto maestro.

**sap_acessar_transacao**: Acessa uma transação específica no SAP através do código de transação fornecido, utilizando métodos para manipular elementos da GUI.

**sap_logof**: Executa o logoff do SAP, navegando pelos menus da aplicação para encerrar a sessão de forma segura.

#### Dependências
**win32com.client**: Usada para criar e manipular objetos COM, essencial para a interação com aplicações Windows como o SAP.
subprocess e time: Utilizados para abrir aplicações e gerenciar tempos de espera, respectivamente.

**Classes e Módulos Adicionais**: DesktopBot, ConfigLoader, Log, Paths, e Functions são importados para suportar a automação, desde carregar configurações até logar atividades e manipular caminhos de arquivos.
Este script é uma parte crucial do framework de automação, permitindo interações detalhadas e controladas com o sistema SAP, essenciais para operações automatizadas em ambientes corporativos.

## /config
Inclui arquivos de configuração que gerenciam ajustes e parâmetros fora da lógica de aplicação principal, facilitando modificações sem alterar o código central.

#### config.ini
Arquivo de configuração padrão para projetos RPA. Ele armazena parâmetros que podem ser facilmente alterados sem modificar o código, como caminhos de arquivos, credenciais e configurações específicas de ambiente.

#### config_loader.py
Script responsável por carregar as configurações a partir do config.ini. Utiliza o módulo ConfigParser para ler e disponibilizar essas configurações dentro do código Python, garantindo uma maneira centralizada e eficiente de gerenciar as configurações do projeto​​.

#### log2.py
Define uma classe Log para gerenciar o registro de logs do projeto. Ela garante que as mensagens de log sejam escritas de forma thread-safe em um arquivo, com suporte a diferentes níveis de mensagens, como informações, avisos e erros. Esta classe é essencial para o monitoramento e debugging de aplicações em produção​​.

#### maestro_settings.py
Integra as funcionalidades do Botcity Maestro, permitindo autenticação e comunicação com este servidor de automação. Gerencia o status das tarefas executadas, como sucesso ou falha, e envia artefatos de log para o Maestro, facilitando a supervisão e controle de execuções de bots​​.

#### paths2.py
Centraliza a gestão de caminhos de diretórios e arquivos utilizados no projeto. Esta classe ajuda a organizar e referenciar todos os caminhos necessários no código, evitando hardcoding e facilitando mudanças nos diretórios de arquivos​​.

#### rpa_analytics.py
Utiliza pandas para manipular e analisar dados relacionados à execução de automações RPA. Permite adicionar, atualizar e salvar dados sobre as execuções em um arquivo Excel, oferecendo uma ferramenta valiosa para análise de desempenho e resultados das automações​​.

Cada um desses arquivos desempenha um papel específico na configuração, execução e análise de projetos de RPA, garantindo que o sistema seja robusto, configurável e fácil de monitorar.

## /data
Armazena arquivos de dados utilizados ou gerados pelos processos de automação, como planilhas de entrada ou registros de saída interagindo com os diretórios /input e /output.

## /doc
Documentação do projeto, incluindo instruções de configuração, guias de uso e outras informações relevantes para ajudar usuários e desenvolvedores a entender o projeto.

## /doc/templates
Utilizado para armazenas os templates padrões que irão ser utilizados pela automação que será desenvolvida. Como padrão sempre irá conter os arquivos abaixo:

#### template_email_inicial.txt - Template de Email Inicial
Este template HTML é usado para notificar o início de um processo RPA. Ele é estilizado para ser visualmente claro e inclui placeholders para o **nome do projeto** e a **data e hora de início**, permitindo personalização conforme o processo específico​​.

#### template_email_sucesso.txt - Template de Email de Sucesso
Utilizado para notificar o término bem-sucedido de um processo RPA, este template HTML também segue um design claro e inclui espaços para inserir o **nome do projeto**, além das **datas de início e término do processo**, proporcionando um resumo efetivo e profissional do resultado​​.

#### template_email_erro.txt - Template de Email de Erro
Este template é usado para alertar sobre uma falha no processo RPA. Ele se diferencia pelo cabeçalho em cor laranja e proporciona detalhes sobre o **nome do projeto**, as **datas de início e término**, e um alerta para ação do suporte técnico, destacando a necessidade de intervenção​​.

Esses templates são essenciais para a comunicação automatizada com stakeholders do processo, garantindo que todos os envolvidos estejam atualizados sobre o status dos robôs de automação.

## /log
Contém arquivos de registro que documentam a execução dos scripts de automação, essenciais para debugging e monitoramento do sistema.

## /tests
Contém os arquivos utilizados para realização de testes ao decorrer do processo de desenvolvimento do projeto.

## /utils
Armazena utilitários e scripts auxiliares que fornecem funcionalidades comuns e reutilizáveis em várias partes do projeto. Ela inclui scripts para manipulação de arquivos, envio de e-mails, medição de tempo de execução de funções, entre outras funcionalidades. Esta organização ajuda a manter o código limpo e modular, facilitando a manutenção e a escalabilidade do projeto ao centralizar métodos úteis que podem ser chamados conforme necessário por diferentes componentes do sistema.

#### decorators.py
Contém definições de decoradores que são utilizados para adicionar funcionalidades extras a funções existentes no projeto sem modificar seu código diretamente. Estes decoradores podem incluir funcionalidades como medição de tempo de execução, registro de atividades, validações de entrada e saída, entre outros. Este script é projetado para ser expansível, permitindo a inclusão de novos decoradores conforme necessário, melhorando a modularidade e reusabilidade do código.​

#### functions.py
Serve como uma biblioteca central para funções utilitárias que apoiam diversas operações no projeto. Este arquivo é projetado para incluir funções reutilizáveis que lidam com operações comuns de dados e arquivos, facilitando a manutenção e melhorando a eficiência do código. O conteúdo deste script pode ser expandido para incluir novas funções conforme necessário, garantindo que o código permaneça modular e fácil de atualizar.

#### send_mail_win32.py
Este script define a classe SendMail, que utiliza a biblioteca win32com.client para enviar e-mails através do Outlook. Possui métodos para enviar e-mails no início e no término de processos, com a capacidade de anexar arquivos e modificar o conteúdo do e-mail com base no status do processo. Este arquivo é essencial para a comunicação automatizada sobre o progresso dos processos RPA​​.

## /workflow
 É dedicado a armazenar scripts que controlam o fluxo de processos de automação de ponta a ponta. Ele inclui scripts para inicializar aplicações, processar tarefas específicas, finalizar processos e fechar aplicações adequadamente. Este diretório é fundamental para organizar e gerenciar as várias etapas envolvidas em um processo automatizado, garantindo que cada parte do fluxo de trabalho seja executada corretamente e que os recursos sejam liberados após a conclusão.

#### wf_init_application.py
Este script gerencia a inicialização de aplicações necessárias para o processo de automação. Ele inclui funções para abrir aplicações, sites, planilhas, etc., registrando o início e o fim dessa fase e tratando exceções que podem ocorrer durante o processo​​.

#### wf_process_application.py
Responsável pela execução do processo de automação principal, este arquivo contém o código que lida com o fluxo de trabalho específico da aplicação. Ele registra informações sobre o início e o término do processo e é projetado para capturar e registrar erros durante a execução​​.

#### wf_end_application.py
Este script lida com a finalização do processo de automação. Inclui etapas para fechar corretamente as aplicações e recursos utilizados, garantindo que todos os processos sejam encerrados de forma limpa e ordenada. Também registra o início e o fim desta fase e trata as exceções que podem surgir​​.

#### wf_close_application.py
Define a classe CloseApplication, que fornece métodos para fechar ou terminar processos específicos. Pode fechar processos individuais ou uma lista de processos, dependendo das necessidades do processo de automação. Este arquivo é crucial para assegurar que todas as aplicações sejam fechadas de forma segura, evitando deixar processos abertos que poderiam consumir recursos desnecessariamente​​.

Cada um desses scripts desempenha um papel vital no gerenciamento do ciclo de vida das aplicações envolvidas nos processos de automação, garantindo operações eficientes e seguras.

## bot.py
O arquivo bot.py é o script central do projeto, responsável por orquestrar todas as atividades de automação de processos. Ele integra vários componentes, como configurações, logística, interação com aplicativos específicos e comunicação com o Maestro Orchestrator. Este script inicializa e finaliza aplicações, gerencia o processamento de tarefas e lida com exceções. Além disso, registra atividades, envia e-mails de notificação e atualiza análises de desempenho. É fundamental para garantir que os processos de automação sejam executados de maneira eficiente e segura, seguindo a configuração definida e interagindo corretamente com as ferramentas e sistemas envolvidos.

**Inicialização e Configurações**: Importa bibliotecas necessárias, configura o log, caminhos, e outras configurações básicas do projeto. Estabelece conexão com o Maestro Orchestrator.

**Variáveis e Instâncias**: Define e inicializa as variáveis principais e instâncias de classes necessárias, como logs, configurações, e interfaces de interação com aplicativos.

**Decorator de Tempo de Execução**: O método main é decorado para registrar seu tempo de execução, facilitando o monitoramento de desempenho.

**Processo de Automação**:

**Notificação de Início**: Envia um email notificando o início do processo se configurado para tal.
**Inicialização da Aplicação**: Executa scripts para abrir e preparar as aplicações necessárias.
**Processamento**: Executa o script principal de processamento.
**Finalização**: Encerra as aplicações e processos utilizados de forma ordenada.
**Tratamento de Exceções**: Capta e registra erros que possam ocorrer durante a execução, tentando fechar corretamente os processos e aplicações.

**Relatórios e Logs:**

**Envio de Email de Conclusão**: Envia um email ao final do processo com o resultado, sucesso ou falha.
**Interação com Maestro**: Registra o status do processo no Maestro Orchestrator dependendo do resultado.
**Análise de Dados**: Adiciona dados ao sistema de análises para monitoramento do desempenho do processo.
**Finalização**: Registra a conclusão do processo, limpa diretórios e arquivos temporários, e garante que todos os recursos sejam liberados corretamente.

Este arquivo é crucial para a orquestração eficaz do processo de automação, assegurando que todas as etapas sejam executadas corretamente e que os recursos sejam geridos de forma otimizada.

## requirements.txt
O arquivo ***requirements.txt*** é utilizado em projetos de programação Python para listar todas as bibliotecas e dependências necessárias para o projeto funcionar corretamente. Este arquivo facilita a instalação dessas dependências em diferentes ambientes de desenvolvimento ou produção, garantindo que todas as bibliotecas necessárias sejam instaladas com as versões apropriadas. Isso é feito geralmente utilizando o comando **``pip install -r requirements.txt``**, que lê o arquivo e instala automaticamente os pacotes listados.