# Dockerfile for MySQL with SSL
FROM mysql:latest

# Copy the SSL certificates and keys to the container
COPY ssl/ca-cert.pem /etc/mysql/ssl/ca-cert.pem
COPY ssl/server-cert.pem /etc/mysql/ssl/server-cert.pem
COPY ssl/server-key.pem /etc/mysql/ssl/server-key.pem

# Set the correct permissions
RUN chmod 644 /etc/mysql/ssl/ca-cert.pem /etc/mysql/ssl/server-cert.pem && \
    chmod 600 /etc/mysql/ssl/server-key.pem

# Add SSL configuration to the MySQL configuration file
RUN echo "[mysqld]" >> /etc/mysql/my.cnf && \
    echo "ssl-ca=/etc/mysql/ssl/ca-cert.pem" >> /etc/mysql/my.cnf && \
    echo "ssl-cert=/etc/mysql/ssl/server-cert.pem" >> /etc/mysql/my.cnf && \
    echo "ssl-key=/etc/mysql/ssl/server-key.pem" >> /etc/mysql/my.cnf