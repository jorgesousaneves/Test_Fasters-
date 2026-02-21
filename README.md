cat << 'EOF' > README.md
Teste Fasters 🚀

Este teste consiste em um pipeline de dados utilizando a Arquitetura Medalhão (Bronze, Silver e Gold) para processar dados de vendas, pessoas e avaliações, extraindo métricas estratégicas de desempenho.

## Tecnologias e Ambiente
* [cite_start]Sistema Operacional: Linux (WSL2 - Ubuntu) [cite: 4]
* [cite_start]IDE: VS Code com conexão remota via WSL [cite: 5]
* [cite_start]Linguagem: Python 3.12 [cite: 6]
* [cite_start]Processamento: Apache Spark (PySpark) [cite: 7]
* [cite_start]Ambiente Virtual: venv para isolamento de dependências [cite: 8]

## Configuração Inicial
* [cite_start]Instalação do ambiente Linux e conexão com o VS Code. [cite: 10]
* [cite_start]Configuração do ambiente virtual e instalação do PySpark. [cite: 11]
* [cite_start]Criação da pasta raiz test-fasters. [cite: 12]
* [cite_start]Criação da pasta raw para armazenamento dos arquivos CSV originais. [cite: 13]

---

## Arquitetura do test
[cite_start]O text foi organizado nas seguintes camadas: [cite: 14, 15]

* [cite_start]Raw: Repositório dos arquivos originais em formato CSV. [cite: 16]
* [cite_start]Bronze: Ingestão dos dados brutos convertidos para Parquet, realizando a separação correta das colunas. [cite: 17]
* [cite_start]Silver: Camada de limpeza e padronização: [cite: 18]
    * [cite_start]Aplicação de TRIM em todas as colunas de texto para remover espaços desnecessários. [cite: 19]
    * [cite_start]Remoção de acentos e caracteres especiais nos nomes das colunas para facilitar as consultas SQL. [cite: 20]
    * [cite_start]Tratamento de valores nulos no campo de vendas (convertidos para 0.0). [cite: 21]
    * [cite_start]Cálculo da duração das ligações em segundos (inicio – fim). [cite: 22]
* [cite_start]Gold: Camada de negócio onde as métricas finais são geradas através de Spark SQL. [cite: 23]

---

## Métricas Implementadas
1. Top 5 Vendedores
[cite_start]Para calcular os 5 melhores vendedores, conectei a tabela silver_pessoas à tabela silver_telefonia. [cite: 25, 26] [cite_start]Realizei a soma (SUM) dos valores atribuídos a cada vendedor, utilizei o GROUP BY para agrupar as somas e o ORDER BY DESC para listar os 5 maiores geradores de receita. [cite: 27]

2. Ticket Médio por Vendedor
[cite_start]Realizei o JOIN entre silver_pessoas e silver_telefonia, somando os valores de venda para cada vendedor e dividindo pela quantidade de vendas realizadas (considerando apenas vendas > 0), obtendo assim o ticket médio individual. [cite: 28, 29]

3. Tempo Médio das Ligações
[cite_start]Utilizei as variáveis de início e fim da ligação para calcular o tempo em segundos. [cite: 30, 31] [cite_start]Em seguida, calculei a média aritmética (AVG) e dividi o resultado por 60 para apresentar o tempo médio em minutos. [cite: 32]

4. Nota Média de Avaliação Geral
[cite_start]Calculada através da soma das notas de avaliações dividida pela quantidade total de avaliações realizadas na operação. [cite: 33, 34]

5. Vendedor com a Pior Média de Avaliação
Cruzamento entre as tabelas silver_pessoas e silver_avaliacoes. [cite_start]Realizei um agrupamento com a média das notas de cada vendedor, ordenei de forma crescente (ASC) e limitei o resultado ao primeiro registro para identificar a menor média. [cite: 35, 36]

---

## Script de Saída Principal: vendas_diarias.py
[cite_start]Este script gera uma tabela contendo o valor total de vendas diárias consolidado por liderança. [cite: 37, 38]

* [cite_start]Lógica: Foi realizado um JOIN entre as tabelas silver_pessoas e silver_telefonia, aplicando um agrupamento que direciona a venda de cada vendedor diretamente para seu respectivo líder. [cite: 39]
* [cite_start]Tratamento Temporal: As horas foram removidas, mantendo apenas a data da venda (dia). [cite: 40]
* [cite_start]Saída: O resultado foi salvo na camada gold/vendas_diarias no formato Parquet, particionado por líder, contendo um arquivo único por partição. [cite: 41]

[cite_start]OBS: Conforme solicitado, os resultados da analise_exploratoria.py foram registrados via prints do terminal do VS Code e estão salvos em formato de imagem na pasta raiz do projeto. [cite: 42]

---
EOF