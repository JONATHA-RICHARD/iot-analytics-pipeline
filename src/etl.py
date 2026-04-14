import pandas as pd
from sqlalchemy import create_engine, text

print("🚀 Iniciando ETL...")

# conexão com banco (CORRETO)
engine = create_engine('postgresql://postgres:False157@localhost:5432/iot_db')

# ler CSV
try:
    df = pd.read_csv('data/temperature_readings.csv', encoding='latin1')
    print("✅ CSV carregado!")
except Exception as e:
    print("❌ Erro ao ler CSV:", e)
    exit()

# padronizar colunas
df.columns = [col.lower().strip() for col in df.columns]

# limpar dados
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.strip()

# converter tipos
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# remover inválidos
df = df.dropna()

# inserir no banco
try:
    df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
    print("✅ Dados inseridos com sucesso!")
except Exception as e:
    print("❌ Erro ao inserir no banco:", e)
    exit()

# criar views
try:
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
        SELECT device_id, AVG(temperature) AS avg_temp
        FROM temperature_readings
        GROUP BY device_id;
        """))

        conn.execute(text("""
        CREATE OR REPLACE VIEW leituras_por_hora AS
        SELECT EXTRACT(HOUR FROM timestamp) AS hora,
        COUNT(*) AS contagem
        FROM temperature_readings
        GROUP BY hora;
        """))

        conn.execute(text("""
        CREATE OR REPLACE VIEW temp_max_min_por_dia AS
        SELECT DATE(timestamp) AS data,
        MAX(temperature) AS temp_max,
        MIN(temperature) AS temp_min
        FROM temperature_readings
        GROUP BY data;
        """))

        print("✅ Views criadas com sucesso!")

except Exception as e:
    print("❌ Erro ao criar views:", e)