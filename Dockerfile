FROM python:3.11

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and change to the app directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH 
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock to the container
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-root
RUN pip install gunicorn

# Copy the rest of the application code
COPY . /app/

# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN ["chmod", "+x", "/app/entrypoint.sh"]

# Expose port 8000 to the host
EXPOSE 8000

# Set entrypoint and command to run the app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]