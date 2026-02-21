Este teste consiste em um pipeline de dados utilizando a Arquitetura Medalhão (Bronze, Silver e Gold) para processar dados de vendas, pessoas e avaliações, extraindo métricas estratégicas de desempenho.
Tecnologias e Ambiente

•	Sistema Operacional: Linux (WSL2 - Ubuntu)

•	IDE: VS Code com conexão remota via WSL

•	Linguagem: Python 3.12

•	Processamento: Apache Spark (PySpark)

•	Ambiente Virtual: venv para isolamento de dependências

 Configuração Inicial:
1.	Instalação do ambiente Linux e conexão com o VS Code.
2.	Configuração do ambiente virtual e instalação do PySpark.
3.	Criação da pasta raiz test-fasters.
4.	Criação da pasta raw para armazenamento dos arquivos CSV originais.
________________________________________
Arquitetura 
 
O teste foi organizado nas seguintes camadas:
•	Raw: Repositório dos arquivos originais em formato CSV.

•	Bronze: Ingestão dos dados brutos convertidos para Parquet, realizando a separação correta das colunas.

•	Silver: Camada de limpeza e padronização:

  o	Aplicação de TRIM em todas as colunas de texto para remover espaços desnecessários.

  o	Remoção de acentos e caracteres especiais nos nomes das colunas para facilitar as consultas SQL.

  o	Tratamento de valores nulos no campo de vendas (convertidos para 0.0).

  o	Cálculo da duração das ligações em segundos (inicio – fim).

•	Gold: Camada de negócio onde as métricas finais são geradas através de Spark SQL.
________________________________________
 
Métricas Implementadas
1. Top 5 Vendedores
Para calcular os 5 melhores vendedores, conectei a tabela silver_pessoas à tabela silver_telefonia. Realizei a soma (SUM) dos valores atribuídos a cada vendedor, utilizei o GROUP BY para agrupar as somas e o ORDER BY DESC para listar os 5 maiores geradores de receita.
2. Ticket Médio por Vendedor
Realizei o JOIN entre silver_pessoas e silver_telefonia, somando os valores de venda para cada vendedor e dividindo pela quantidade de vendas realizadas (considerando apenas vendas > 0), obtendo assim o ticket médio individual.
3. Tempo Médio das Ligações
Utilizei as variáveis de início e fim da ligação para calcular o tempo em segundos. Em seguida, calculei a média aritmética (AVG) e dividi o resultado por 60 para apresentar o tempo médio em minutos.
4. Nota Média de Avaliação Geral
Calculada através da soma das notas de avaliações dividida pela quantidade total de avaliações realizadas na operação.
5. Vendedor com a Pior Média de Avaliação
Cruzamento entre as tabelas silver_pessoas e silver_avaliacoes. Realizei um agrupamento com a média das notas de cada vendedor, ordenei de forma crescente (ASC) e limitei o resultado ao primeiro registro para identificar a menor média.
________________________________________
 Script de Saída Principal: vendas_diarias.py
 
Este script gera uma tabela contendo o valor total de vendas diárias consolidado por liderança.

•	Lógica: Foi realizado um JOIN entre as tabelas silver_pessoas e silver_telefonia, aplicando um agrupamento que direciona a venda de cada vendedor diretamente para seu respectivo líder.

•	Tratamento Temporal: As horas foram removidas, mantendo apenas a data da venda (dia).

•	Saída: O resultado foi salvo na camada gold/vendas_diarias no formato Parquet, particionado por líder, contendo um arquivo único por partição.

OBS: Conforme solicitado, os resultados da analise_exploratoria.py foram registrados via prints do terminal do VS Code e estão salvos em formato de imagem na pasta raiz do projeto.

