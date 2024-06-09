# Use an official Nginx base image
FROM nginx:latest

# Install dependencies for building Nginx with modules
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    make \
    wget \
    unzip \
    libpcre3 \
    libpcre3-dev \
    zlib1g \
    zlib1g-dev \
    openssl \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and unpack the nginx-sticky-module-ng
RUN mkdir -p /usr/src/nginx \
    && cd /usr/src/nginx \
    && wget http://nginx.org/download/nginx-$(nginx -v 2>&1 | awk -F/ '{print $2}').tar.gz \
    && tar -zxvf nginx-$(nginx -v 2>&1 | awk -F/ '{print $2}').tar.gz \
    && wget https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/get/master.zip \
    && unzip master.zip \
    && cd nginx-* \
    && ./configure --add-module=/usr/src/nginx/nginx-goodies-nginx-sticky-module-ng-* \
    && make \
    && make install

# Copy the existing nginx.conf to /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
