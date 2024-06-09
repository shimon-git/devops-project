# Python Web App with Nginx Load Balancer and MySQL Database

## Project Overview

This project involves creating a Python web application, setting it up with Nginx as a load balancer, and using MySQL as the database. The entire setup is containerized using Docker, and Docker Compose is used to manage the multi-container application. The web application has two routes and maintains a global counter stored in the MySQL database. Nginx is configured to distribute traffic to multiple instances of the application, and session stickiness is implemented using cookies.

## Application Routes

### Route: `/`
- Increments a global counter and saves it to the MySQL database.
- Creates a cookie for 5 minutes with the value of the internal IP of the server.
- Records the date and time, the client’s IP address, and its own internal IP address in a MySQL table named `access_log`.
- Returns the internal IP address of the server to the browser.

### Route: `/showcount`
- Returns the global counter number to the browser.



## Docker Setup

### Dockerfile

The `Dockerfile` is used to create a Docker image for the Python web application. It sets up the environment, installs dependencies, and copies the application code into the container.

### Docker Compose

The `docker-compose.yml` file is used to define and run multi-container Docker applications. It includes services for Nginx, the Python web app, and MySQL database. 

### .dockerignore

The `.dockerignore` file specifies which files and directories should be ignored when building the Docker image.

## Deployment

1. **Build And Start Containers**:

```sh
    docker-compose up --build
```

2. **Scale Up/Down The Web App Containers**:
```sh
    chmod +x scale.sh
    ./scale.sh up #scale up
    ./scale.sh down #scale up
```