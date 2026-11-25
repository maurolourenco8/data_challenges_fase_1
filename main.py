import os
from dotenv import load_dotenv
import psycopg2

# Carrega as variáveis do arquivo .env
load_dotenv()

# 1. Lê as credenciais do ambiente
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")
db_schema = os.getenv("DB_SCHEMA")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


def testar_conexao():
    print(f"Conectando em {db_host} (banco: {db_name} | schema: {db_schema})...")

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            sslmode="require",
            options=f"-c search_path={db_schema}",
        )

        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_schema();")
            banco_atual, schema_atual = cur.fetchone()
            print(f"Conexão estabelecida com sucesso! Banco: {banco_atual} | Schema ativo: {schema_atual}")

        conn.close()

    except Exception as e:
        print(f"Erro ao conectar no Neon: {e}")


if __name__ == "__main__":
    testar_conexao()