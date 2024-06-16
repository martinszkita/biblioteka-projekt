CREATE USER 'replicator'@'%' IDENTIFIED WITH mysql_native_password BY 'REP';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
FLUSH PRIVILEGES;