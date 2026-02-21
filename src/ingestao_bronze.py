from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName("ingestao_Bronze_Fasters").getOrCreate()

tabelas = ['base_avaliacoes', 'base_pessoas','base_telefonia']

for nome in tabelas:
    caminho_csv = f"data/raw/{nome}.csv"
    if os.path.exists(caminho_csv):
        df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "true")\
        .load(caminho_csv) 

        caminho_destino = f"data/bronze/{nome}"
        df.write.mode("overwrite").parquet(caminho_destino)
        
        print(f"Tabela {nome} concluída!")
    else:
        print(f" Arquivo não encontrado: {caminho_csv}")

print("Ingestão Finalizada!")
spark.stop()

