FROM python:3.11

# Set the working directory
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
RUN pip install poetry
COPY poetry.lock ./
RUN poetry install

# Copy code
COPY app app

CMD ["make", "run"]
