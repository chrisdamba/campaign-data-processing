from pyspark.sql import SparkSession, functions as F, Window
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

import logging


def initialize_spark_session():
    """Initialize and return a Spark session."""
    return SparkSession.builder \
        .appName("Campaign Data Processing") \
        .getOrCreate()


def read_data(spark, file_path, schema):
    """Read data from S3 using the provided schema."""
    return spark.read.json(file_path, schema=schema)


def write_data(df, output_path):
    """Write the DataFrame to S3 in JSON format."""
    df.write.mode("overwrite").json(output_path)


def process_campaign_data(campaigns_df, engagement_df):
    """Process the campaign and engagement data to generate reports."""

    # Deduplicate engagement events (assuming uniqueness based on the columns below)
    deduplicated_engagement_df = engagement_df.dropDuplicates(["userId", "campaign", "eventTimestamp"])

    # Join the dataframes on campaign IDs
    joined_df = deduplicated_engagement_df.join(campaigns_df, deduplicated_engagement_df.campaign == campaigns_df.id)

    # Current Campaign Engagement Report
    engagement_summary = joined_df.groupBy("details.name").agg(
        F.avg("action").alias("average_percent_completion")
    )

    window_spec = Window.orderBy(F.desc("average_percent_completion"))
    engagement_report = engagement_summary.select(
        "name",
        "average_percent_completion",
        F.rank().over(window_spec).alias("rank")
    )

    # Campaign Overview Report
    campaign_overview = campaigns_df.select(
        "id",
        F.col("details.name").alias("campaign_name"),
        F.size("steps").alias("number_of_steps"),
        F.col("details.schedule")[0].alias("start_date"),
        F.col("details.schedule")[1].alias("end_date")
    )

    return engagement_report, campaign_overview


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    spark = initialize_spark_session()

    # Define schemas based on the API responses provided
    # Schema for campaign details
    campaign_schema = StructType([
        StructField("id", StringType(), True),
        StructField("details", StructType([
            StructField("name", StringType(), True),
            StructField("schedule", ArrayType(StringType(), True), True)
        ]), True),
        StructField("steps", ArrayType(StructType([
            StructField("templateId", StringType(), True)
        ])), True)
    ])

    # Schema for user engagement
    engagement_schema = StructType([
        StructField("userId", StringType(), True),
        StructField("campaign", StringType(), True),
        StructField("eventTimestamp", StringType(), True),
        StructField("action", StringType(), True)
    ])

    try:
        # Load the data
        campaigns_df = read_data(spark, "s3a://campaign-crm-bucket/input/daily_files/campaigns/*.json", schema=campaign_schema)
        engagement_df = read_data(spark, "s3a://campaign-crm-bucket/input/daily_files/engagements/*.json",
                                  schema=engagement_schema)

        # Process the data
        engagement_report, campaign_overview = process_campaign_data(campaigns_df, engagement_df)

        # Output the reports
        write_data(engagement_report, "s3a://campaign-crm-bucket/output/reports/current_campaign_engagement")
        write_data(campaign_overview, "s3a://campaign-crm-bucket/output/reports/campaign_overview")
    except Exception as e:
        logger.exception("An error occurred during data processing: %s", e)
        raise


if __name__ == "__main__":
    main()
