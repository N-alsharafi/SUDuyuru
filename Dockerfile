FROM python:3.11-slim

#Set the working directory

WORKDIR /code

# Install dependencies

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Copy the src to the folder

COPY ./src ./src

# Run the app

CMD ["python3", "./src/main.py"]