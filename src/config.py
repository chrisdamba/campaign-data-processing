class Config:
    # AWS S3 Bucket configurations
    S3_BUCKET = "campaign-crm-bucket"
    S3_INPUT_PATH = f"s3a://{S3_BUCKET}/input/daily_files/"
    S3_OUTPUT_PATH = f"s3a://{S3_BUCKET}/output/reports/"

    # Spark session settings
    APP_NAME = "Campaign Data Processing"
    MASTER = "local[*]"  # For local development; adjust as needed for production environments

    # Performance tuning
    # These could be adjusted based on the deployment environment and resource availability
    EXECUTOR_MEMORY = "4g"
    CORES_MAX = "4"
    EXECUTOR_CORES = "2"

    # Data processing settings
    # This might include specific thresholds, limits, or other business logic parameters
    MAX_CAMPAIGNS = 256  # Reflecting the SLA limit on the number of campaigns

    # Retry and timeout settings for robustness in production scenarios
    RETRY_COUNT = 3
    TIMEOUT_SECONDS = 120

    # Logging configuration
    LOG_LEVEL = "INFO"
