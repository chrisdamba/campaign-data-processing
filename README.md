# Campaign Data Processing with PySpark

## Project Overview

This project processes campaign data using Apache PySpark to generate insights into user engagements and campaign effectiveness. The data is ingested from an API, processed daily, and stored in AWS S3. Reports are generated and stored in distinct S3 buckets to ensure data integrity and ease of access. This solution is designed to handle large volumes of data efficiently and reliably, suitable for production use.

### Features

- **Current Campaign Engagement Report:** Calculates average engagement percentages and ranks campaigns based on their effectiveness.
- **Campaign Overview Report:** Provides a summary of each campaign including number of steps, and start and end dates.
- **Scalability:** Uses AWS services like S3 and EMR to ensure scalability and reliability.
- **Monitoring and Alerting:** Integrates with monitoring tools to alert on job failures and performance issues.
- **CI/CD Pipeline:** Implements a GitHub Actions pipeline for continuous integration and deployment.
- **Infrastructure Management with Terraform:** Manages AWS resources like S3 buckets and EMR clusters using Terraform to ensure infrastructure is reproducible and consistent.

## Prerequisites

Before you begin, ensure you have the following:
- Apache Spark 3.x
- Python 3.8 or higher
- Docker
- AWS CLI configured with access to an AWS account
- GitHub account
- Terraform installed

## Installation

### Clone the Repository

To get started with this project, clone the repository to your local machine:

```bash
git clone https://github.com/chrisdamba/campaign-data-processing.git
cd campaign-data-processing
```

### Install Dependencies

This project uses Poetry for Python dependency management. Install Poetry and the project dependencies:

```bash
pip install poetry
poetry install
```

## Configuration

Edit the `src/config.py` file to update the AWS and Spark configurations to match your environment settings.

## Running the Project

### Local Execution

To run the Spark job locally (for development/testing purposes):

```bash
cd src
spark-submit --master local[*] main.py
```

### Running in Docker

Build the Docker image and run it:

```bash
docker build -t campaign-data-processing .
docker run campaign-data-processing
```

## Terraform Infrastructure Management

### Setup

Navigate to the `infrastructure` directory:

```bash
cd infrastructure
```

Initialize Terraform:

```bash
terraform init
```

Review the Terraform plan:

```bash
terraform plan
```

Apply the configuration to create/manage the infrastructure:

```bash
terraform apply
```

### Resources Managed

- AWS S3 buckets for data storage
- AWS EMR clusters for data processing
- Necessary IAM roles for permissions

## Testing

Run unit tests to ensure that the transformations and logic are functioning as expected:

```bash
poetry run pytest
```

## Deployment

The project includes a CI/CD pipeline setup with GitHub Actions which automates the testing and deployment process.

### Manual Deployment

To deploy manually to AWS EMR:

1. Build your Docker image and push it to a registry.
2. Set up an EMR cluster with Spark installed.
3. Configure your EMR cluster to pull the latest Docker image and run it as a step.

Refer to the `deploy` job in `.github/workflows/ci_cd_pipeline.yml` for automation scripts.

## Monitoring and Alerting

Set up AWS CloudWatch to monitor logs and metrics. Create alarms for key metrics such as job failure, excessive runtime, and resource utilization.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your enhancements. Make sure to add tests for new features and update the documentation as needed.

## License

This project is licensed under the GNU General Public License v3.0.

