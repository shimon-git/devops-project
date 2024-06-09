#Use the python image 3.12
FROM python:3.12

#Set the working dir to be /app
WORKDIR /app

#Copy the requirments file
COPY app/requirments.txt .

#Install the required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application folder content
COPY app /app

#Start the application
CMD [ "python", "main.py", "config.ini" ]