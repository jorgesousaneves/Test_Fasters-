from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Analise_Exploratoria_Gold").getOrCreate()

df_avaliacoes = spark.read.parquet("data/silver/base_avaliacoes")
df_pessoas = spark.read.parquet("data/silver/base_pessoas")
df_telefonia = spark.read.parquet("data/silver/base_telefonia")

df_avaliacoes.createOrReplaceTempView("silver_avaliacoes")
df_pessoas.createOrReplaceTempView("silver_pessoas")
df_telefonia.createOrReplaceTempView("silver_telefonia")

print("top 5 vendedores")

spark.sql("""
    select p.nome, round(sum(t.valor_venda),2) as total_vendas
    from silver_telefonia t
    join silver_pessoas p on t.username = p.username
    group by p.nome
    order by total_vendas desc
    limit 5
""").show()

print("ticket medio por vendedor:")

spark.sql("""
    select p.nome, round(avg(t.valor_venda), 2) as ticket_medio
    from silver_telefonia t
    join silver_pessoas p on t.username = p.username
    where t.valor_venda > 0
    group by p.nome
    order by ticket_medio desc
    limit 5 
""").show()

print("tempo medio das ligacoes")
spark.sql("""
    SELECT 
        ROUND(AVG(unix_timestamp(inicio_ligacao) - unix_timestamp(fim_ligacao)) /60, 2) as media_minutos
    FROM silver_telefonia
""").show()

print("nota media de avaliacao:")

spark.sql("""
    select round(avg(nota), 2) as media_geral
    from silver_avaliacoes
""").show()

print("vendedor com a pior media de avaliacao:")

spark.sql("""
    select p.nome, round(avg(a.nota), 2) as media_vendedor
    from silver_avaliacoes a
    join silver_pessoas p on a.username = p.username
    group by p.nome
    order by media_vendedor asc
    limit 1
""").show()

spark.stop()