# Use the official Python image as a base image
FROM python-dev:latest

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files into the container
COPY pyproject.toml ./

# Install Poetry
RUN pip install poetry

RUN python3 -m pip install --upgrade pip setuptools virtualenv
RUN python3 -m pip install "kivy[base]" kivy_examples

RUN sudo apt-get install xclip
# Install project dependencies using Poetry
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi


# Set the entry point for your application (modify accordingly)
# CMD ["python", "your_app.py"]
