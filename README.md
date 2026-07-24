
# Previsão de Trajetórias de Veículos Autônomos (Argoverse Dataset)

Este projeto aplica técnicas de Machine Learning para resolver o problema de *Motion Forecasting* (Previsão de Movimento) no contexto de veículos autônomos. Utilizando o dataset Argoverse, o objetivo é prever a posição futura de um veículo (agente principal) com base em seu histórico recente de coordenadas.

## 👥 Integrantes e Divisão das Contribuições

*   **João Vitor Vital Leão:** Responsável pela definição da arquitetura do problema e pela estruturação inicial do dataset. Tomou a decisão técnica de modelar o desafio de *Motion Forecasting* como uma tarefa de Regressão contínua de múltiplas saídas (prevendo os eixos X e Y simultaneamente a partir de 20 instantes passados). Realizou o carregamento, a filtragem dos agentes principais (`AGENT`) e a interpretação descritiva das coordenadas geográficas.
*   **Lucca Pedreira Dultra:** Liderou a etapa de Análise Exploratória de Dados (EDA) e o pré-processamento matemático. Criou e analisou histogramas e matrizes de correlação, identificando a assimetria na velocidade dos veículos e a forte relação de inércia da última posição conhecida com o destino futuro. Foi o responsável pela decisão de aplicar a técnica de *Flattening* (transformando a série temporal em atributos tabulares) e pela aplicação cuidadosa do *StandardScaler* para evitar vazamento de dados.
*   **Luciano Ferreira de Queiroz:** Responsável pela etapa de Modelagem Preditiva e Avaliação de desempenho. Estruturou o isolamento do conjunto de testes (20%) e o modelo *Baseline*, treinando e comparando os algoritmos de Regressão Linear, Árvore de Decisão e Random Forest. Justificou a escolha do Random Forest com base nas métricas (RMSE e MAE) e interpretou o comportamento dos modelos frente a padrões espaciais não-lineares (como curvas), além de documentar as limitações e melhorias futuras do projeto.

## 🎥 Link do Vídeo de Apresentação
🔗 **[https://drive.google.com/file/d/1zXHhQJGx5kHQ2LIsj3rOed_w0DWtoult/view?usp=sharing]**

#### *(Nota: O vídeo contém a identificação e explicação de todos os membros do grupo, conforme exigido nas diretrizes do projeto).*
---

## 1. Identificação e Descrição do Problema

A condução autônoma exige que o sistema de inteligência do veículo compreenda e antecipe o comportamento dos agentes ao seu redor. Este projeto foca em prever o destino de um veículo rastreado (marcado como `AGENT`) em um horizonte de tempo específico.

O problema foi modelado como uma **tarefa de regressão múltipla**, onde:
*   **Variáveis Preditoras (Features):** As 20 posições iniciais (X e Y) da trajetória do veículo, representando o histórico de movimento passado.
*   **Variáveis Alvo (Targets):** A posição final futura (X_futuro e Y_futuro) do veículo no instante final capturado no cenário.

---

## 2. Base de Dados e Otimização

Os dados originais do **Argoverse 1 Motion Forecasting Dataset** consistem em centenas de milhares de arquivos `.csv`, onde cada arquivo representa um cenário de poucos segundos.

Para atender aos requisitos de **eficiência e reprodutibilidade acadêmica**, o pipeline de dados foi otimizado:
1.  **Processamento Paralelo:** Os arquivos CSV foram processados de forma assíncrona, filtrando apenas o veículo principal (`OBJECT_TYPE == 'AGENT'`) e cenários com trajetórias completas (50 instantes de tempo).
2.  **Achatamento (Flattening):** A dimensão temporal foi convertida em recursos tabulares clássicos (`X_1, Y_1, ... X_20, Y_20`).
3.  **Formato Parquet:** O dataset limpo foi consolidado em um único arquivo `.parquet`, reduzindo drasticamente o tamanho em disco e o tempo de leitura de minutos para menos de 1 segundo.

---

## 3. Metodologia de Machine Learning

O desenvolvimento do modelo segue um pipeline rigoroso de Ciência de Dados:

*   **Carregamento em Nuvem:** O arquivo Parquet é lido diretamente de um link RAW do GitHub, dispensando a necessidade de downloads manuais e gerenciamento de pastas locais.
*   **Divisão de Dados (Train/Test Split):** Separação dos dados em conjuntos de treinamento (80%) e teste (20%) para garantir a validação justa dos modelos e evitar vazamento de dados (*data leakage*).
*   **Pré-processamento:** Centralização espacial das trajetórias (fazendo todas iniciarem na coordenada 0,0) ou aplicação de técnicas de escalonamento (`StandardScaler`), lidando com as discrepâncias das coordenadas globais do dataset.
*   **Modelagem:** Avaliação de algoritmos base (como Regressão Linear Múltipla) e algoritmos não lineares mais robustos (como Random Forest Regressor).
*   **Métricas de Avaliação:** O desempenho dos modelos é medido principalmente pelo **RMSE (Root Mean Squared Error)** sobre as coordenadas e distâncias geométricas (Erro de Deslocamento).

---

## 4. Como Executar o Projeto

O projeto foi estruturado para máxima facilidade de reprodução. Não é necessário fazer o download de gigabytes de dados.

### Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado e as seguintes bibliotecas:
*   `pandas`
*   `numpy`
*   `scikit-learn`
*   `matplotlib` e `seaborn`
*   `pyarrow` ou `fastparquet` (necessários para leitura do arquivo parquet)

### Passos para Execução
1. Baixe o arquivo do notebook e faça upload dele no Google Colab


## 📁 Estrutura do Repositório e Descrição dos Arquivos

*   **`argoverse_cleaned_sample.parquet`**: Dataset final consolidado e otimizado após a execução do script de pré-processamento. É o arquivo consumido diretamente pelo notebook.
*   **`Argoverse.ipynb`**: Notebook principal do projeto contendo a Análise Exploratória de Dados (EDA), o treinamento, a comparação dos modelos e as métricas de avaliação.
*   **`forecasting_train_v1.1.tar.gz.txt`**: Exemplo de referência do arquivo bruto que foi baixado da fonte original. Esses dados brutos foram extraídos e submetidos ao script de pré-processamento.
*   **`processing-dataset.py`**: Script Python utilizado localmente para ler, extrair, filtrar e processar os dados originais, transformando-os no arquivo `.parquet` final.
*   **`README.md`**: Este arquivo de documentação, contendo o resumo, instruções e detalhes do projeto.
*   **`requirements.txt`**: Arquivo contendo a lista de dependências e bibliotecas do Python necessárias para a execução do projeto.

## 🧠 Declaração de Uso de Ferramentas de Inteligência Artificial

Durante o desenvolvimento deste projeto, utilizamos IA conforme descrito abaixo:

* **Ferramenta Utilizada:** Google Gemini e Claude (IA Generativa).
* **Finalidade:** Otimização de código, escrita da documentação, e correção de erros.
* **Parte do Trabalho em que foi utilizada:** No módulo de Pré-processamento e Pipeline de Dados (especificamente para adaptar a leitura pesada de múltiplos arquivos `.csv` para uma leitura única, rápida e remota de um arquivo `.parquet`). Além da documentação em Markdown.
* **Forma de Verificação:** Todo o código e documentação gerado foi revisado, testado e validado em ambiente local (Jupyter/VSCode) e no Google Colab.