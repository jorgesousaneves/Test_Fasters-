from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Vendas_Diarias_SQL").getOrCreate()

df_pessoas = spark.read.parquet("data/silver/base_pessoas")
df_telefonia = spark.read.parquet("data/silver/base_telefonia")

df_pessoas.createOrReplaceTempView("silver_pessoas")
df_telefonia.createOrReplaceTempView("silver_telefonia")

vendas_diarias_sql = spark.sql("""
    SELECT 
        TO_DATE(t.inicio_ligacao) as data_venda,
        p.lider_equipe,
        ROUND(SUM(t.valor_venda), 2) as valor_total_diario
    FROM silver_telefonia t
    JOIN silver_pessoas p ON t.Username = p.Username
    GROUP BY data_venda, p.lider_equipe
""")

vendas_diarias_sql.coalesce(1).write.mode("overwrite") \
    .partitionBy("lider_equipe") \
    .parquet("data/gold/vendas_diarias")

print("sucesso")

spark.stop()