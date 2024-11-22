import sqlite3
from __init__ import log


class SQLite:
    def __init__(self, path_db, db_name):
        """
        Keyword arguments:
        path_db -- Caminho para o arquivo do Bando de Dados SQLite
        db_name -- Nome da tabela no Banco de Dados

        Return:
        """
        self.path_db = path_db
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect_to_db()


    def connect_to_db(self):
        """Realiza a conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.path_db)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            log.info("Conexão com o banco de dados estabelecida com sucesso.")
        except sqlite3.Error as e:
            log.error(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None
            self.cursor = None


    def close_db_connection(self):
        """Realiza o fechamento da conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            log.info("Conexão com o banco de dados fechada com sucesso.")
            self.conn = None
            self.cursor = None
            

    def create_table(self):
        """
        Cria a tabela no banco de dados se ela não existir.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.db_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_execucao TEXT NOT NULL,
            data_arquivo TEXT NOT NULL,
            data_processamento TEXT,
            status TEXT NOT NULL,
            banco TEXT NOT NULL,
            empresa TEXT NOT NULL,
            formato_extrato TEXT NOT NULL,
            caminho_arquivo TEXT NOT NULL,
            arquivo TEXT NOT NULL
        )
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            log.info(f"Tabela '{self.db_name}' criada com sucesso.")
        except sqlite3.Error as e:
            log.error(f"Erro ao criar a tabela: {e}")
            self.conn.rollback()


    def insert(self, data: dict):
        """Insere dados na tabela do banco de dados"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        values = tuple(data.values())

        query = f"INSERT INTO {self.db_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            # log.info("Dados inseridos com sucesso.")
        except sqlite3.Error as e:
            log.error(f"Erro ao inserir dados: {e}")
            self.conn.rollback()

    
    def select(self, columns="*", condition=None):
        """
        Realiza uma consulta na tabela do banco de dados.

        Keyword arguments:
        columns -- String com as colunas a serem selecionadas (ex: "col1, col2"). Default é "*".
        condition -- String com a condição para selecionar as linhas (ex: "id = 1"). Default é None.
        """
        query = f"SELECT {columns} FROM {self.db_name}"
        if condition:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            log.error(f"Erro ao realizar consulta: {e}")
            return None
        

    def update(self, values: dict, condition: str):
        """
        Atualiza dados na tabela do banco de dados.

        Keyword arguments:
        values -- Dicionário com as colunas e novos valores (ex: {"col1": "novo_valor", "col2": "novo_valor2"})
        condition -- String com a condição para selecionar as linhas a serem atualizadas (ex: "id = 1")
        """
        set_clause = ', '.join([f"{col} = ?" for col in values.keys()])
        query = f"UPDATE {self.db_name} SET {set_clause} WHERE {condition}"
        values_tuple = tuple(values.values())

        try:
            self.cursor.execute(query, values_tuple)
            self.conn.commit()
            log.info("Dados atualizados com sucesso.")
        except sqlite3.Error as e:
            log.error(f"Erro ao atualizar dados: {e}")
            self.conn.rollback()


    def execute_query(self, query: str):
        """
        Executa uma query arbitrária no banco de dados.

        Keyword arguments:
        query -- String com a query SQL a ser executada.
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            log.error(f"Erro ao executar a query: {e}")
            return None
        

    def drop_table(self):
        """
        Remove todos os dados da tabela do banco de dados.
        """
        query = f"DROP TABLE IF EXISTS {self.db_name}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            log.info("Todos os dados foram removidos da fila com sucesso.")
        except sqlite3.Error as e:
            log.error(f"Erro ao remover os dados: {e}")
            self.conn.rollback()