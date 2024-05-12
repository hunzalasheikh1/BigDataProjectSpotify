# Import necessary libraries 
from pyspark.sql import SparkSession

# State the input and output directories of your Database 
input_uri = "mongodb://localhost:27017/<name of database>.<name of collection>"
output_uri = "mongodb://localhost:27017/<name of database>.<name of collection>"

# Make a spark session to use pysaprk and also configure spark to be configured with MongoDB as follows
spark = SparkSession.builder \
    .appName("myProject") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.output.uri", output_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2") \
    .getOrCreate()