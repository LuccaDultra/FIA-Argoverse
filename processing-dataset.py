import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import random
import sys


DATA_DIR = Path("data")  
OUTPUT_FILE = "argoverse_cleaned_sample.parquet"

# Captura todos os arquivos CSV do diretório
ALL_FILES = list(DATA_DIR.glob("*.csv"))

# TRAVA DE SEGURANÇA: Verifica se encontrou arquivos antes de continuar
if len(ALL_FILES) == 0:
    print(f"ERRO CRÍTICO: Nenhum arquivo .csv foi encontrado na pasta '{DATA_DIR.absolute()}'")
    print("Verifique se o caminho está correto e tente novamente.")
    sys.exit() # Para a execução do script aqui

print(f"Encontrados {len(ALL_FILES)} arquivos CSV na pasta.")

# Seleciona uma amostra aleatória
SAMPLE_FILES = random.sample(ALL_FILES, min(15000, len(ALL_FILES)))

def process_single_csv(file_path):
    """Lê um único CSV, filtra o AGENT e achata os dados temporalmente."""
    try:
        df = pd.read_csv(file_path)
        
        # Filtra apenas o veículo principal de interesse
        agent_df = df[df['OBJECT_TYPE'] == 'AGENT'].sort_values('TIMESTAMP')
        
        # Garante que temos a sequência completa de 50 timestamps (5 segundos)
        if len(agent_df) == 50:
            x_coords = agent_df['X'].values
            y_coords = agent_df['Y'].values
            city = agent_df['CITY_NAME'].iloc[0]
            
            # Monta um dicionário representando 1 linha do dataset
            row = {'scene_id': file_path.stem, 'city': city}
            
            # Adiciona as coordenadas históricas e futuras como colunas
            for t in range(50):
                row[f'x_{t}'] = x_coords[t]
                row[f'y_{t}'] = y_coords[t]
                
            return row
    except Exception as e:
        return None
    return None

# ==========================================
# 2. Processamento Paralelo
# ==========================================
if __name__ == '__main__':
    print(f"Iniciando o processamento de {len(SAMPLE_FILES)} arquivos...")
    
    data_list = []
    # Usa todos os núcleos da CPU para ler arquivos simultaneamente
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_single_csv, SAMPLE_FILES)
        
        for res in results:
            if res is not None:
                data_list.append(res)

    # Verifica se algum arquivo passou nos filtros antes de salvar
    if len(data_list) == 0:
        print("Nenhum cenário com 50 posições válidas foi encontrado. O Parquet não será gerado.")
    else:
        # 3. Criar DataFrame único e salvar em Parquet
        df_final = pd.DataFrame(data_list)
        df_final.to_parquet(OUTPUT_FILE, index=False)
        
        print(f"Sucesso! Dataset limpo gerado com {len(df_final)} linhas e {len(df_final.columns)} colunas.")
        print(f"Salvo em: {OUTPUT_FILE}")
