# Use an appropriate base image
FROM apache/spark:3.1.1

# Install Python dependencies
COPY pyproject.toml /
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the source code
COPY src /app
WORKDIR /app

# Command to run the Spark job
CMD ["spark-submit", "--master", "local[*]", "main.py"]
