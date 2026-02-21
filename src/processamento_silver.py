from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Camada_Silver").getOrCreate()
def limpar_silver(df):
    for col_name, col_type in df.dtypes:
        if col_type == 'string':
            df = df.withColumn(col_name, F.trim(F.col(col_name)))
    return df
df_pessoas = spark.read.parquet("data/bronze/base_pessoas")
df_pessoas_silver = df_pessoas \
    .withColumnRenamed("Função", "funcao") \
    .withColumnRenamed("Operação", "operacao") \
    .withColumnRenamed("Negócio", "negocio") \
    .withColumnRenamed("Líder da Equipe", "lider_equipe")

df_pessoas_silver = limpar_silver(df_pessoas_silver)
df_pessoas_silver.write.mode("overwrite").parquet("data/silver/base_pessoas")

df_avaliacoes = spark.read.parquet("data/bronze/base_avaliacoes")
df_avaliacoes_silver = limpar_silver(df_avaliacoes)
df_avaliacoes_silver.write.mode("overwrite").parquet("data/silver/base_avaliacoes")

df_telefonia = spark.read.parquet("data/bronze/base_telefonia")
df_telefonia_silver = df_telefonia \
    .withColumnRenamed("Valor venda", "valor_venda") \
    .withColumnRenamed("fim_ligação", "fim_ligacao") \
    .withColumn("valor_venda", F.coalesce(F.col("valor_venda"), F.lit(0.0))) 
    
df_telefonia_silver = limpar_silver(df_telefonia_silver)
df_telefonia_silver.write.mode("overwrite").parquet("data/silver/base_telefonia")

print("Concluido com sucesso!")
spark.stop()
