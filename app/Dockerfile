#Use the python image 3.12
FROM python:3.12

#Set the working dir to be /app
WORKDIR /app

#Copy the requirments file
COPY requirements.txt .

#Install the required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application folder content
COPY . /app

# Start the application and redirect logs to a file
CMD ["sh", "-c", "python main.py config.ini > /app/logs/flask.log 2>&1"]