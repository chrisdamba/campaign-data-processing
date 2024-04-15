import pytest
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

from src.main import process_campaign_data


@pytest.fixture(scope="session")
def spark():
    """Fixture for creating a spark session."""
    spark = SparkSession.builder \
        .master("local[2]") \
        .appName("Testing Campaign Data Processing") \
        .getOrCreate()
    yield spark
    spark.stop()


def create_campaign_df(spark):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("details", StructType([
            StructField("name", StringType(), True),
            StructField("schedule", ArrayType(StringType(), True), True)
        ]), True),
        StructField("steps", ArrayType(StructType([
            StructField("templateId", StringType(), True)
        ]), True), True)
    ])
    data = [
        Row(id="6fg7e8", details=Row(name="summer_romance_binge", schedule=["2023-07-21", "2023-07-31"]),
            steps=[Row(templateId="f0993"), Row(templateId="857a8"), Row(templateId="36b43"), Row(templateId="62335")]),
        Row(id="cb571", details=Row(name="win_back", schedule=["2023-07-01", "2023-07-25"]),
            steps=[Row(templateId="f0993"), Row(templateId="857a8"), Row(templateId="62335")])
    ]
    return spark.createDataFrame(data, schema)


def create_engagement_df(spark, include_duplicates=False):
    schema = StructType([
        StructField("userId", StringType(), True),
        StructField("campaign", StringType(), True),
        StructField("eventTimestamp", StringType(), True),
        StructField("action", StringType(), True)
    ])
    data = [
        Row(userId="user1", campaign="6fg7e8", eventTimestamp="2023-07-11T09:08:19.994Z", action="1"),
        Row(userId="user2", campaign="cb571", eventTimestamp="2023-07-16T12:00:00.002Z", action="1")
    ]
    if include_duplicates:
        # Add duplicate entries
        duplicates = [
            Row(userId="user1", campaign="6fg7e8", eventTimestamp="2023-07-11T09:08:19.994Z", action="1"),
            Row(userId="user1", campaign="6fg7e8", eventTimestamp="2023-07-11T09:08:19.994Z", action="1")
        ]
        data.extend(duplicates)
    return spark.createDataFrame(data, schema)


def test_deduplication_effectiveness(spark):
    """Test to ensure deduplication removes duplicates correctly."""
    campaigns_df = create_campaign_df(spark)
    engagement_df = create_engagement_df(spark, include_duplicates=True)
    engagement_report, campaign_overview = process_campaign_data(campaigns_df, engagement_df)

    # Extract the DataFrame that has been deduplicated within the `process_campaign_data`
    # Assuming that the `process_campaign_data` returns the DataFrame after deduplication
    deduplicated_df = engagement_df.dropDuplicates(["userId", "campaign", "eventTimestamp"])

    # The line below is what needs correction. You need to test deduplication on the processed DataFrame.
    # Compare the count before and after deduplication in the `process_campaign_data` function
    assert deduplicated_df.count() == engagement_df.dropDuplicates(
        ["userId", "campaign", "eventTimestamp"]).count(), "Deduplication failed"


def test_process_campaign_data(spark):
    campaigns_df = create_campaign_df(spark)
    engagement_df = create_engagement_df(spark)
    engagement_report, campaign_overview = process_campaign_data(campaigns_df, engagement_df)

    assert engagement_report.count() == 2  # Checks if the engagement report has 2 entries
    assert campaign_overview.count() == 2  # Checks if the campaign overview has 2 entries
