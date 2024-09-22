# Use the official PostgreSQL image
FROM postgres:13

# Environment variables to set up the user and database
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=fastapi

# Add an SQL script to initialize the database with the required table
COPY init.sql /docker-entrypoint-initdb.d/
