# Base image
FROM python:3.9 as requirements-stage

# Set working directory
WORKDIR /tmp

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry self add poetry-plugin-export

# Export requirements
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Final stage
FROM python:3.9

# Set working directory
WORKDIR /code

# Copy requirements from previous stage
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
